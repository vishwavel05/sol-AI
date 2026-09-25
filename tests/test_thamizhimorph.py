import unittest
from backend.schemas.evidence import Evidence
from backend.resources.thamizhimorph import ThamizhiMorphAdapter


class TestThamizhiMorphAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = ThamizhiMorphAdapter()

    def test_known_noun(self):
        query = "மரங்களில்"
        evidences = self.adapter.lookup(query)
        self.assertIsInstance(evidences, list)
        self.assertGreaterEqual(len(evidences), 1)

        first_ev = evidences[0]
        self.assertIsInstance(first_ev, Evidence)
        self.assertEqual(first_ev.surface, query)
        self.assertEqual(first_ev.source, "ThamizhiMorph")
        self.assertEqual(first_ev.lemma, "மரம்")
        self.assertEqual(first_ev.pos, "noun")
        self.assertIn("raw_foma_output", first_ev.metadata)
        self.assertIn("fst_model", first_ev.metadata)

    def test_inflected_noun(self):
        query = "மரத்தை"
        evidences = self.adapter.lookup(query)
        self.assertGreaterEqual(len(evidences), 1)
        lemmas = [ev.lemma for ev in evidences if ev.lemma]
        self.assertIn("மரம்", lemmas)

    def test_known_verb(self):
        query = "வந்தார்கள்"
        evidences = self.adapter.lookup(query)
        self.assertGreaterEqual(len(evidences), 1)
        lemmas = [ev.lemma for ev in evidences if ev.lemma]
        self.assertIn("வா", lemmas)
        self.assertEqual(evidences[0].pos, "verb")

    def test_complex_verb(self):
        query = "சென்றுகொண்டிருந்தான்"
        evidences = self.adapter.lookup(query)
        self.assertGreaterEqual(len(evidences), 1)
        first_ev = evidences[0]
        self.assertEqual(first_ev.surface, query)
        self.assertEqual(first_ev.source, "ThamizhiMorph")
        self.assertIsNotNone(first_ev.lemma)

    def test_ambiguity_preservation(self):
        query = "வந்தார்கள்"
        evidences = self.adapter.lookup(query)
        # Came (he/she honorific) vs Came (they plural)
        self.assertGreaterEqual(len(evidences), 2)
        raw_outputs = [ev.metadata.get("raw_foma_output") for ev in evidences]
        self.assertEqual(len(raw_outputs), len(set(raw_outputs)))

    def test_unknown_word_safety(self):
        query = "xyz_unknown_nonword_123"
        evidences = self.adapter.lookup(query)
        self.assertEqual(len(evidences), 1)
        ev = evidences[0]
        self.assertEqual(ev.surface, query)
        self.assertIsNone(ev.lemma)
        self.assertEqual(ev.metadata.get("normalization_status"), "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
