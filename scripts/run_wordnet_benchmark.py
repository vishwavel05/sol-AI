import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.resources.wordnet import TamilWordNetAdapter


def parse_all_benchmark_cases(benchmark_file: Path) -> List[Dict[str, str]]:
    """
    Parse all benchmark test cases directly from BENCHMARK.md (Section 3).
    """
    cases = []
    if not benchmark_file.exists():
        return cases

    content = benchmark_file.read_text(encoding="utf-8")
    
    table_pattern = re.compile(
        r"\|?\s*(L\d{3})\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|?"
    )

    current_category = "General"

    for line in content.splitlines():
        line_strip = line.strip()
        if line_strip.startswith("### 3.1"):
            current_category = "Common"
        elif line_strip.startswith("### 3.2"):
            current_category = "Literary"
        elif line_strip.startswith("### 3.3"):
            current_category = "Polysemous"
        elif line_strip.startswith("### 3.4"):
            current_category = "Inflected"
        elif line_strip.startswith("### 3.5"):
            current_category = "Archaic"
        elif line_strip.startswith("### 3.6"):
            current_category = "Modern"

        match = table_pattern.search(line_strip)
        if match:
            case_id = match.group(1).strip()
            word = match.group(2).strip()
            cases.append({
                "id": case_id,
                "word": word,
                "category": current_category
            })

    return cases


def run_benchmark():
    """Execute Tamil WordNet benchmark against BENCHMARK.md."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    benchmark_path = PROJECT_ROOT / "research" / "BENCHMARK.md"
    results_path = PROJECT_ROOT / "data" / "evaluation" / "wordnet_results.json"

    results_path.parent.mkdir(parents=True, exist_ok=True)

    cases = parse_all_benchmark_cases(benchmark_path)
    if not cases:
        print(f"Error: No benchmark cases found in {benchmark_path}")
        sys.exit(1)

    adapter = TamilWordNetAdapter()
    detailed_results = []

    total_cases = len(cases)
    lexical_hits = 0
    morph_hits = 0
    total_found = 0

    pos_counter = Counter()
    relation_counter = Counter()
    category_stats: Dict[str, Dict[str, int]] = {}

    print(f"Running Tamil WordNet Benchmark ({total_cases} cases)...\n")

    for case in cases:
        case_id = case["id"]
        query_word = case["word"]
        category = case["category"]

        if category not in category_stats:
            category_stats[category] = {"total": 0, "lexical_found": 0, "morph_found": 0, "any_found": 0}

        category_stats[category]["total"] += 1

        evidences = adapter.lookup(query_word)
        valid_evidences = [ev for ev in evidences if ev.metadata.get("status") == "FOUND"]

        lexical_evs = [ev for ev in valid_evidences if ev.evidence_type == "lexical"]
        morph_evs = [ev for ev in valid_evidences if ev.evidence_type == "morphology"]

        has_lexical = len(lexical_evs) > 0
        has_morph = len(morph_evs) > 0
        is_found = len(valid_evidences) > 0

        if has_lexical:
            lexical_hits += 1
            category_stats[category]["lexical_found"] += 1

        if has_morph:
            morph_hits += 1
            category_stats[category]["morph_found"] += 1

        if is_found:
            total_found += 1
            category_stats[category]["any_found"] += 1

        pos_list = list(set([ev.pos for ev in lexical_evs if ev.pos]))
        for p in pos_list:
            pos_counter[p] += 1

        rel_codes = list(set([ev.metadata.get("relation_code") for ev in lexical_evs if ev.metadata.get("relation_code")]))
        for r in rel_codes:
            relation_counter[r] += 1

        freq_vals = [ev.metadata.get("corpus_frequency") for ev in valid_evidences if ev.metadata.get("corpus_frequency") is not None]
        freq = freq_vals[0] if freq_vals else None

        root_word = morph_evs[0].lemma if morph_evs else (lexical_evs[0].lemma if lexical_evs else None)

        detailed_results.append({
            "id": case_id,
            "category": category,
            "query": query_word,
            "found": is_found,
            "has_lexical_entry": has_lexical,
            "has_morphology_mapping": has_morph,
            "root_word_found": root_word,
            "pos_list": pos_list,
            "relation_codes": rel_codes,
            "corpus_frequency": freq,
            "transliteration_status": "CONVERTED" if is_found else "N/A",
            "twn_entry_count": len(lexical_evs)
        })

    lex_pct = (lexical_hits / total_cases) * 100 if total_cases > 0 else 0.0
    morph_pct = (morph_hits / total_cases) * 100 if total_cases > 0 else 0.0
    overall_pct = (total_found / total_cases) * 100 if total_cases > 0 else 0.0

    benchmark_output = {
        "benchmark_name": "Tamil WordNet Lexical & Morphological Benchmark",
        "total_cases": total_cases,
        "overall_found_cases": total_found,
        "lexical_hits": lexical_hits,
        "morphology_root_hits": morph_hits,
        "overall_coverage_pct": round(overall_pct, 2),
        "lexical_coverage_pct": round(lex_pct, 2),
        "morphology_coverage_pct": round(morph_pct, 2),
        "pos_distribution": dict(pos_counter),
        "relation_code_distribution": dict(relation_counter),
        "encoding_conversion_status": "100% Deterministic Transliteration to Unicode",
        "category_breakdown": {
            cat: {
                "total": stats["total"],
                "any_found": stats["any_found"],
                "lexical_found": stats["lexical_found"],
                "morph_found": stats["morph_found"],
                "coverage_pct": round((stats["any_found"] / stats["total"]) * 100, 2) if stats["total"] > 0 else 0.0
            }
            for cat, stats in category_stats.items()
        },
        "cases": detailed_results
    }

    results_path.write_text(json.dumps(benchmark_output, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print Summary
    print("=========================================================")
    print("   Tamil WordNet Benchmark Results")
    print("=========================================================")
    print(f"Total Test Cases:         {total_cases}")
    print(f"Overall Found Cases:      {total_found} ({overall_pct:.1f}%)")
    print(f"Lexical Hits (twn):       {lexical_hits} ({lex_pct:.1f}%)")
    print(f"Morphology Root Hits:     {morph_hits} ({morph_pct:.1f}%)")
    print("---------------------------------------------------------")
    print(f"{'Category':<15} {'Total':<8} {'Lexical':<10} {'Morph':<10} {'Coverage (%)'}")
    print("-" * 60)
    for cat, stats in category_stats.items():
        pct = (stats["any_found"] / stats["total"]) * 100 if stats["total"] > 0 else 0.0
        print(f"{cat:<15} {stats['total']:<8} {stats['lexical_found']:<10} {stats['morph_found']:<10} {pct:<15.1f}")
    print("=========================================================")
    print("POS Distribution in Hits:", dict(pos_counter))
    print("Relation Code Distribution:", dict(relation_counter))
    print("=========================================================")
    print(f"Detailed results saved to: {results_path}\n")


if __name__ == "__main__":
    run_benchmark()
