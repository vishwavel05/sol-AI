import sys
import sqlite3
from pathlib import Path
from typing import List, Optional

from backend.schemas.evidence import Evidence
from backend.resources.base import ResourceAdapter


class TamilWiktionaryAdapter(ResourceAdapter):
    """
    Resource adapter for Tamil Wiktionary.
    Provides lexical meanings extracted from the offline Wiktionary XML dump.
    """

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            project_root = Path(__file__).resolve().parents[2]
            self.db_path = project_root / "data" / "processed" / "wiktionary_index.db"
        else:
            self.db_path = Path(db_path)

        self._check_or_build_db()

    def _check_or_build_db(self):
        """Verify database existence, or build if missing."""
        if not self.db_path.exists():
            project_root = Path(__file__).resolve().parents[2]
            scripts_dir = project_root / "scripts"
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))
            try:
                from build_wiktionary_index import build_index
                build_index()
            except ImportError:
                print("Warning: build_wiktionary_index not found.")

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def lookup(self, query: str) -> List[Evidence]:
        query = query.strip()
        if not query:
            return []

        if not self.db_path.exists():
            return [
                Evidence(
                    surface=query,
                    lemma=None,
                    source="Tamil Wiktionary",
                    evidence_type="lexical",
                    metadata={
                        "error": f"Database file not found: {self.db_path}",
                        "status": "ERROR"
                    }
                )
            ]

        conn = self._get_connection()
        cur = conn.cursor()

        rows = cur.execute(
            "SELECT * FROM definitions WHERE headword = ?",
            (query,)
        ).fetchall()

        conn.close()

        results: List[Evidence] = []
        for i, row in enumerate(rows):
            results.append(
                Evidence(
                    surface=query,
                    lemma=query,
                    source="Tamil Wiktionary",
                    evidence_type="lexical",
                    meaning=row["meaning"],
                    source_id=f"wiktionary:{query}:{i}",
                    metadata={
                        "status": "FOUND"
                    }
                )
            )

        if not results:
            results.append(
                Evidence(
                    surface=query,
                    lemma=None,
                    source="Tamil Wiktionary",
                    evidence_type="lexical",
                    meaning=None,
                    metadata={
                        "status": "NOT_FOUND"
                    }
                )
            )

        return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m backend.resources.wiktionary <tamil_word>")
        sys.exit(1)

    word = sys.argv[1]
    adapter = TamilWiktionaryAdapter()
    evidences = adapter.lookup(word)

    print(f"Query Surface: {word}")
    print(f"Source:        Tamil Wiktionary")
    print(f"Entries Found: {len([e for e in evidences if e.metadata.get('status') == 'FOUND'])}\n")

    for i, ev in enumerate(evidences, 1):
        if ev.metadata.get("status") == "NOT_FOUND":
            print("Status: NOT_FOUND")
            print(f"No Wiktionary entry found for '{word}'.")
        else:
            print(f"--- Entry {i} ---")
            print(f"Headword:     {ev.lemma}")
            print(f"Meaning:      {ev.meaning}")
            print()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
