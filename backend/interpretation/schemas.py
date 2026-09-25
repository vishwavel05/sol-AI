"""
Pydantic schemas and dataclasses for the SOL AI Contextual Interpretation Layer.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.schemas.evidence import Evidence


class LiteraryContextItem(BaseModel):
    """Represents a single selected literary context occurrence."""

    work: Optional[str] = Field(default=None, description="Name of the literary work (e.g. Kuruntokai)")
    author: Optional[str] = Field(default=None, description="Author if available")
    period: Optional[str] = Field(default=None, description="Historical period (e.g. Sangam)")
    passage: Optional[str] = Field(default=None, description="Classical Tamil verse or passage")
    verse_number: Optional[str] = Field(default=None, description="Verse or line number")
    meaning: Optional[str] = Field(default=None, description="Modern Tamil translation or meaning")
    source: str = Field(default="Sentamizh", description="Source corpus name")


class SOLResponse(BaseModel):
    """
    Structured response schema for SOL AI interpretation layer.
    Strictly grounded in retrieved evidence.
    """

    query: str = Field(description="Original user query string")
    normalized_query: str = Field(description="Normalized query string")
    lemma: Optional[str] = Field(default=None, description="Primary root/lemma determined from evidence")
    meaning: Optional[str] = Field(default=None, description="Primary meaning(s) supported by dictionary evidence")
    english_meaning: Optional[str] = Field(default=None, description="English translation of the meaning")
    morphology: Optional[Dict[str, Any]] = Field(
        default=None, description="Morphological breakdown (POS, root, suffixes, model type)"
    )
    contextual_meaning: Optional[str] = Field(
        default=None, description="Precise meaning specifically derived from the query_context, if provided"
    )
    contextual_interpretation: Optional[str] = Field(
        default=None, description="Grounded explanation synthesizing available evidence without fabrication"
    )
    literary_context: List[LiteraryContextItem] = Field(
        default_factory=list, description="Selected representative classical literary verses/passages"
    )
    related_words: List[str] = Field(
        default_factory=list, description="Related lemmas or synset terms found in evidence"
    )
    sources: List[str] = Field(
        default_factory=list, description="List of contributing resource names"
    )
    uncertainties: List[str] = Field(
        default_factory=list, description="Explicit notes on missing data, conflicts, or guesser analyses"
    )
    evidence_summary: Dict[str, Any] = Field(
        default_factory=dict, description="Summary counts and resource hit statuses"
    )


class EvidencePack(BaseModel):
    """
    Container for all structured evidence passed to the LLM interpreter.
    Preserves original Evidence objects in un-flattened form.
    """

    query: str
    normalized_query: str
    query_context: Optional[str] = None
    lemma_candidates: List[str] = Field(default_factory=list)
    morphology_evidence: List[Evidence] = Field(default_factory=list)
    lexical_evidence: List[Evidence] = Field(default_factory=list)
    literary_evidence: List[Evidence] = Field(default_factory=list)
    related_evidence: List[Evidence] = Field(default_factory=list)
    conflicts: List[Dict[str, Any]] = Field(default_factory=list)
    source_provenance: Dict[str, Any] = Field(default_factory=dict)
    evidence_counts: Dict[str, int] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True
