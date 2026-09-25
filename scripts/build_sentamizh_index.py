import os
import re
import json
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "sentamizh" / "data" / "processed"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROCESSED_DIR / "sentamizh_index.db"

# Tamil Unicode block range: U+0B80 to U+0BFF
TAMIL_TOKEN_REGEX = re.compile(r'[\u0B80-\u0BFF]+')

def tokenize_tamil(text: str):
    """
    Conservative Tamil tokenizer.
    Extracts continuous Tamil Unicode character sequences while preserving exact surface forms.
    Strips whitespace and punctuation.
    """
    if not text:
        return []
    tokens = TAMIL_TOKEN_REGEX.findall(text)
    return tokens

def build_index():
    print(f"Indexing Sentamizh Corpus from: {RAW_DIR}")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        print(f"Removing existing index DB at: {DB_PATH}")
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create verses table
    cur.execute("""
    CREATE TABLE verses (
        verse_id TEXT PRIMARY KEY,
        source_text TEXT NOT NULL,
        layer TEXT NOT NULL,
        period TEXT NOT NULL,
        verse_number INTEGER,
        classical_tamil TEXT NOT NULL,
        modern_tamil TEXT,
        english TEXT,
        source_url TEXT,
        difficulty TEXT,
        thinai TEXT,
        turai TEXT,
        akam_or_puram TEXT,
        karu TEXT,
        uri TEXT,
        ullurai TEXT,
        speaker_role TEXT,
        metre TEXT,
        pann TEXT,
        dhvani_layer TEXT,
        rasa_primary TEXT,
        rasa_secondary TEXT,
        themes TEXT,
        philosophical_concept TEXT,
        cultural_context TEXT,
        storytelling_seed_narrative TEXT,
        storytelling_seed_emotional TEXT,
        nayika_bheda TEXT,
        visual_imagery TEXT,
        emotional_valence TEXT,
        annotator TEXT,
        annotation_confidence REAL
    );
    """)

    # Create verse_tokens table
    cur.execute("""
    CREATE TABLE verse_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT NOT NULL,
        normalized_token TEXT NOT NULL,
        verse_id TEXT NOT NULL,
        source_text TEXT NOT NULL,
        FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
    );
    """)

    cur.execute("CREATE INDEX idx_token ON verse_tokens(token);")
    cur.execute("CREATE INDEX idx_norm_token ON verse_tokens(normalized_token);")
    cur.execute("CREATE INDEX idx_verse_id ON verse_tokens(verse_id);")
    cur.execute("CREATE INDEX idx_source_text ON verse_tokens(source_text);")

    json_files = sorted(RAW_DIR.glob("*.json"))
    total_records = 0
    total_tokens = 0

    for json_file in json_files:
        if json_file.name == "corpus_statistics.json":
            continue
        print(f"Processing {json_file.name}...")
        with open(json_file, "r", encoding="utf-8") as f:
            records = json.load(f)

        if not isinstance(records, list):
            continue

        verse_rows = []
        token_rows = []

        for rec in records:
            if not isinstance(rec, dict):
                continue
            verse_id = rec.get("verse_id")
            source_text = rec.get("source_text")
            layer = rec.get("layer")
            period = rec.get("period")
            verse_number = rec.get("verse_number")
            classical_tamil = rec.get("classical_tamil", "")
            modern_tamil = rec.get("modern_tamil")
            english = rec.get("english")
            source_url = rec.get("source_url")
            difficulty = rec.get("difficulty")
            thinai = rec.get("thinai")
            turai = rec.get("turai")
            akam_or_puram = rec.get("akam_or_puram")
            karu = rec.get("karu")
            uri = rec.get("uri")
            ullurai = rec.get("ullurai")
            speaker_role = rec.get("speaker_role")
            metre = rec.get("metre")
            pann = rec.get("pann")
            dhvani_layer = rec.get("dhvani_layer")
            rasa_primary = rec.get("rasa_primary")
            rasa_secondary = rec.get("rasa_secondary")
            themes = rec.get("themes")
            philosophical_concept = rec.get("philosophical_concept")
            cultural_context = rec.get("cultural_context")
            storytelling_seed_narrative = rec.get("storytelling_seed_narrative")
            storytelling_seed_emotional = rec.get("storytelling_seed_emotional")
            nayika_bheda = rec.get("nayika_bheda")
            visual_imagery = rec.get("visual_imagery")
            emotional_valence = rec.get("emotional_valence")
            annotator = rec.get("annotator")
            confidence = rec.get("annotation_confidence")

            verse_rows.append((
                verse_id, source_text, layer, period, verse_number, classical_tamil,
                modern_tamil, english, source_url, difficulty, thinai, turai,
                akam_or_puram, karu, uri, ullurai, speaker_role, metre, pann,
                dhvani_layer, rasa_primary, rasa_secondary, themes, philosophical_concept,
                cultural_context, storytelling_seed_narrative, storytelling_seed_emotional,
                nayika_bheda, visual_imagery, emotional_valence, annotator, confidence
            ))

            tokens = tokenize_tamil(classical_tamil)
            for token in tokens:
                norm_token = token.strip()
                if norm_token:
                    token_rows.append((token, norm_token, verse_id, source_text))

        cur.executemany("""
        INSERT INTO verses VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?
        );
        """, verse_rows)

        cur.executemany("""
        INSERT INTO verse_tokens (token, normalized_token, verse_id, source_text)
        VALUES (?, ?, ?, ?);
        """, token_rows)

        total_records += len(verse_rows)
        total_tokens += len(token_rows)

    conn.commit()

    # Get index size
    db_size_mb = DB_PATH.stat().st_size / (1024 * 1024)
    print(f"\nIndex Build Complete!")
    print(f"Indexed Records: {total_records:,}")
    print(f"Indexed Tokens:  {total_tokens:,}")
    print(f"Database Path:   {DB_PATH}")
    print(f"Database Size:   {db_size_mb:.2f} MB")

    conn.close()

if __name__ == "__main__":
    build_index()
