import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.resources.akarathi import ThaniThamizhAkarathiAdapter


def parse_all_benchmark_cases(benchmark_file: Path) -> List[Dict[str, str]]:
    """
    Parse all lexical benchmark test cases directly from BENCHMARK.md (Section 3).
    """
    cases = []
    if not benchmark_file.exists():
        return cases

    content = benchmark_file.read_text(encoding="utf-8")
    
    # Table line pattern matching: | ID | Word | Category/Notes | ...
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
    """Execute Thani Thamizh Akarathi benchmark against BENCHMARK.md."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    benchmark_path = PROJECT_ROOT / "research" / "BENCHMARK.md"
    results_path = PROJECT_ROOT / "data" / "evaluation" / "akarathi_results.json"

    results_path.parent.mkdir(parents=True, exist_ok=True)

    cases = parse_all_benchmark_cases(benchmark_path)
    if not cases:
        print(f"Error: No benchmark cases found in {benchmark_path}")
        sys.exit(1)

    adapter = ThaniThamizhAkarathiAdapter()
    detailed_results = []

    total_cases = len(cases)
    found_cases = 0
    total_entries_returned = 0
    category_stats: Dict[str, Dict[str, int]] = {}

    print(f"Running Thani Thamizh Akarathi Benchmark ({total_cases} cases)...\n")

    for case in cases:
        case_id = case["id"]
        query_word = case["word"]
        category = case["category"]

        if category not in category_stats:
            category_stats[category] = {"total": 0, "found": 0, "entries": 0}

        category_stats[category]["total"] += 1

        evidences = adapter.lookup(query_word)
        valid_evidences = [ev for ev in evidences if ev.metadata.get("status") == "FOUND"]

        if valid_evidences:
            is_found = True
            found_cases += 1
            category_stats[category]["found"] += 1
            category_stats[category]["entries"] += len(valid_evidences)
            total_entries_returned += len(valid_evidences)
            failure_reason = None
        else:
            is_found = False
            failure_reason = f"No entry for '{query_word}' in Thani Thamizh Akarathi"

        meanings = [ev.meaning for ev in valid_evidences if ev.meaning]
        sources = list(set([ev.metadata.get("source_name", ev.source) for ev in valid_evidences]))

        detailed_results.append({
            "id": case_id,
            "category": category,
            "query": query_word,
            "found": is_found,
            "matching_headword": query_word if is_found else None,
            "number_of_entries": len(valid_evidences),
            "source_dictionaries": sources,
            "meanings_returned": meanings,
            "failure": failure_reason
        })

    not_found_cases = total_cases - found_cases
    coverage_pct = (found_cases / total_cases) * 100 if total_cases > 0 else 0.0

    benchmark_output = {
        "benchmark_name": "Thani Thamizh Akarathi Lexical Benchmark",
        "total_cases": total_cases,
        "found_cases": found_cases,
        "not_found_cases": not_found_cases,
        "coverage_percentage": round(coverage_pct, 2),
        "total_entries_returned": total_entries_returned,
        "category_breakdown": {
            cat: {
                "total": stats["total"],
                "found": stats["found"],
                "coverage_pct": round((stats["found"] / stats["total"]) * 100, 2) if stats["total"] > 0 else 0.0,
                "entries_returned": stats["entries"]
            }
            for cat, stats in category_stats.items()
        },
        "cases": detailed_results
    }

    results_path.write_text(json.dumps(benchmark_output, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print Summary
    print("=========================================================")
    print("   Thani Thamizh Akarathi Benchmark Results")
    print("=========================================================")
    print(f"Total Test Cases:         {total_cases}")
    print(f"Found Cases:              {found_cases}")
    print(f"Not Found Cases:          {not_found_cases}")
    print(f"Lexical Coverage:         {coverage_pct:.1f}%")
    print(f"Total Entries Returned:   {total_entries_returned}")
    print("---------------------------------------------------------")
    print(f"{'Category':<15} {'Total':<8} {'Found':<8} {'Coverage (%)':<15} {'Entries'}")
    print("-" * 60)
    for cat, stats in category_stats.items():
        pct = (stats["found"] / stats["total"]) * 100 if stats["total"] > 0 else 0.0
        print(f"{cat:<15} {stats['total']:<8} {stats['found']:<8} {pct:<15.1f} {stats['entries']}")
    print("=========================================================")
    print(f"Detailed results saved to: {results_path}\n")


if __name__ == "__main__":
    run_benchmark()
