import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.retrieval.engine import RetrievalEngine


def parse_benchmark_cases(benchmark_file: Path) -> List[Dict[str, str]]:
    """
    Parse all 60 benchmark cases (L001-L055 lexical cases + M001-M005 dedicated morphology cases) from BENCHMARK.md.
    """
    cases = []
    if not benchmark_file.exists():
        return cases

    content = benchmark_file.read_text(encoding="utf-8")
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
            current_category = "Archaic/Rare"
        elif line_strip.startswith("### 3.6"):
            current_category = "Modern/Technical"
        elif line_strip.startswith("## 5. Morphological"):
            current_category = "Morphology"

        if "---" in line_strip or "ID" in line_strip or "Word" in line_strip or "Surface Form" in line_strip:
            continue

        if line_strip.startswith("| L"):
            parts = [p.strip() for p in line_strip.split("|") if p.strip()]
            if len(parts) >= 2 and parts[0].startswith("L"):
                case_id = parts[0]
                word = parts[1]
                if not any(c["id"] == case_id for c in cases):
                    cases.append({
                        "id": case_id,
                        "word": word,
                        "category": current_category
                    })

        if line_strip.startswith("| M"):
            parts = [p.strip() for p in line_strip.split("|") if p.strip()]
            if len(parts) >= 3 and parts[0].startswith("M"):
                case_id = parts[0]
                word = parts[2]
                if not any(c["id"] == case_id for c in cases):
                    cases.append({
                        "id": case_id,
                        "word": word,
                        "category": "Morphology"
                    })

    return cases


