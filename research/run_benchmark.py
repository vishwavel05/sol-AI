import sys
import os
import re
import json
import urllib.request
import urllib.error
from pathlib import Path

# Fix Windows console encoding for Tamil characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Config
API_URL = "http://localhost:8000/api/query"
BENCHMARK_FILE = Path(__file__).parent / "BENCHMARK.md"
OUTPUT_FILE = Path(__file__).parent / "BENCHMARK_RESULTS.md"

def parse_benchmark_md():
    cases = []
    
    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        # Match markdown table rows starting with Lxxx
        if re.match(r"^\|\s*L\d{3}\s*\|", line):
            parts = [p.strip() for p in line.split("|")]
            # parts will be ['', 'L001', 'வீடு', 'Common', 'Everyday noun', '']
            if len(parts) >= 5:
                case_id = parts[1]
                word = parts[2]
                category = parts[3]
                expected_lemma = None
                expected_features = None
                
                # Check if it's the 5-column inflected table
                if category.lower() == "inflected" and len(parts) >= 6:
                    expected_lemma = parts[4]
                    expected_features = parts[5]
                
                cases.append({
                    "id": case_id,
                    "word": word,
                    "category": category,
                    "expected_lemma": expected_lemma,
                    "expected_features": expected_features
                })
    return cases

def query_api(word):
    data = json.dumps({"query": word, "provider": "mock"}).encode("utf-8")
    req = urllib.request.Request(
        API_URL, 
        data=data, 
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error querying {word}: {e}")
        return None

def main():
    print("Parsing BENCHMARK.md...")
    cases = parse_benchmark_md()
    print(f"Found {len(cases)} test cases.")
    
    results = []
    
    stats = {
        "total": len(cases),
        "found": 0,
        "literary_total": 0,
        "literary_found": 0,
        "morph_total": 0,
        "morph_found": 0,
        "combined_total": len(cases),
        "combined_found": 0
    }
    
    print("Running API tests...")
    for i, case in enumerate(cases):
        word = case["word"]
        print(f"[{i+1}/{len(cases)}] Querying: {word} ... ", end="", flush=True)
        
        api_res = query_api(word)
        
        case_res = {
            "id": case["id"],
            "word": word,
            "category": case["category"],
            "status": "FAIL",
            "retrieved_lemma": "-",
            "sources_count": 0,
            "has_literary": False,
            "morph_match": False,
            "actual_features": "-"
        }
        
        if api_res:
            meaning = api_res.get("meaning", "")
            lemma = api_res.get("lemma", "")
            evidence = api_res.get("evidence_summary", {})
            total_found = evidence.get("total_found", 0)
            lit_context = api_res.get("literary_context", [])
            sources = api_res.get("sources", [])
            morph = api_res.get("morphology", {})
            
            # 1. Lexical Coverage
            if meaning or lemma or total_found > 0:
                stats["found"] += 1
                case_res["status"] = "PASS"
            
            case_res["retrieved_lemma"] = lemma or "-"
            case_res["sources_count"] = len(sources)
            case_res["has_literary"] = len(lit_context) > 0
            
            # Format actual features for report if present
            if morph:
                feats = []
                if "part_of_speech" in morph: feats.append(morph["part_of_speech"])
                if "tense" in morph: feats.append(morph["tense"])
                if "person" in morph: feats.append(morph["person"])
                if "number" in morph: feats.append(morph["number"])
                if "case_marker" in morph: feats.append(morph["case_marker"])
                case_res["actual_features"] = " + ".join([f for f in feats if f]) or "-"
            
            # 2. Literary Retrieval
            if case["category"].lower() == "literary":
                stats["literary_total"] += 1
                if case_res["has_literary"]:
                    stats["literary_found"] += 1
                    
            # 3. Morphological Accuracy
            if case["category"].lower() == "inflected":
                stats["morph_total"] += 1
                expected = case["expected_lemma"]
                if expected and lemma and expected.strip() == lemma.strip():
                    case_res["morph_match"] = True
                    stats["morph_found"] += 1
                    
            # 4. Combined Evidence
            if len(sources) >= 2:
                stats["combined_found"] += 1
                
            print("OK")
        else:
            print("ERROR")
            
        results.append(case_res)

    print("\nGenerating report...")
    
    # Calculate percentages
    lexical_score = (stats["found"] / stats["total"]) * 100 if stats["total"] else 0
    literary_score = (stats["literary_found"] / stats["literary_total"]) * 100 if stats["literary_total"] else 0
    morph_score = (stats["morph_found"] / stats["morph_total"]) * 100 if stats["morph_total"] else 0
    combined_score = (stats["combined_found"] / stats["combined_total"]) * 100 if stats["combined_total"] else 0

    report = f"""# SOL AI — Benchmark Results

This file was automatically generated by `run_benchmark.py`.

## 1. Summary Metrics

| Metric | Score | Details |
|---|---|---|
| **Lexical Coverage** | **{lexical_score:.1f}%** | {stats['found']} / {stats['total']} words |
| **Morphological Accuracy** | **{morph_score:.1f}%** | {stats['morph_found']} / {stats['morph_total']} inflected words matched expected lemma |
| **Literary Retrieval** | **{literary_score:.1f}%** | {stats['literary_found']} / {stats['literary_total']} literary words returned context |
| **Combined Evidence Coverage** | **{combined_score:.1f}%** | {stats['combined_found']} / {stats['combined_total']} words had ≥2 sources |

---

## 2. Detailed Results by Category
"""

    # Group results by category
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)
        
    for cat, cases in categories.items():
        cat_total = len(cases)
        cat_passed = sum(1 for c in cases if c["status"] == "PASS")
        cat_score = (cat_passed / cat_total) * 100 if cat_total else 0
        
        report += f"\n### {cat} Words (Score: {cat_score:.1f}% - {cat_passed}/{cat_total})\n\n"
        report += "| ID | Word | Status | Retrieved Lemma | Sources | Lit. Context | Morph Match? | Extracted Features |\n"
        report += "|---|---|---|---|---|---|---|---|\n"
        
        for r in cases:
            status_icon = "✅ PASS" if r["status"] == "PASS" else "❌ FAIL"
            lit_icon = "📖 YES" if r["has_literary"] else "-"
            morph_icon = "✅ YES" if r["morph_match"] else ("❌ NO" if r["category"].lower() == "inflected" else "-")
            
            row = f"| {r['id']} | {r['word']} | {status_icon} | {r['retrieved_lemma']} | {r['sources_count']} | {lit_icon} | {morph_icon} | {r['actual_features']} |\n"
            report += row

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Done! Results written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
