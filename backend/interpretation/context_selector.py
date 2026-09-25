"""
Deterministic context selector for literary evidence (Sentamizh corpus).
Ranks and filters literary occurrences using a multi-signal scoring function
and work-diversity constraint to select a small, representative context set.
"""

from typing import List, Dict, Any, Optional
from backend.schemas.evidence import Evidence


class SentamizhContextSelector:
    """
    Scores and selects a small, representative, work-diverse subset of literary contexts.
    """

    def __init__(self, max_contexts: int = 5, max_per_work_initial: int = 1):
        self.max_contexts = max_contexts
        self.max_per_work_initial = max_per_work_initial

    def score_evidence(
        self, ev: Evidence, query: str, lemma_candidates: List[str]
    ) -> float:
        """
        Calculates a deterministic quality score based on surface/lemma match,
        verse completeness, metadata richness, and translation availability.
        """
        score = 0.0

        # Signal 1: Exact surface match
        if ev.lemma == query or (ev.passage and query in ev.passage):
            score += 10.0

        # Signal 2: Exact candidate lemma match
        if ev.lemma in lemma_candidates:
            score += 8.0

        # Signal 3: Complete verse / passage available
        passage_text = ev.passage or ev.metadata.get("classical_tamil", "")
        if passage_text and len(passage_text.strip()) > 10:
            score += 5.0

        # Signal 4: Metadata completeness (work, period, verse_number)
        if ev.work or ev.metadata.get("source_text"):
            score += 3.0
        if ev.period or ev.metadata.get("period"):
            score += 2.0
        if ev.metadata.get("verse_number"):
            score += 1.0

        # Signal 5: Modern Tamil translation / meaning available
        if ev.meaning or ev.metadata.get("modern_tamil"):
            score += 2.0

        return score

    def select(
        self,
        evidence_list: List[Evidence],
        query: str,
        lemma_candidates: Optional[List[str]] = None,
        max_contexts: Optional[int] = None,
    ) -> List[Evidence]:
        """
        Ranks evidence items by score, applies work diversity constraint,
        and returns up to max_contexts items.
        """
        if max_contexts is None:
            max_contexts = self.max_contexts

        if lemma_candidates is None:
            lemma_candidates = [query]

        if not evidence_list:
            return []

        # Score each evidence item
        scored_items = []
        for ev in evidence_list:
            s = self.score_evidence(ev, query, lemma_candidates)
            scored_items.append((s, ev))

        # Sort descending by score
        scored_items.sort(key=lambda x: x[0], reverse=True)

        selected: List[Evidence] = []
        work_counts: Dict[str, int] = {}

        # Pass 1: Select top candidates enforcing work diversity
        remaining_items = []
        for score, ev in scored_items:
            work_name = ev.work or ev.metadata.get("source_text", "UNKNOWN_WORK")
            count = work_counts.get(work_name, 0)
            if count < self.max_per_work_initial and len(selected) < max_contexts:
                selected.append(ev)
                work_counts[work_name] = count + 1
            else:
                remaining_items.append((score, ev))

        # Pass 2: Fill remaining slots up to max_contexts if needed
        if len(selected) < max_contexts and remaining_items:
            for score, ev in remaining_items:
                if len(selected) >= max_contexts:
                    break
                selected.append(ev)

        return selected
