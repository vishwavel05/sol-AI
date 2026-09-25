import sys
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any

from backend.schemas.evidence import Evidence
from backend.resources.base import ResourceAdapter


class SentamizhAdapter(ResourceAdapter):
    """
    Resource adapter for Sentamizh Literary Corpus.
    Provides structured literary evidence lookup across Sangam poetry, Bhakti hymns,
    and classical epics.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize the Sentamizh adapter.
        
        :param db_path: Optional path to pre-built SQLite index database.
        """
        if db_path is None:
            project_root = Path(__file__).resolve().parents[2]
            self.db_path = project_root / "data" / "processed" / "sentamizh_index.db"
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
            from build_sentamizh_index import build_index
            build_index()

    def _get_connection(self) -> sqlite3.Connection:
        """Create a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def lookup(self, query: str) -> List[Evidence]:
        """
        Look up a Tamil word/phrase in Sentamizh literary corpus.
        Returns matching Evidence objects representing literary verse occurrences.
        
        :param query: Tamil surface token or phrase to look up.
        :return: List of Evidence objects.
        """
        query = query.strip()
        if not query:
            return []

        if not self.db_path.exists():
            return [
                Evidence(
                    surface=query,
                    lemma=None,
                    source="Sentamizh",
                    evidence_type="literary_context",
                    metadata={
                        "error": f"Database file not found: {self.db_path}",
                        "status": "ERROR"
                    }
                )
            ]

        conn = self._get_connection()
        cur = conn.cursor()

        # Query verse_tokens joined with verses table
        sql = """
        SELECT DISTINCT v.*
        FROM verse_tokens vt
        JOIN verses v ON vt.verse_id = v.verse_id
        WHERE vt.token = ? OR vt.normalized_token = ?
        """
        rows = cur.execute(sql, (query, query)).fetchall()
        conn.close()

        if not rows:
            return [
                Evidence(
                    surface=query,
                    lemma=None,
                    source="Sentamizh",
                    evidence_type="literary_context",
                    metadata={
                        "status": "NOT_FOUND"
                    }
                )
            ]

        results: List[Evidence] = []
        for r in rows:
            verse_num_str = str(r["verse_number"]) if r["verse_number"] is not None else None
            
            results.append(
                Evidence(
                    surface=query,
                    lemma=None,  # Conservative lookup preserving surface form
                    source="Sentamizh",
                    evidence_type="literary_context",
                    passage=r["classical_tamil"],
                    work=r["source_text"],
                    author=r["speaker_role"],  # Preserve speaker_role if available
                    period=r["period"],
                    genre=r["layer"],
                    verse=verse_num_str,
                    source_url=r["source_url"],
                    source_id=r["verse_id"],
                    metadata={
                        "verse_id": r["verse_id"],
                        "thinai": r["thinai"],
                        "turai": r["turai"],
                        "akam_or_puram": r["akam_or_puram"],
                        "speaker_role": r["speaker_role"],
                        "pann": r["pann"],
                        "rasa_primary": r["rasa_primary"],
                        "cultural_context": r["cultural_context"],
                        "annotation_confidence": r["annotation_confidence"],
                        "english": r["english"],
                        "status": "FOUND"
                    }
                )
            )

        return results


def main():
    """CLI runner for Sentamizh adapter."""
    if len(sys.argv) < 2:
        print("Usage: python -m backend.resources.sentamizh <tamil_word>")
        sys.exit(1)

    word = sys.argv[1]
    adapter = SentamizhAdapter()
    evidences = adapter.lookup(word)

    print(f"Query Surface: {word}")
    print(f"Source:        Sentamizh Corpus")
    print(f"Verses Found:  {len(evidences)}\n")

    for i, ev in enumerate(evidences[:10], 1):
        if ev.metadata.get("status") == "NOT_FOUND":
            print("Status: NOT_FOUND")
            print(f"No literary occurrences found for '{word}'.")
        else:
            print(f"--- Occurrence {i} ---")
            print(f"Work:       {ev.work}")
            print(f"Verse ID:   {ev.source_id}")
            print(f"Period:     {ev.period}")
            print(f"Layer:      {ev.genre}")
            print(f"Speaker:    {ev.author}")
            print(f"Thinai:     {ev.metadata.get('thinai')}")
            print(f"Turai:      {ev.metadata.get('turai')}")
            print(f"Rasa:       {ev.metadata.get('rasa_primary')}")
            print(f"Passage:    {ev.passage[:100]}..." if ev.passage and len(ev.passage) > 100 else f"Passage:    {ev.passage}")
            print()

    if len(evidences) > 10:
        print(f"... and {len(evidences) - 10} more occurrences.")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
