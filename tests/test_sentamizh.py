import unittest
from pathlib import Path
from backend.resources.sentamizh import SentamizhAdapter
from backend.schemas.evidence import Evidence


class TestSentamizhAdapter(unittest.TestCase):
    """
    Unit test suite for Sentamizh literary evidence adapter.
    """

    @classmethod
    def setUpClass(cls):
        cls.adapter = SentamizhAdapter()

    def test_known_literary_word(self):
        """1. Test lookup of a known classical literary word (யாழ்)."""
        evidences = self.adapter.lookup("யாழ்")
        self.assertGreater(len(evidences), 0)
        found_evs = [e for e in evidences if e.metadata.get("status") == "FOUND"]
        self.assertGreater(len(found_evs), 0)
        first = found_evs[0]
        self.assertEqual(first.source, "Sentamizh")
        self.assertEqual(first.evidence_type, "literary_context")
        self.assertIsNotNone(first.passage)
        self.assertIsNotNone(first.work)

    def test_known_common_word(self):
        """2. Test lookup of a known common Tamil word (மரம்)."""
        evidences = self.adapter.lookup("மரம்")
        found_evs = [e for e in evidences if e.metadata.get("status") == "FOUND"]
        self.assertGreater(len(found_evs), 0)
        self.assertTrue(any("மரம்" in e.passage for e in found_evs))

    def test_multiple_occurrences(self):
        """3. Test word with multiple occurrences across verses."""
        evidences = self.adapter.lookup("யாழ்")
        found_evs = [e for e in evidences if e.metadata.get("status") == "FOUND"]
        self.assertGreater(len(found_evs), 1)

    def test_multiple_works(self):
        """4. Test word that appears across multiple source works."""
        evidences = self.adapter.lookup("யாழ்")
        found_evs = [e for e in evidences if e.metadata.get("status") == "FOUND"]
        works = set(e.work for e in found_evs if e.work)
        self.assertGreater(len(works), 1)

    def test_missing_word(self):
        """5. Test lookup of a non-existent / missing word."""
        evidences = self.adapter.lookup("போலிச்சொல்வார்த்தை123")
        self.assertEqual(len(evidences), 1)
        self.assertEqual(evidences[0].metadata.get("status"), "NOT_FOUND")
        self.assertIsNone(evidences[0].passage)

    def test_unicode_handling(self):
        """6. Test Unicode normalization and punctuation handling."""
        evidences_clean = self.adapter.lookup("யாழ்")
        evidences_spaced = self.adapter.lookup("  யாழ்  ")
        self.assertEqual(len(evidences_clean), len(evidences_spaced))

    def test_metadata_preservation(self):
        """7. Test preservation of metadata fields and NULLs."""
        evidences = self.adapter.lookup("யாழ்")
        found_evs = [e for e in evidences if e.metadata.get("status") == "FOUND"]
        self.assertGreater(len(found_evs), 0)
        sample = found_evs[0]
        self.assertIn("verse_id", sample.metadata)
        self.assertIn("cultural_context", sample.metadata)

    def test_verse_source_preservation(self):
        """8. Test verse number, period, genre, and source preservation."""
        evidences = self.adapter.lookup("யாழ்")
        found_evs = [e for e in evidences if e.metadata.get("status") == "FOUND"]
        sample = found_evs[0]
        self.assertIsNotNone(sample.source_id)
        self.assertIsNotNone(sample.period)
        self.assertIsNotNone(sample.genre)


if __name__ == "__main__":
    unittest.main()
