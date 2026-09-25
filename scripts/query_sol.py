import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.retrieval.engine import RetrievalEngine


def format_evidence_summary(evidences):
    """Format evidence objects concisely for terminal display."""
    lines = []
    found_evs = [e for e in evidences if e.metadata.get("status") == "FOUND"]
    if not found_evs:
        return "  Status: NOT_FOUND"

    for i, ev in enumerate(found_evs[:5], 1):
        if ev.source == "ThamizhiMorph":
            analysis_type = ev.metadata.get("analysis_type", "unknown").upper()
            model = ev.metadata.get("fst_model", "")
            lines.append(f"  [{i}] Lemma: {ev.lemma:<10} POS: {ev.pos or 'N/A':<8} Model: {model:<15} ({analysis_type})")
            if ev.morphology:
                lines.append(f"      Morphology: {ev.morphology}")

        elif ev.source == "Tamil WordNet":
            ev_type = ev.evidence_type.upper()
            freq = ev.metadata.get("corpus_frequency")
            freq_str = f", Freq: {freq}" if freq is not None else ""
            lines.append(f"  [{i}] Type: {ev_type:<10} Lemma/Root: {ev.lemma or 'N/A':<12} POS: {ev.pos or 'N/A'}{freq_str}")
            if ev.metadata.get("relation_code"):
                lines.append(f"      Relation Code: {ev.metadata.get('relation_code')}")

        elif ev.source == "Thani Thamizh Akarathi":
            dict_name = ev.metadata.get("dictionary", "Akarathi")
            lines.append(f"  [{i}] Headword: {ev.lemma:<10} Meaning: {ev.meaning}")
            lines.append(f"      Dict: {dict_name}")

        elif ev.source == "Tamil Wiktionary":
            lines.append(f"  [{i}] Headword: {ev.lemma:<10} Meaning: {ev.meaning}")

        elif ev.source == "Sentamizh":
            passage_snippet = ev.passage.replace("\n", " ") if ev.passage else ""
            if len(passage_snippet) > 80:
                passage_snippet = passage_snippet[:80] + "..."
            lines.append(f"  [{i}] Work: {ev.work:<15} Verse ID: {ev.source_id:<10} Period: {ev.period or 'N/A'}")
            lines.append(f"      Passage: {passage_snippet}")

    if len(found_evs) > 5:
        lines.append(f"  ... and {len(found_evs) - 5} more entries.")

    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("Usage: python scripts/query_sol.py <tamil_query>")
        sys.exit(1)

    query = sys.argv[1]
    engine = RetrievalEngine()
    result = engine.search(query)

    print("\n" + "=" * 65)
    print("                    SOL AI UNIFIED RETRIEVAL")
    print("=" * 65)
    print(f"QUERY:             {result.query}")
    print(f"NORMALIZED QUERY:  {result.normalized_query}")
    print(f"LEMMA CANDIDATES:  {', '.join(result.lemma_candidates) if result.lemma_candidates else 'None'}")
    print("=" * 65)

    resources = ["ThamizhiMorph", "Tamil WordNet", "Tamil Wiktionary", "Thani Thamizh Akarathi", "Sentamizh"]

    for res in resources:
        res_summary = result.resource_summary.get(res, {})
        status = res_summary.get("status", "NOT_FOUND")
        total = res_summary.get("total_entries", 0)
        res_evs = [ev for ev in result.evidence if ev.source == res]

        print(f"\n[{res}] (Status: {status}, Hits: {total})")
        print("-" * 65)
        print(format_evidence_summary(res_evs))

    print("\n" + "=" * 65)
    print("                 CROSS-RESOURCE SUPPORT ANALYSIS")
    print("=" * 65)
    if result.cross_resource_support:
        for lemma, sources in result.cross_resource_support.items():
            sources_str = ", ".join(sources)
            print(f"  Candidate Lemma / Form: {lemma:<15} → Supported by [{sources_str}]")
    else:
        print("  No cross-resource agreement detected.")

    if result.errors:
        print("\n" + "=" * 65)
        print("                        RESOURCE ERRORS")
        print("=" * 65)
        for res, err in result.errors.items():
            print(f"  {res}: {err}")

    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
