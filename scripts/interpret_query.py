"""
CLI Demo script for SOL AI Contextual Interpretation Layer.
Searches deterministic retrieval engine, builds EvidencePack, and invokes BaseLLMInterpreter.
"""

import sys
import json
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.retrieval.engine import RetrievalEngine
from backend.interpretation.evidence_pack import build_evidence_pack
from backend.interpretation.interpreter import get_interpreter, BaseLLMInterpreter


def main():
    # Ensure stdout uses utf-8 on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="SOL AI Contextual Interpretation CLI Demo")
    parser.add_argument("query", type=str, help="Tamil query word to interpret")
    parser.add_argument("--provider", type=str, default=None, help="LLM provider: 'mock', 'gemini' (default: mock)")
    parser.add_argument("--debug", action="store_true", help="Print EvidencePack before LLM response")
    parser.add_argument("--max-contexts", type=int, default=5, help="Max literary contexts to include")

    args = parser.parse_args()
    query = args.query

    # Step 1: Deterministic Retrieval
    engine = RetrievalEngine()
    retrieval_result = engine.search(query)

    # Step 2: Build Evidence Pack
    pack = build_evidence_pack(retrieval_result, max_literary_contexts=args.max_contexts)

    if args.debug:
        print("=" * 60)
        print("DEBUG: EVIDENCE PACK")
        print("=" * 60)
        print(f"Query: {pack.query}")
        print(f"Normalized: {pack.normalized_query}")
        print(f"Lemma Candidates: {pack.lemma_candidates}")
        print(f"Counts: {pack.evidence_counts}")
        print(f"Morphology Items: {len(pack.morphology_evidence)}")
        print(f"Lexical Items: {len(pack.lexical_evidence)}")
        print(f"Selected Literary Items: {len(pack.literary_evidence)}")
        print(f"Conflicts: {pack.conflicts}")
        print("=" * 60)
        print()

    # Step 3: LLM Interpreter
    interpreter = get_interpreter(args.provider)
    response = interpreter.interpret(pack)

    # Output formatting
    print("=" * 60)
    print("SOL AI CONTEXTUAL RESPONSE")
    print("=" * 60)
    print(f"QUERY: {response.query}")
    print(f"LEMMA: {response.lemma or 'N/A'}")
    print(f"MEANING: {response.meaning or 'N/A'}")
    
    print("\nMORPHOLOGY:")
    if response.morphology:
        pos = response.morphology.get('pos', 'N/A')
        fst_model = response.morphology.get('fst_model')
        atype = response.morphology.get('analysis_type', 'N/A')
        model_str = f"{fst_model} ({atype})" if fst_model else atype
        print(f"  POS: {pos}")
        print(f"  Model: {model_str}")
        print(f"  Details: {response.morphology}")
    else:
        print("  None")

    print("\nCONTEXTUAL INTERPRETATION:")
    print(f"  {response.contextual_interpretation}")

    print("\nLITERARY CONTEXT:")
    if response.literary_context:
        for idx, item in enumerate(response.literary_context, 1):
            print(f"  [{idx}] Work: {item.work or 'N/A'} | Period: {item.period or 'N/A'} | Verse #: {item.verse_number or 'N/A'}")
            print(f"      Passage: {item.passage}")
            if item.meaning:
                print(f"      Modern Gloss: {item.meaning}")
    else:
        print("  None")

    print("\nRELATED INFORMATION:")
    if response.related_words:
        print(f"  {', '.join(response.related_words)}")
    else:
        print("  None")

    print("\nSOURCES:")
    print(f"  {', '.join(response.sources) if response.sources else 'None'}")

    print("\nUNCERTAINTIES:")
    if response.uncertainties:
        for u in response.uncertainties:
            print(f"  - {u}")
    else:
        print("  None")
    print("=" * 60)


if __name__ == "__main__":
    main()
