from abc import ABC, abstractmethod
from typing import List
from backend.schemas.evidence import Evidence


class ResourceAdapter(ABC):
    """
    Abstract base class for all SOL AI resource adapters.
    Ensures a common lookup interface across dictionaries, morphological tools,
    WordNet, and literary corpora.
    """

    @abstractmethod
    def lookup(self, query: str) -> List[Evidence]:
        """
        Look up a Tamil surface form in the resource and return normalized Evidence objects.
        
        :param query: The Tamil surface word/string to look up.
        :return: List of Evidence objects representing all matching analyses/records.
        """
        raise NotImplementedError
