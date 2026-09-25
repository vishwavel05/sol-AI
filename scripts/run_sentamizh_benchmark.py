import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.resources.sentamizh import SentamizhAdapter


def parse_all_benchmark_cases(benchmark_file: Path) -> List[Dict[str, str]]:
    """
    Parse benchmark test cases directly from BENCHMARK.md (Section 3).
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
    """Execute Sentamizh literary evidence retrieval benchmark against BENCHMARK.md."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    benchmark_path = PROJECT_ROOT / "research" / "BENCHMARK.md"
    results_path = PROJECT_ROOT / "data" / "evaluation" / "sentamizh_results.json"

    results_path.parent.mkdir(parents=True, exist_ok=True)

    cases = parse_all_benchmark_cases(benchmark_path)
    if not cases:
        print(f"Error: No benchmark cases found in {benchmark_path}")
        sys.exit(1)

    adapter = SentamizhAdapter()
    detailed_results = []

    total_cases = len(cases)
    total_found = 0
    total_occurrences = 0

    all_works_counter = Counter()
    category_stats: Dict[str, Dict[str, int]] = {}

    print(f"Running Sentamizh Literary Benchmark ({total_cases} cases)...\n")

    for case in cases:
        case_id = case["id"]
        query_word = case["word"]
        category = case["category"]

        if category not in category_stats:
            category_stats[category] = {"total": 0, "found": 0, "total_occurrences": 0}

        category_stats[category]["total"] += 1

        evidences = adapter.lookup(query_word)
        valid_evidences = [ev for ev in evidences if ev.metadata.get("status") == "FOUND"]

        is_found = len(valid_evidences) > 0
        occ_count = len(valid_evidences)

        if is_found:
            total_found += 1
            total_occurrences += occ_count
            category_stats[category]["found"] += 1
            category_stats[category]["total_occurrences"] += occ_count

        works = sorted(list(set([ev.work for ev in valid_evidences if ev.work])))
        for w in works:
            all_works_counter[w] += 1

        verse_ids = [ev.source_id for ev in valid_evidences if ev.source_id][:5]

        # Annotation availability counts
        thinai_count = sum(1 for ev in valid_evidences if ev.metadata.get("thinai"))
        turai_count = sum(1 for ev in valid_evidences if ev.metadata.get("turai"))
        speaker_count = sum(1 for ev in valid_evidences if ev.author)
        pann_count = sum(1 for ev in valid_evidences if ev.metadata.get("pann"))
        rasa_count = sum(1 for ev in valid_evidences if ev.metadata.get("rasa_primary"))
        cultural_count = sum(1 for ev in valid_evidences if ev.metadata.get("cultural_context"))
        english_count = sum(1 for ev in valid_evidences if ev.metadata.get("english"))

        detailed_results.append({
            "id": case_id,
            "category": category,
            "query": query_word,
            "found": is_found,
            "occurrences_count": occ_count,
            "works": works,
            "example_verse_ids": verse_ids,
            "annotation_availability": {
                "thinai": thinai_count,
                "turai": turai_count,
                "speaker_role": speaker_count,
                "pann": pann_count,
                "rasa_primary": rasa_count,
                "cultural_context": cultural_count,
                "english": english_count
            }
        })

    overall_pct = (total_found / total_cases) * 100 if total_cases > 0 else 0.0

    benchmark_output = {
        "benchmark_name": "Sentamizh Literary Evidence Retrieval Benchmark",
        "total_cases": total_cases,
        "overall_found_cases": total_found,
        "not_found_cases": total_cases - total_found,
        "total_literary_occurrences": total_occurrences,
        "overall_coverage_pct": round(overall_pct, 2),
        "work_distribution_in_hits": dict(all_works_counter),
        "category_breakdown": {
            cat: {
                "total": stats["total"],
                "found": stats["found"],
                "total_occurrences": stats["total_occurrences"],
                "coverage_pct": round((stats["found"] / stats["total"]) * 100, 2) if stats["total"] > 0 else 0.0
            }
            for cat, stats in category_stats.items()
        },
        "cases": detailed_results
    }

    results_path.write_text(json.dumps(benchmark_output, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print Summary
    print("=========================================================")
    print("   Sentamizh Literary Evidence Benchmark Results")
    print("=========================================================")
    print(f"Total Test Cases:         {total_cases}")
    print(f"Overall Found Cases:      {total_found} ({overall_pct:.1f}%)")
    print(f"Not Found Cases:          {total_cases - total_found}")
    print(f"Total Literary Matches:   {total_occurrences:,}")
    print("---------------------------------------------------------")
    print(f"{'Category':<15} {'Total':<8} {'Found':<8} {'Occurrences':<12} {'Coverage (%)'}")
    print("-" * 60)
    for cat, stats in category_stats.items():
        pct = (stats["found"] / stats["total"]) * 100 if stats["total"] > 0 else 0.0
        print(f"{cat:<15} {stats['total']:<8} {stats['found']:<8} {stats['total_occurrences']:<12} {pct:<15.1f}")
    print("=========================================================")
    print("Source Text Work Distribution in Hits:", dict(all_works_counter))
    print("=========================================================")
    print(f"Detailed results saved to: {results_path}\n")


if __name__ == "__main__":
    run_benchmark()
