import json
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

from backend.schemas.evidence import Evidence
from backend.resources.base import ResourceAdapter


class ThaniThamizhAkarathiAdapter(ResourceAdapter):
    """
    Resource adapter for Thani Thamizh Akarathi (Open Source Tamil Dictionary).
    Provides lexical meanings, Tamil equivalents, and headword definitions.
    """

    def __init__(self, index_path: Optional[Path] = None):
        """
        Initialize the Thani Thamizh Akarathi adapter.
        
        :param index_path: Optional custom path to the pre-processed JSON index.
        """
        if index_path is None:
            project_root = Path(__file__).resolve().parents[2]
            self.index_path = project_root / "data" / "processed" / "akarathi_index.json"
        else:
            self.index_path = Path(index_path)

        self.index_data: Dict[str, List[Dict[str, Any]]] = {}
        self._load_or_build_index()

    def _load_or_build_index(self):
        """Load pre-processed index from JSON, or trigger build if missing."""
        if not self.index_path.exists():
            # Dynamically import and run build_index if index file doesn't exist
            project_root = Path(__file__).resolve().parents[2]
            scripts_dir = project_root / "scripts"
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))
            from build_akarathi_index import build_index
            build_index()

        if self.index_path.exists():
            content = json.loads(self.index_path.read_text(encoding="utf-8"))
            self.index_data = content.get("headword_index", {})

    def lookup(self, query: str) -> List[Evidence]:
        """
        Look up a Tamil headword in Thani Thamizh Akarathi and return normalized Evidence objects.
        Preserves all matching entries across source dictionaries without merging.
        
        :param query: Tamil surface word/string to look up.
        :return: List of Evidence objects representing matching dictionary records.
        """
        query = query.strip()
        if not query:
            return []

        entries = self.index_data.get(query, [])
        if not entries:
            return [
                Evidence(
                    surface=query,
                    lemma=None,
                    source="Thani Thamizh Akarathi",
                    evidence_type="lexical",
                    meaning=None,
                    metadata={
                        "status": "NOT_FOUND",
                        "lookup_method": "exact_headword"
                    }
                )
            ]

        results: List[Evidence] = []
        for entry in entries:
            results.append(
                Evidence(
                    surface=query,
                    lemma=entry.get("headword", query),
                    source="Thani Thamizh Akarathi",
                    evidence_type="lexical",
                    meaning=entry.get("meaning"),
                    source_id=entry.get("source_id"),
                    metadata={
                        "source_file": entry.get("source_file"),
                        "source_name": entry.get("source_name"),
                        "entry_format": entry.get("entry_format"),
                        "raw_entry": entry.get("raw_entry"),
                        "status": "FOUND"
                    }
                )
            )

        return results


def main():
    """CLI test runner for Thani Thamizh Akarathi adapter."""
    if len(sys.argv) < 2:
        print("Usage: python -m backend.resources.akarathi <tamil_word>")
        sys.exit(1)

    word = sys.argv[1]
    adapter = ThaniThamizhAkarathiAdapter()
    evidences = adapter.lookup(word)

    print(f"Query Surface: {word}")
    print(f"Source:        Thani Thamizh Akarathi")
    print(f"Entries Found: {len(evidences)}\n")

    for i, ev in enumerate(evidences, 1):
        if ev.metadata.get("status") == "NOT_FOUND":
            print("Status: NOT_FOUND")
            print(f"No dictionary entry found for '{word}'.")
        else:
            print(f"--- Entry {i} ---")
            print(f"Headword:     {ev.lemma}")
            print(f"Meaning:      {ev.meaning}")
            print(f"Dictionary:   {ev.metadata.get('source_name')}")
            print(f"Source File:  {ev.metadata.get('source_file')}")
            print(f"Source ID:    {ev.source_id}")
            print(f"Raw Entry:\n{ev.metadata.get('raw_entry')}")
            print()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
