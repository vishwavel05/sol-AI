from dataclasses import dataclass, field
from typing import List, Dict, Any
from backend.schemas.evidence import Evidence


@dataclass
class UnifiedResult:
    """
    Unified retrieval result object for SOL AI.
    Aggregates evidence across all resource adapters while preserving source provenance.
    """
    query: str
    normalized_query: str
    lemma_candidates: List[str] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    resource_summary: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    cross_resource_support: Dict[str, List[str]] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert UnifiedResult instance to a JSON-serializable dictionary."""
        return {
            "query": self.query,
            "normalized_query": self.normalized_query,
            "lemma_candidates": self.lemma_candidates,
            "evidence": [ev.to_dict() for ev in self.evidence],
            "resource_summary": self.resource_summary,
            "cross_resource_support": self.cross_resource_support,
            "errors": self.errors,
        }
