import os
import re
import sys
import sqlite3
import tarfile
from pathlib import Path

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_TGZ_PATH = PROJECT_ROOT / "data" / "raw" / "tamil_wordnet" / "TamilWordnet.tgz"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROCESSED_DIR / "wordnet_index.db"


def tamil_transliterate(text: str) -> str:
    """
    Convert Tamil WordNet Romanized transliteration into modern Tamil Unicode.
    Preserves non-transliterable characters safely.
    """
    if not text:
        return text

    vowel_map = {
        'aa': 'ஆ', 'ii': 'ஈ', 'uu': 'ஊ', 'ee': 'ஏ', 'oo': 'ஓ', 'ai': 'ஐ', 'au': 'ஔ',
        'a': 'அ', 'i': 'இ', 'u': 'உ', 'e': 'எ', 'o': 'ஒ'
    }

    consonant_map = {
        'ng': 'ங', 'nj': 'ஞ', 'sh': 'ஷ', 'n2': 'ன',
        'k': 'க', 'c': 'ச', 'T': 'ட', 't': 'த', 'p': 'ப', 'R': 'ற',
        'N': 'ண', 'n': 'ந', 'm': 'ம', 'y': 'ய', 'r': 'ர', 'l': 'ல',
        'v': 'வ', 'z': 'ழ', 'L': 'ள', 's': 'ஸ', 'j': 'ஜ', 'h': 'ஹ'
    }

    vowel_sign_map = {
        'aa': 'ா', 'ii': 'ீ', 'uu': 'ூ', 'ee': 'ே', 'oo': 'ோ', 'ai': 'ை', 'au': 'ௌ',
        'a': '', 'i': 'ி', 'u': 'ு', 'e': 'ெ', 'o': 'ொ'
    }

    tokens = []
    i = 0
    length = len(text)

    while i < length:
        consonant = None
        c_len = 0
        for c_candidate in ['ng', 'nj', 'sh', 'n2', 'k', 'c', 'T', 't', 'p', 'R', 'N', 'n', 'm', 'y', 'r', 'l', 'v', 'z', 'L', 's', 'j', 'h']:
            if text.startswith(c_candidate, i):
                consonant = c_candidate
                c_len = len(c_candidate)
                break

        if consonant:
            vowel = None
            v_len = 0
            rem_idx = i + c_len
            for v_candidate in ['aa', 'ii', 'uu', 'ee', 'oo', 'ai', 'au', 'a', 'i', 'u', 'e', 'o']:
                if text.startswith(v_candidate, rem_idx):
                    vowel = v_candidate
                    v_len = len(v_candidate)
                    break

            if vowel:
                base = consonant_map[consonant]
                sign = vowel_sign_map[vowel]
                tokens.append(base + sign)
                i += c_len + v_len
            else:
                base = consonant_map[consonant]
                tokens.append(base + '்')
                i += c_len
        else:
            vowel = None
            v_len = 0
            for v_candidate in ['aa', 'ii', 'uu', 'ee', 'oo', 'ai', 'au', 'a', 'i', 'u', 'e', 'o']:
                if text.startswith(v_candidate, i):
                    vowel = v_candidate
                    v_len = len(v_candidate)
                    break
            if vowel:
                tokens.append(vowel_map[vowel])
                i += v_len
            else:
                tokens.append(text[i])
                i += 1

    return "".join(tokens)


def parse_sql_values(line: str):
    """Parse SQL INSERT statement value tuple."""
    m = re.search(r"VALUES\s*\((.*)\);?$", line, re.IGNORECASE)
    if not m:
        return []
    raw_vals = m.group(1)

    tokens = []
    in_quote = False
    cur = []

    for char in raw_vals:
        if char == "'" and (not cur or cur[-1] != "\\"):
            in_quote = not in_quote
        elif char == "," and not in_quote:
            tok = "".join(cur).strip()
            if tok.upper() == "NULL":
                tokens.append(None)
            elif tok.startswith("'") and tok.endswith("'"):
                tokens.append(tok[1:-1].replace("\\'", "'"))
            else:
                tokens.append(tok)
            cur = []
            continue
        cur.append(char)

    if cur:
        tok = "".join(cur).strip()
        if tok.upper() == "NULL":
            tokens.append(None)
        elif tok.startswith("'") and tok.endswith("'"):
            tokens.append(tok[1:-1].replace("\\'", "'"))
        else:
            tokens.append(tok)

    return tokens


