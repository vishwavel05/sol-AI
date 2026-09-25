"""
SOL AI Contextual Interpretation Package.
"""

from backend.interpretation.schemas import (
    LiteraryContextItem,
    SOLResponse,
    EvidencePack,
)
from backend.interpretation.context_selector import SentamizhContextSelector
from backend.interpretation.evidence_pack import build_evidence_pack
from backend.interpretation.interpreter import (
    BaseLLMInterpreter,
    MockLLMInterpreter,
    GeminiLLMInterpreter,
    get_interpreter,
)

__all__ = [
    "LiteraryContextItem",
    "SOLResponse",
    "EvidencePack",
    "SentamizhContextSelector",
    "build_evidence_pack",
    "BaseLLMInterpreter",
    "MockLLMInterpreter",
    "GeminiLLMInterpreter",
    "get_interpreter",
]
