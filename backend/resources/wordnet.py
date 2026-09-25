import sys
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any

from backend.schemas.evidence import Evidence
from backend.resources.base import ResourceAdapter


class TamilWordNetAdapter(ResourceAdapter):
    """
    Resource adapter for Tamil WordNet (AU-KBC / TVU archive).
    Provides lexical entries, sense index data, morphological root mappings,
    and corpus frequencies.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize the Tamil WordNet adapter.
        
        :param db_path: Optional custom path to the pre-processed SQLite database.
        """
        if db_path is None:
            project_root = Path(__file__).resolve().parents[2]
            self.db_path = project_root / "data" / "processed" / "wordnet_index.db"
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
            from build_wordnet_index import build_index
            build_index()

    def _get_connection(self) -> sqlite3.Connection:
        """Create a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def lookup(self, query: str) -> List[Evidence]:
        """
        Look up a Tamil surface form in Tamil WordNet.
        Returns matching Evidence objects covering lexical entries, morphology roots,
        sense hypernyms, and corpus frequency.
        
        :param query: Tamil surface string to look up.
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
                    source="Tamil WordNet",
                    evidence_type="lexical",
                    metadata={
                        "error": f"Database file not found: {self.db_path}",
                        "status": "ERROR"
                    }
                )
            ]

        conn = self._get_connection()
        cur = conn.cursor()

        # 1. Lexical Lookup (twn_index)
        twn_rows = cur.execute(
            "SELECT * FROM twn_index WHERE unicode_label = ? OR raw_label = ?",
            (query, query)
        ).fetchall()

        # 2. Sense Lookup (sense_index)
        sense_rows = cur.execute(
            "SELECT * FROM sense_index WHERE unicode_label = ? OR raw_label = ?",
            (query, query)
        ).fetchall()

        # 3. Morphology Lookup (morphtable_index)
        morph_rows = cur.execute(
            "SELECT * FROM morphtable_index WHERE inflated_unicode = ? OR inflated_raw = ?",
            (query, query)
        ).fetchall()

        # 4. Frequency Lookup (frequency_index)
        freq_row = cur.execute(
            "SELECT freq, word_raw FROM frequency_index WHERE word_unicode = ? OR word_raw = ?",
            (query, query)
        ).fetchone()

        corpus_freq = freq_row["freq"] if freq_row else None
        freq_raw_word = freq_row["word_raw"] if freq_row else None

        conn.close()

        results: List[Evidence] = []
        seen_keys = set()

        # Process TWN Lexical Entries
        for row in twn_rows:
            nodeindex = row["nodeindex"]
            unicode_label = row["unicode_label"]
            raw_label = row["raw_label"]
            pos = row["pos"]
            rel_code = row["relation_code"]
            feat_code = row["feature_code"]

            # Match corresponding sense info if available
            matching_senses = [s for s in sense_rows if s["pos"] == pos or not pos]
            hypernym = matching_senses[0]["hypernym"] if matching_senses else None
            hypercount = matching_senses[0]["hypercount"] if matching_senses else None

            key = ("twn", nodeindex, unicode_label, pos)
            if key not in seen_keys:
                seen_keys.add(key)
                results.append(
                    Evidence(
                        surface=query,
                        lemma=unicode_label,
                        source="Tamil WordNet",
                        evidence_type="lexical",
                        pos=pos,
                        meaning=None,  # Source dump gloss is 100% NULL
                        source_id=f"wordnet:twn:{nodeindex}",
                        metadata={
                            "nodeindex": nodeindex,
                            "raw_label": raw_label,
                            "relation_code": rel_code,
                            "feature_code": feat_code,
                            "hypernym": hypernym,
                            "hypercount": hypercount,
                            "corpus_frequency": corpus_freq,
                            "transliteration_status": "CONVERTED",
                            "status": "FOUND"
                        }
                    )
                )

        # Process Morphtable Supporting Evidence if present
        for mrow in morph_rows:
            root_uni = mrow["root_unicode"]
            root_raw = mrow["root_raw"]
            inflated_raw = mrow["inflated_raw"]

            key = ("morph", root_uni)
            if key not in seen_keys:
                seen_keys.add(key)
                results.append(
                    Evidence(
                        surface=query,
                        lemma=root_uni,
                        source="Tamil WordNet",
                        evidence_type="morphology",
                        pos=None,
                        meaning=None,
                        source_id=f"wordnet:morphtable:{query}",
                        metadata={
                            "inflated_word": query,
                            "inflated_raw": inflated_raw,
                            "root_word": root_uni,
                            "root_raw": root_raw,
                            "corpus_frequency": corpus_freq,
                            "transliteration_status": "CONVERTED",
                            "status": "FOUND"
                        }
                    )
                )

        # Handle Frequency-only match if no TWN/Morph match found
        if not results and corpus_freq is not None:
            results.append(
                Evidence(
                    surface=query,
                    lemma=query,
                    source="Tamil WordNet",
                    evidence_type="frequency",
                    meaning=None,
                    source_id=f"wordnet:frequency:{query}",
                    metadata={
                        "corpus_frequency": corpus_freq,
                        "raw_word": freq_raw_word,
                        "status": "FOUND"
                    }
                )
            )

        # Return NOT_FOUND if no entries match
        if not results:
            results.append(
                Evidence(
                    surface=query,
                    lemma=None,
                    source="Tamil WordNet",
                    evidence_type="lexical",
                    meaning=None,
                    metadata={
                        "status": "NOT_FOUND"
                    }
                )
            )

        return results


def main():
    """CLI test runner for Tamil WordNet adapter."""
    if len(sys.argv) < 2:
        print("Usage: python -m backend.resources.wordnet <tamil_word>")
        sys.exit(1)

    word = sys.argv[1]
    adapter = TamilWordNetAdapter()
    evidences = adapter.lookup(word)

    print(f"Query Surface: {word}")
    print(f"Source:        Tamil WordNet")
    print(f"Entries Found: {len(evidences)}\n")

    for i, ev in enumerate(evidences, 1):
        if ev.metadata.get("status") == "NOT_FOUND":
            print("Status: NOT_FOUND")
            print(f"No WordNet entry found for '{word}'.")
        else:
            print(f"--- Entry {i} ---")
            print(f"Type:         {ev.evidence_type.upper()}")
            print(f"Lemma/Root:   {ev.lemma}")
            print(f"POS:          {ev.pos}")
            print(f"Source ID:    {ev.source_id}")
            print(f"Frequency:    {ev.metadata.get('corpus_frequency')}")
            print(f"Relation Code:{ev.metadata.get('relation_code')}")
            print(f"Feature Code: {ev.metadata.get('feature_code')}")
            print(f"Raw Label:    {ev.metadata.get('raw_label') or ev.metadata.get('root_raw')}")
            print()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
