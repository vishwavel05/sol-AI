"""
End-to-end offline integration test suite for SOL AI.
Verifies complete pipeline from Query -> Retrieval -> EvidencePack -> ContextSelection -> Interpreter -> SOLResponse.
"""

import unittest
from backend.retrieval.engine import RetrievalEngine
from backend.interpretation.evidence_pack import build_evidence_pack
from backend.interpretation.interpreter import MockLLMInterpreter
from backend.interpretation.schemas import SOLResponse


class TestEndToEndIntegration(unittest.TestCase):
    """
    Offline end-to-end integration test suite.
    """

    @classmethod
    def setUpClass(cls):
        cls.engine = RetrievalEngine()
        cls.interpreter = MockLLMInterpreter()

    def test_marangalil_e2e_pipeline(self):
        """1. End-to-end pipeline for inflected word 'மரங்களில்'."""
        query = "மரங்களில்"
        # 1. Retrieval
        retrieval_result = self.engine.search(query)
        self.assertEqual(retrieval_result.normalized_query, "மரங்களில்")

        # 2. EvidencePack & Context Selection
        pack = build_evidence_pack(retrieval_result, max_literary_contexts=5)
        self.assertIn("மரம்", pack.lemma_candidates)
        self.assertGreater(len(pack.morphology_evidence), 0)
        self.assertGreater(len(pack.literary_evidence), 0)

        # 3. Interpretation -> SOLResponse
        response = self.interpreter.interpret(pack)
        self.assertIsInstance(response, SOLResponse)
        self.assertEqual(response.query, "மரங்களில்")
        self.assertEqual(response.lemma, "மரம்")
        self.assertIsNotNone(response.morphology)
        self.assertGreater(len(response.literary_context), 0)
        self.assertIn("ThamizhiMorph", response.sources)
        self.assertIn("Sentamizh", response.sources)

    def test_yaazh_e2e_pipeline(self):
        """2. End-to-end pipeline for classical literary word 'யாழ்'."""
        query = "யாழ்"
        retrieval_result = self.engine.search(query)
        pack = build_evidence_pack(retrieval_result, max_literary_contexts=5)
        response = self.interpreter.interpret(pack)

        self.assertIsInstance(response, SOLResponse)
        self.assertEqual(response.query, "யாழ்")
        self.assertEqual(response.lemma, "யாழ்")
        self.assertGreater(len(response.literary_context), 0)
        self.assertIn("Sentamizh", response.sources)

    def test_agathi_e2e_pipeline(self):
        """3. End-to-end pipeline for purist dictionary word 'அகதி'."""
        query = "அகதி"
        retrieval_result = self.engine.search(query)
        pack = build_evidence_pack(retrieval_result, max_literary_contexts=5)
        response = self.interpreter.interpret(pack)

        self.assertIsInstance(response, SOLResponse)
        self.assertEqual(response.query, "அகதி")
        self.assertEqual(response.lemma, "அகதி")
        self.assertIsNotNone(response.meaning)
        self.assertIn("Thani Thamizh Akarathi", response.sources)
        self.assertIn("Tamil WordNet", response.sources)


if __name__ == "__main__":
    unittest.main()