def build_index():
    """Extract tvudump.sql from TGZ and build SQLite index database."""
    print("Opening TamilWordnet.tgz archive...")
    if not RAW_TGZ_PATH.exists():
        print(f"Error: Archive not found at {RAW_TGZ_PATH}")
        sys.exit(1)

    sql_content = None
    with tarfile.open(RAW_TGZ_PATH, "r:gz") as tar:
        for member in tar.getmembers():
            if member.name.endswith("tvudump.sql"):
                f = tar.extractfile(member)
                if f:
                    sql_content = f.read().decode("utf-8", errors="replace")
                    break

    if not sql_content:
        print("Error: tvudump.sql not found inside archive.")
        sys.exit(1)

    print(f"Extracted tvudump.sql ({len(sql_content)} characters).")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE twn_index (
        nodeindex TEXT PRIMARY KEY,
        unicode_label TEXT,
        raw_label TEXT,
        pos TEXT,
        relation_code TEXT,
        feature_code TEXT,
        indexlength TEXT
    );

    CREATE TABLE sense_index (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unicode_label TEXT,
        raw_label TEXT,
        pos TEXT,
        hypercount INTEGER,
        hypernym TEXT
    );

    CREATE TABLE morphtable_index (
        inflated_unicode TEXT,
        root_unicode TEXT,
        inflated_raw TEXT,
        root_raw TEXT,
        PRIMARY KEY (inflated_unicode, root_unicode)
    );

    CREATE TABLE frequency_index (
        word_unicode TEXT PRIMARY KEY,
        freq INTEGER,
        word_raw TEXT
    );
    """)

    twn_rows = []
    sense_rows = []
    morph_rows = []
    freq_rows = []

    seen_morph = set()

    print("Parsing SQL statements and transliterating records...")

    for line in sql_content.splitlines():
        line_str = line.strip()
        if not line_str.upper().startswith("INSERT INTO"):
            continue

        if line_str.upper().startswith("INSERT INTO TWN") or line_str.upper().startswith("INSERT INTO `TWN`"):
            vals = parse_sql_values(line_str)
            if len(vals) >= 9 and vals[0]:
                nodeindex, raw_label, gloss, example, relation, feature, english, indexlength, pos = vals[:9]
                unicode_label = tamil_transliterate(raw_label) if raw_label else ""
                twn_rows.append((nodeindex, unicode_label, raw_label, pos, relation, feature, indexlength))

        elif line_str.upper().startswith("INSERT INTO SENSE") or line_str.upper().startswith("INSERT INTO `SENSE`"):
            vals = parse_sql_values(line_str)
            if len(vals) >= 4:
                raw_label, pos, hypercount, hypernym = vals[:4]
                unicode_label = tamil_transliterate(raw_label) if raw_label else ""
                try:
                    hc = int(hypercount) if hypercount is not None else 0
                except ValueError:
                    hc = 0
                sense_rows.append((unicode_label, raw_label, pos, hc, hypernym))

        elif line_str.upper().startswith("INSERT INTO MORPHTABLE") or line_str.upper().startswith("INSERT INTO `MORPHTABLE`"):
            vals = parse_sql_values(line_str)
            if len(vals) >= 2 and vals[0]:
                inflated_raw = vals[0]
                root_raw = vals[1] if vals[1] else inflated_raw
                inflated_uni = tamil_transliterate(inflated_raw)
                root_uni = tamil_transliterate(root_raw)

                key = (inflated_uni, root_uni)
                if key not in seen_morph:
                    seen_morph.add(key)
                    morph_rows.append((inflated_uni, root_uni, inflated_raw, root_raw))

        elif line_str.upper().startswith("INSERT INTO FREQUENCY") or line_str.upper().startswith("INSERT INTO `FREQUENCY`"):
            vals = parse_sql_values(line_str)
            if len(vals) >= 2 and vals[0]:
                w_raw = vals[0]
                try:
                    f_val = int(vals[1]) if vals[1] is not None else 0
                except ValueError:
                    f_val = 0
                w_uni = tamil_transliterate(w_raw)
                freq_rows.append((w_uni, f_val, w_raw))

    print(f"Inserting {len(twn_rows)} twn records into SQLite...")
    cur.executemany("INSERT OR REPLACE INTO twn_index VALUES (?,?,?,?,?,?,?)", twn_rows)

    print(f"Inserting {len(sense_rows)} sense records into SQLite...")
    cur.executemany("INSERT INTO sense_index (unicode_label, raw_label, pos, hypercount, hypernym) VALUES (?,?,?,?,?)", sense_rows)

    print(f"Inserting {len(morph_rows)} morphtable records into SQLite...")
    cur.executemany("INSERT OR REPLACE INTO morphtable_index VALUES (?,?,?,?)", morph_rows)

    print(f"Inserting {len(freq_rows)} frequency records into SQLite...")
    cur.executemany("INSERT OR REPLACE INTO frequency_index VALUES (?,?,?)", freq_rows)

    print("Creating database indexes...")
    cur.executescript("""
    CREATE INDEX idx_twn_unicode ON twn_index (unicode_label);
    CREATE INDEX idx_twn_raw ON twn_index (raw_label);
    CREATE INDEX idx_sense_unicode ON sense_index (unicode_label);
    CREATE INDEX idx_morph_inflated ON morphtable_index (inflated_unicode);
    CREATE INDEX idx_freq_word ON frequency_index (word_unicode);
    """)

    conn.commit()
    conn.close()

    print("\nSuccessfully built WordNet SQLite Index:")
    print(f"  twn_index rows:        {len(twn_rows)}")
    print(f"  sense_index rows:      {len(sense_rows)}")
    print(f"  morphtable_index rows: {len(morph_rows)}")
    print(f"  frequency_index rows:  {len(freq_rows)}")
    print(f"  Database file:         {DB_PATH}")


if __name__ == "__main__":
    build_index()
