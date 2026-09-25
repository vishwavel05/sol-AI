from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Evidence:
    """
    Unified evidence data model for SOL AI.
    Captures lexical, morphological, semantic, and literary evidence from resources.
    """
    surface: str
    lemma: Optional[str] = None
    source: str = ""
    evidence_type: str = ""
    meaning: Optional[str] = None
    english_meaning: Optional[str] = None
    pos: Optional[str] = None
    morphology: Optional[str] = None
    passage: Optional[str] = None
    work: Optional[str] = None
    author: Optional[str] = None
    period: Optional[str] = None
    genre: Optional[str] = None
    verse: Optional[str] = None
    line: Optional[str] = None
    relations: List[Any] = field(default_factory=list)
    source_url: Optional[str] = None
    source_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert evidence instance to a dictionary."""
        return {
            "surface": self.surface,
            "lemma": self.lemma,
            "source": self.source,
            "evidence_type": self.evidence_type,
            "meaning": self.meaning,
            "english_meaning": self.english_meaning,
            "pos": self.pos,
            "morphology": self.morphology,
            "passage": self.passage,
            "work": self.work,
            "author": self.author,
            "period": self.period,
            "genre": self.genre,
            "verse": self.verse,
            "line": self.line,
            "relations": self.relations,
            "source_url": self.source_url,
            "source_id": self.source_id,
            "metadata": self.metadata,
        }
