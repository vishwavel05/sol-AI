"""
Unit tests for SentamizhContextSelector.
Verifies scoring signals, work diversity constraint, context limits, and empty handling.
"""

import unittest
from backend.schemas.evidence import Evidence
from backend.interpretation.context_selector import SentamizhContextSelector


class TestSentamizhContextSelector(unittest.TestCase):
    """
    Tests deterministic context selection, scoring rules, and work-diversity constraint.
    """

    def setUp(self):
        self.selector = SentamizhContextSelector(max_contexts=5, max_per_work_initial=1)

    def test_empty_input(self):
        """Test handling of empty evidence lists."""
        res = self.selector.select([], query="மரங்களில்")
        self.assertEqual(res, [])

    def test_max_context_limit(self):
        """Test that context selector never exceeds max_contexts limit."""
        mock_evs = []
        for i in range(24):
            mock_evs.append(
                Evidence(
                    surface="மரங்களில்",
                    source="Sentamizh",
                    evidence_type="literary",
                    lemma="மரம்",
                    passage=f"மரம் பற்றிய பாடல் {i}",
                    work=f"Work_{i % 6}",
                    metadata={"source_text": f"Work_{i % 6}", "classical_tamil": f"மரம் பற்றிய பாடல் {i}"},
                )
            )

        selected = self.selector.select(mock_evs, query="மரங்களில்", lemma_candidates=["மரம்"], max_contexts=5)
        self.assertLessEqual(len(selected), 5)
        self.assertEqual(len(selected), 5)

    def test_work_diversity_constraint(self):
        """Test that selected contexts prioritize distinct works rather than duplicates from one work."""
        evs = [
            Evidence(surface="மரங்களில்", source="Sentamizh", evidence_type="literary", lemma="மரம்", work="Kuruntokai", passage="மரங்களில் பறவை 1"),
            Evidence(surface="மரங்களில்", source="Sentamizh", evidence_type="literary", lemma="மரம்", work="Kuruntokai", passage="மரங்களில் பறவை 2"),
            Evidence(surface="மரங்களில்", source="Sentamizh", evidence_type="literary", lemma="மரம்", work="Kuruntokai", passage="மரங்களில் பறவை 3"),
            Evidence(surface="மரங்களில்", source="Sentamizh", evidence_type="literary", lemma="மரம்", work="Manimekalai", passage="மரங்களில் பூக்கள் 1"),
            Evidence(surface="மரங்களில்", source="Sentamizh", evidence_type="literary", lemma="மரம்", work="Natrinai", passage="மரங்களில் பழங்கள் 1"),
            Evidence(surface="மரங்களில்", source="Sentamizh", evidence_type="literary", lemma="மரம்", work="Silappatikaram", passage="மரங்களில் கிளைகள் 1"),
        ]

        selected = self.selector.select(evs, query="மரங்களில்", lemma_candidates=["மரம்"], max_contexts=4)
        works = [e.work for e in selected]
        self.assertEqual(len(selected), 4)
        # 4 distinct works must be selected
        self.assertEqual(set(works), {"Kuruntokai", "Manimekalai", "Natrinai", "Silappatikaram"})


if __name__ == "__main__":
    unittest.main()