def run_benchmark():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    benchmark_path = PROJECT_ROOT / "research" / "BENCHMARK.md"
    results_path = PROJECT_ROOT / "data" / "evaluation" / "unified_results.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)

    cases = parse_benchmark_cases(benchmark_path)
    if not cases:
        print(f"Error: Could not parse benchmark cases from {benchmark_path}")
        sys.exit(1)

    print(f"Loaded {len(cases)} benchmark cases from BENCHMARK.md.\n")

    engine = RetrievalEngine()
    detailed_cases = []

    # Overall Summary Counters
    total_cases = len(cases)
    any_evidence_count = 0
    multi_2plus_count = 0
    multi_3plus_count = 0
    multi_4_count = 0

    morphology_evidence_count = 0
    lexical_evidence_count = 0
    literary_evidence_count = 0

    cross_resource_agreement_count = 0
    cross_resource_conflicts_count = 0
    guesser_only_count = 0

    # Category Breakdown Structure
    categories = ["Common", "Literary", "Polysemous", "Inflected", "Archaic/Rare", "Modern/Technical", "Morphology"]
    cat_stats = {
        cat: {
            "total": 0,
            "any_evidence": 0,
            "multi_2plus": 0,
            "multi_3plus": 0,
            "lemma_agreement": 0,
            "literary_evidence": 0
        }
        for cat in categories
    }

    audit_targets = {}

    for case in cases:
        case_id = case["id"]
        word = case["word"]
        category = case["category"]

        if category not in cat_stats:
            cat_stats[category] = {
                "total": 0, "any_evidence": 0, "multi_2plus": 0,
                "multi_3plus": 0, "lemma_agreement": 0, "literary_evidence": 0
            }

        cat_stats[category]["total"] += 1

        # Execute Unified Retrieval
        res = engine.search(word)

        # 1. Filter ONLY valid FOUND evidence
        valid_evs = [ev for ev in res.evidence if ev.metadata.get("status") == "FOUND"]
        found_sources = sorted(list(set([ev.source for ev in valid_evs])))
        found_source_count = len(found_sources)

        # Resource-specific extractions
        tm_evs = [ev for ev in valid_evs if ev.source == "ThamizhiMorph"]
        tm_core = [ev for ev in tm_evs if ev.metadata.get("analysis_type") == "core"]
        tm_guesser = [ev for ev in tm_evs if ev.metadata.get("analysis_type") == "guesser"]
        tm_lemmas = sorted(list(set([ev.lemma for ev in tm_evs if ev.lemma])))

        ak_evs = [ev for ev in valid_evs if ev.source == "Thani Thamizh Akarathi"]
        ak_headwords = sorted(list(set([ev.lemma for ev in ak_evs if ev.lemma])))
        ak_meanings = [ev.meaning for ev in ak_evs if ev.meaning]

        wn_evs = [ev for ev in valid_evs if ev.source == "Tamil WordNet"]
        wn_lex = [ev for ev in wn_evs if ev.evidence_type == "lexical"]
        wn_morph = [ev for ev in wn_evs if ev.evidence_type == "morphology"]
        wn_freq = [ev for ev in wn_evs if ev.evidence_type == "frequency"]
        wn_rel_codes = sorted(list(set([ev.metadata.get("relation_code") for ev in wn_lex if ev.metadata.get("relation_code")])))

        sent_evs = [ev for ev in valid_evs if ev.source == "Sentamizh"]
        sent_works = sorted(list(set([ev.work for ev in sent_evs if ev.work])))
        sent_verse_ids = [ev.source_id for ev in sent_evs if ev.source_id][:5]

        # 2. Check Metrics
        has_any = found_source_count >= 1
        has_2plus = found_source_count >= 2
        has_3plus = found_source_count >= 3
        has_4 = found_source_count >= 4

        has_morph = len(tm_evs) > 0 or len(wn_morph) > 0
        has_lex = len(ak_evs) > 0 or len(wn_lex) > 0
        has_lit = len(sent_evs) > 0

        # Genuine Cross-Resource Lemma Agreement:
        # A candidate string supported by 2+ independent resources with FOUND evidence
        has_agreement = False
        for cand, sources in res.cross_resource_support.items():
            if len(sources) >= 2:
                has_agreement = True
                break

        # Genuine Cross-Resource Conflicts:
        # >1 candidate lemmas produced across resources
        has_conflict = len(res.lemma_candidates) > 1

        # Guesser-only dependency:
        # ThamizhiMorph provided ONLY guesser analyses and no other resource returned evidence
        is_guesser_only = (len(tm_guesser) > 0 and len(tm_core) == 0 and found_source_count == 1)

        # Update Summary Counters
        if has_any:
            any_evidence_count += 1
            cat_stats[category]["any_evidence"] += 1
        if has_2plus:
            multi_2plus_count += 1
            cat_stats[category]["multi_2plus"] += 1
        if has_3plus:
            multi_3plus_count += 1
            cat_stats[category]["multi_3plus"] += 1
        if has_4:
            multi_4_count += 1

        if has_morph:
            morphology_evidence_count += 1
        if has_lex:
            lexical_evidence_count += 1
        if has_lit:
            literary_evidence_count += 1
            cat_stats[category]["literary_evidence"] += 1

        if has_agreement:
            cross_resource_agreement_count += 1
            cat_stats[category]["lemma_agreement"] += 1

        if has_conflict:
            cross_resource_conflicts_count += 1

        if is_guesser_only:
            guesser_only_count += 1

        case_record = {
            "benchmark_id": case_id,
            "category": category,
            "query": word,
            "normalized_query": res.normalized_query,
            "lemma_candidates": res.lemma_candidates,
            "resources_attempted": ["ThamizhiMorph", "Thani Thamizh Akarathi", "Tamil WordNet", "Sentamizh"],
            "resources_with_evidence": found_sources,
            "evidence_count": len(valid_evs),
            "ThamizhiMorph_evidence": {
                "found": len(tm_evs) > 0,
                "total_entries": len(tm_evs),
                "core_count": len(tm_core),
                "guesser_count": len(tm_guesser),
                "lemmas": tm_lemmas
            },
            "Akarathi_evidence": {
                "found": len(ak_evs) > 0,
                "total_entries": len(ak_evs),
                "headwords": ak_headwords,
                "meanings": ak_meanings
            },
            "WordNet_evidence": {
                "found": len(wn_evs) > 0,
                "total_entries": len(wn_evs),
                "lexical_count": len(wn_lex),
                "morphology_count": len(wn_morph),
                "frequency_count": len(wn_freq),
                "relation_codes": wn_rel_codes
            },
            "Sentamizh_evidence": {
                "found": len(sent_evs) > 0,
                "total_entries": len(sent_evs),
                "works": sent_works,
                "verse_ids": sent_verse_ids
            },
            "cross_resource_support": res.cross_resource_support,
            "conflicting_candidates": has_conflict,
            "guesser_only_dependency": is_guesser_only,
            "errors": res.errors
        }

        detailed_cases.append(case_record)

        if word in ["மரங்களில்", "யாழ்", "அகதி"]:
            audit_targets[word] = case_record

    # Save Results JSON
    output_data = {
        "benchmark_name": "SOL AI Unified Retrieval Benchmark",
        "total_cases": total_cases,
        "cases_with_any_evidence": any_evidence_count,
        "cases_with_2plus_resources": multi_2plus_count,
        "cases_with_3plus_resources": multi_3plus_count,
        "cases_with_4_resources": multi_4_count,
        "morphology_evidence_cases": morphology_evidence_count,
        "lexical_evidence_cases": lexical_evidence_count,
        "literary_evidence_cases": literary_evidence_count,
        "cross_resource_lemma_agreement_cases": cross_resource_agreement_count,
        "cross_resource_conflicts_cases": cross_resource_conflicts_count,
        "guesser_only_cases": guesser_only_count,
        "category_breakdown": cat_stats,
        "cases": detailed_cases
    }

    results_path.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print Summary Metrics
    print("=========================================================")
    print("        SOL AI UNIFIED RETRIEVAL BENCHMARK")
    print("=========================================================")
    print(f"Total cases:                      {total_cases}")
    print(f"Cases with any evidence:          {any_evidence_count} ({(any_evidence_count/total_cases)*100:.1f}%)")
    print(f"Cases with 2+ resources:          {multi_2plus_count} ({(multi_2plus_count/total_cases)*100:.1f}%)")
    print(f"Cases with 3+ resources:          {multi_3plus_count} ({(multi_3plus_count/total_cases)*100:.1f}%)")
    print(f"Cases with 4 resources:           {multi_4_count} ({(multi_4_count/total_cases)*100:.1f}%)")
    print("---------------------------------------------------------")
    print(f"Morphology evidence:              {morphology_evidence_count}")
    print(f"Lexical evidence:                 {lexical_evidence_count}")
    print(f"Literary evidence:                {literary_evidence_count}")
    print("---------------------------------------------------------")
    print(f"Cross-resource lemma agreement:   {cross_resource_agreement_count}")
    print(f"Cross-resource conflicts:         {cross_resource_conflicts_count}")
    print(f"Guesser-only cases:               {guesser_only_count}")
    print("=========================================================")
    print("\nCATEGORY BREAKDOWN\n")
    print(f"{'Category':<18} {'Total':<7} {'Any-Ev':<8} {'2+-Res':<8} {'3+-Res':<8} {'Agreement':<11} {'Literary'}")
    print("-" * 75)
    for cat, stats in cat_stats.items():
        if stats["total"] > 0:
            print(f"{cat:<18} {stats['total']:<7} {stats['any_evidence']:<8} {stats['multi_2plus']:<8} {stats['multi_3plus']:<8} {stats['lemma_agreement']:<11} {stats['literary_evidence']}")
    print("=========================================================\n")

    # Print Detailed Audit for Three Key Queries
    print("=========================================================")
    print("         AUDIT OF THREE IMPORTANT QUERIES")
    print("=========================================================")

    for word in ["மரங்களில்", "யாழ்", "அகதி"]:
        rec = audit_targets.get(word)
        if rec:
            print(f"\nQUERY SURFACE:         {rec['query']}")
            print(f"LEMMA CANDIDATES:      {rec['lemma_candidates']}")
            print("RESOURCE EVIDENCE:")
            print(f"  - ThamizhiMorph:     {rec['ThamizhiMorph_evidence']}")
            print(f"  - Akarathi:          {rec['Akarathi_evidence']}")
            print(f"  - WordNet:           {rec['WordNet_evidence']}")
            print(f"  - Sentamizh:         {rec['Sentamizh_evidence']}")
            print(f"CROSS-RESOURCE SUPPORT: {rec['cross_resource_support']}")
            print(f"CONFLICTS DISCOVERED:  {rec['conflicting_candidates']}")
            print("-" * 60)

    print(f"\nDetailed benchmark results saved to: {results_path}\n")


if __name__ == "__main__":
    run_benchmark()
