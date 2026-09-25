import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_AKARATHI_DIR = PROJECT_ROOT / "data" / "raw" / "thani_thamizh_akarathi" / "agarathi"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def parse_search_directory(search_dir: Path) -> List[Dict[str, Any]]:
    """
    Recursively parse the markdown files in the search/ directory.
    Each file represents a single headword.
    """
    entries = []
    if not search_dir.exists():
        return entries
        
    for file_path in search_dir.rglob("*"):
        if file_path.is_file():
            headword = file_path.name
            try:
                content = file_path.read_text(encoding="utf-8-sig", errors="replace")
                
                import re
                
                # Replace squashed headings with newlines and clean brackets
                content = re.sub(r'##\s*(பெயர்|வினை|பண்பு|இடை|உரி)', r'\n[\1]\n', content)
                content = content.replace("##", "")
                
                # Extract meaning by ignoring the first header and transliteration
                meaning_lines = []
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line == ".":
                        continue
                    if line.startswith("# இசையினி தமிழ் அகராதி"):
                        continue
                    if line.startswith("[") and line.endswith("]"):
                        continue
                    if line.startswith(". "):
                        line = line[2:]
                        
                    # Rule: Ignore cross-reference lines
                    if line.startswith("பார்."):
                        continue
                        
                    # Rule: Strip parenthetical citations like (பிங்.), (சூடா.)
                    line = re.sub(r'\([^)]+\)', '', line).strip()
                    if not line:
                        continue
                    
                    # Rule 1: Strip abbreviation lines like "யா."
                    if re.match(r'^[^a-zA-Z0-9\s]{1,4}\.$', line):
                        continue
                        
                    meaning_lines.append(line)
                    
                # Rule 2: Collapse fragmented lists
                collapsed_meaning = ""
                for i, line in enumerate(meaning_lines):
                    collapsed_meaning += line
                    if i < len(meaning_lines) - 1:
                        if line.endswith((".", ";", ")")):
                            collapsed_meaning += "\n"
                        else:
                            collapsed_meaning += ", "
                            
                meaning = collapsed_meaning.strip()
                
                if meaning:
                    entries.append({
                        "headword": headword,
                        "meaning": meaning,
                        "source_file": f"search/{file_path.parent.name}/{headword}",
                        "source_name": "Isaiyini Tamil Dictionary",
                        "entry_format": "MARKDOWN",
                        "raw_entry": content
                    })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
    return entries


def parse_pav_words(pav_file: Path) -> List[Dict[str, Any]]:
    """
    Parse plain_text_dicts/Pav_Words.txt.
    Format:
    HEADWORD
    ==
    MEANING(S)
    """
    entries = []
    if not pav_file.exists():
        return entries

    content = pav_file.read_text(encoding="utf-8", errors="replace")
    blocks = content.split("==")

    for i in range(len(blocks) - 1):
        lines_before = [l.strip() for l in blocks[i].splitlines() if l.strip()]
        lines_after = [l.strip() for l in blocks[i + 1].splitlines() if l.strip()]

        if lines_before and lines_after:
            headword = lines_before[-1]
            meaning = lines_after[0]

            if not headword.startswith("///"):
                raw_block = f"{headword}\n==\n{meaning}"
                entries.append({
                    "headword": headword,
                    "meaning": meaning,
                    "source_file": "plain_text_dicts/Pav_Words.txt",
                    "source_name": "Devaneya Pavanar Pure Tamil Dictionary",
                    "entry_format": "WORD\\n==\\nMEANING",
                    "raw_entry": raw_block
                })

    return entries


def parse_neelambigai_dict(neela_file: Path) -> List[Dict[str, Any]]:
    """
    Parse plain_text_dicts/Sanskrit to Tamil - Dictionary by Neelambigai Ammaiyar.txt.
    Format:
    HEADWORD(S) - MEANING(S)
    """
    entries = []
    if not neela_file.exists():
        return entries

    content = neela_file.read_text(encoding="utf-8", errors="replace")

    for line_idx, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "-" in line:
            parts = line.split("-", 1)
            headwords_raw = parts[0].strip()
            meaning = parts[1].strip()

            if not headwords_raw or not meaning:
                continue

            # Split comma-separated headwords if multiple exist
            headwords = [hw.strip() for hw in headwords_raw.split(",") if hw.strip()]
            for hw in headwords:
                entries.append({
                    "headword": hw,
                    "meaning": meaning,
                    "source_file": "plain_text_dicts/Sanskrit to Tamil - Dictionary by Neelambigai Ammaiyar.txt",
                    "source_name": "Neelambigai Ammaiyar Sanskrit to Tamil Dictionary",
                    "entry_format": "HEADWORD - MEANING",
                    "raw_entry": line
                })

    return entries


def build_index():
    """Build pre-processed JSON index for Thani Thamizh Akarathi."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    index_file = PROCESSED_DIR / "akarathi_index.json"

    pav_path = RAW_AKARATHI_DIR / "plain_text_dicts" / "Pav_Words.txt"
    neela_path = RAW_AKARATHI_DIR / "plain_text_dicts" / "Sanskrit to Tamil - Dictionary by Neelambigai Ammaiyar.txt"
    search_dir = RAW_AKARATHI_DIR / "search"

    print("Parsing Thani Thamizh Akarathi plain text dictionary files...")

    pav_entries = parse_pav_words(pav_path)
    print(f"  Parsed {len(pav_entries)} entries from Pav_Words.txt")

    neela_entries = parse_neelambigai_dict(neela_path)
    print(f"  Parsed {len(neela_entries)} entries from Neelambigai Ammaiyar dictionary")
    
    search_entries = parse_search_directory(search_dir)
    print(f"  Parsed {len(search_entries)} entries from search directory")

    all_entries = pav_entries + neela_entries + search_entries
    headword_index: Dict[str, List[Dict[str, Any]]] = {}

    for idx, entry in enumerate(all_entries):
        hw = entry["headword"]
        entry_with_id = dict(entry)
        entry_with_id["source_id"] = f"akarathi:{entry['source_file']}:{hw}:{idx}"
        headword_index.setdefault(hw, []).append(entry_with_id)

    index_data = {
        "metadata": {
            "dictionary_name": "Thani Thamizh Akarathi Kalanjiyam",
            "total_indexed_entries": len(all_entries),
            "unique_headwords": len(headword_index),
            "source_files": [
                "plain_text_dicts/Pav_Words.txt",
                "plain_text_dicts/Sanskrit to Tamil - Dictionary by Neelambigai Ammaiyar.txt"
            ]
        },
        "headword_index": headword_index
    }

    index_file.write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSuccessfully built Akarathi index:")
    print(f"  Total Indexed Entries: {len(all_entries)}")
    print(f"  Unique Headwords:      {len(headword_index)}")
    print(f"  Index saved to:        {index_file}")


if __name__ == "__main__":
    build_index()
