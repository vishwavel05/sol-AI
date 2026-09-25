import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.resources.thamizhimorph import ThamizhiMorphAdapter


def parse_benchmark_cases(benchmark_file: Path) -> List[Dict[str, str]]:
    """
    Parse the morphology benchmark test cases directly from BENCHMARK.md (Section 3.4 Inflected).
    """
    cases = []
    if not benchmark_file.exists():
        return cases

    content = benchmark_file.read_text(encoding="utf-8")
    
    table_pattern = re.compile(
        r"\|?\s*(L\d{3})\s*\|\s*([^|]+)\s*\|\s*Inflected\s*\|\s*([^|]+)\s*\|\s*([^|\n]+)"
    )

    for match in table_pattern.finditer(content):
        case_id = match.group(1).strip()
        surface = match.group(2).strip()
        expected_lemma = match.group(3).strip()
        expected_features = match.group(4).strip()

        cases.append({
            "id": case_id,
            "surface": surface,
            "expected_lemma": expected_lemma,
            "expected_features": expected_features
        })

    return cases


def run_benchmark():
    """Execute ThamizhiMorph morphological benchmark with core vs guesser classification."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    benchmark_path = PROJECT_ROOT / "research" / "BENCHMARK.md"
    results_path = PROJECT_ROOT / "data" / "evaluation" / "thamizhimorph_results.json"

    results_path.parent.mkdir(parents=True, exist_ok=True)

    cases = parse_benchmark_cases(benchmark_path)
    if not cases:
        print(f"Error: No inflected test cases found in {benchmark_path}")
        sys.exit(1)

    adapter = ThamizhiMorphAdapter()
    detailed_results = []

    valid_core_count = 0
    guesser_only_count = 0
    unknown_count = 0
    lemma_match_count = 0
    core_lemma_match_count = 0

    print(f"Running ThamizhiMorph Benchmark ({len(cases)} cases)...\n")

    for case in cases:
        case_id = case["id"]
        surface = case["surface"]
        expected_lemma = case["expected_lemma"]
        expected_features = case["expected_features"]

        evidences = adapter.lookup(surface)

        analyses_data = []
        raw_outputs = []
        fst_models = []

        is_unknown = False
        has_core = False
        has_guesser = False
        lemma_matched = False
        core_lemma_matched = False

        for ev in evidences:
            status = ev.metadata.get("normalization_status")
            if status == "UNKNOWN":
                is_unknown = True
                continue

            analysis_type = ev.metadata.get("analysis_type", "core")
            raw_out = ev.metadata.get("raw_foma_output", "")
            fst_model = ev.metadata.get("fst_model", "")

            if analysis_type == "core":
                has_core = True
            elif analysis_type == "guesser":
                has_guesser = True

            if raw_out:
                raw_outputs.append(raw_out)
            if fst_model and fst_model not in fst_models:
                fst_models.append(fst_model)

            analyses_data.append({
                "lemma": ev.lemma,
                "pos": ev.pos,
                "morphology": ev.morphology,
                "analysis_type": analysis_type,
                "fst_model": fst_model,
                "raw_foma_output": raw_out
            })

            if ev.lemma:
                if ev.lemma == expected_lemma or expected_lemma in ev.lemma or ev.lemma in expected_lemma:
                    lemma_matched = True
                    if analysis_type == "core":
                        core_lemma_matched = True

        guesser_only = has_guesser and not has_core

        if is_unknown or not analyses_data:
            case_classification = "UNKNOWN"
            unknown_count += 1
        elif has_core:
            case_classification = "VALID_CORE"
            valid_core_count += 1
        else:
            case_classification = "GUESSER_ONLY"
            guesser_only_count += 1

        if lemma_matched:
            lemma_match_count += 1
        if core_lemma_matched:
            core_lemma_match_count += 1

        result_entry = {
            "id": case_id,
            "surface": surface,
            "expected_lemma": expected_lemma,
            "expected_features": expected_features,
            "classification": case_classification,
            "valid_core_analysis": has_core,
            "guesser_only_analysis": guesser_only,
            "unknown": is_unknown,
            "lemma_matched": lemma_matched,
            "core_lemma_matched": core_lemma_matched,
            "fst_models_used": fst_models,
            "analyses": analyses_data,
            "raw_foma_outputs": raw_outputs
        }
        detailed_results.append(result_entry)

    total = len(cases)
    lemma_acc = (lemma_match_count / total) * 100
    core_lemma_acc = (core_lemma_match_count / total) * 100

    benchmark_output = {
        "benchmark_name": "ThamizhiMorph Evaluation Benchmark (Core vs Guesser)",
        "total_cases": total,
        "valid_core_analyses": valid_core_count,
        "guesser_only_analyses": guesser_only_count,
        "unknown_cases": unknown_count,
        "overall_lemma_match_percent": round(lemma_acc, 2),
        "core_lemma_match_percent": round(core_lemma_acc, 2),
        "cases": detailed_results
    }

    results_path.write_text(json.dumps(benchmark_output, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print Summary
    print("=========================================================")
    print("   ThamizhiMorph Benchmark Results (Core vs Guesser)")
    print("=========================================================")
    print(f"Total Test Cases:          {total}")
    print(f"Valid Core Analyses:       {valid_core_count}")
    print(f"Guesser-Only Analyses:     {guesser_only_count}")
    print(f"Unknown Cases:             {unknown_count}")
    print(f"Overall Lemma Match Rate:  {lemma_acc:.1f}%")
    print(f"Core Lemma Match Rate:     {core_lemma_acc:.1f}%")
    print("=========================================================")
    print(f"Detailed results saved to: {results_path}\n")

    print(f"{'ID':<6} {'Surface':<20} {'Expected Lemma':<15} {'Classification':<16} {'FST Models'}")
    print("-" * 80)
    for c in detailed_results:
        fst_str = ", ".join(c["fst_models_used"]) if c["fst_models_used"] else "N/A"
        print(f"{c['id']:<6} {c['surface']:<20} {c['expected_lemma']:<15} {c['classification']:<16} {fst_str}")


if __name__ == "__main__":
    run_benchmark()
