import unicodedata
from dataclasses import dataclass, field
from typing import List


@dataclass
class NormalizedQuery:
    """
    Data model representing a query after lightweight normalization.
    Preserves original surface form and consistent Unicode representation.
    """
    raw_query: str
    normalized_query: str
    candidate_lemmas: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "raw_query": self.raw_query,
            "normalized_query": self.normalized_query,
            "candidate_lemmas": self.candidate_lemmas
        }


class QueryNormalizer:
    """
    Lightweight query normalizer for Tamil surface text.
    Preserves original surface form while normalizing Unicode composition (NFC)
    and whitespace variation without applying hardcoded linguistic transformations.
    """

    @staticmethod
    def normalize(query: str) -> NormalizedQuery:
        """
        Normalize a raw input query string.
        
        :param query: Input surface string
        :return: NormalizedQuery instance
        """
        if not query:
            return NormalizedQuery(raw_query="", normalized_query="")

        # 1. Preserve original string before whitespace stripping
        raw_query = query

        # 2. Trim whitespace
        stripped = query.strip()

        # 3. Apply NFC Unicode normalization (canonical decomposition followed by canonical composition)
        nfc_normalized = unicodedata.normalize("NFC", stripped)

        return NormalizedQuery(
            raw_query=raw_query,
            normalized_query=nfc_normalized,
            candidate_lemmas=[]
        )
