import unittest
from backend.schemas.evidence import Evidence
from backend.resources.wordnet import TamilWordNetAdapter


class TestTamilWordNetAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = TamilWordNetAdapter()

    def test_known_lexical_entry(self):
        query = "மரம்"
        evidences = self.adapter.lookup(query)
        self.assertIsInstance(evidences, list)
        self.assertGreaterEqual(len(evidences), 1)

        first_ev = evidences[0]
        self.assertIsInstance(first_ev, Evidence)
        self.assertEqual(first_ev.surface, query)
        self.assertEqual(first_ev.source, "Tamil WordNet")
        self.assertEqual(first_ev.lemma, "மரம்")
        self.assertEqual(first_ev.pos, "Noun")
        self.assertEqual(first_ev.metadata.get("status"), "FOUND")

    def test_known_morphtable_mapping(self):
        query = "மரங்களில்"
        evidences = self.adapter.lookup(query)
        self.assertGreaterEqual(len(evidences), 1)

        morph_evs = [ev for ev in evidences if ev.evidence_type == "morphology"]
        self.assertGreaterEqual(len(morph_evs), 1)
        self.assertEqual(morph_evs[0].lemma, "மரம்")

    def test_frequency_lookup(self):
        query = "குறிஞ்சி"
        evidences = self.adapter.lookup(query)
        self.assertGreaterEqual(len(evidences), 1)
        freq = evidences[0].metadata.get("corpus_frequency")
        self.assertIsNotNone(freq)
        self.assertEqual(freq, 71)

    def test_pos_retrieval(self):
        query = "கல்"
        evidences = self.adapter.lookup(query)
        poses = [ev.pos for ev in evidences if ev.pos]
        self.assertIn("Noun", poses)

    def test_missing_word_safety(self):
        query = "xyz_missing_word_999"
        evidences = self.adapter.lookup(query)
        self.assertEqual(len(evidences), 1)
        ev = evidences[0]
        self.assertEqual(ev.surface, query)
        self.assertIsNone(ev.lemma)
        self.assertEqual(ev.metadata.get("status"), "NOT_FOUND")

    def test_missing_null_metadata(self):
        query = "மரம்"
        evidences = self.adapter.lookup(query)
        first_ev = evidences[0]
        # Source dump gloss/example/english are 100% NULL
        self.assertIsNone(first_ev.meaning)

    def test_raw_relation_preservation(self):
        query = "மரம்"
        evidences = self.adapter.lookup(query)
        rel_codes = [ev.metadata.get("relation_code") for ev in evidences if ev.metadata.get("relation_code")]
        self.assertTrue(any(rc in ["3", "4"] for rc in rel_codes))

    def test_transliteration_conversion(self):
        query = "சொர்க்கம்"
        evidences = self.adapter.lookup(query)
        self.assertGreaterEqual(len(evidences), 1)
        self.assertEqual(evidences[0].metadata.get("raw_label"), "corkkam")


if __name__ == "__main__":
    unittest.main()
