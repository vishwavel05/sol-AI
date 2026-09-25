import os
import sys
import bz2
import sqlite3
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
import re

DUMP_URL = "https://dumps.wikimedia.org/tawiktionary/latest/tawiktionary-latest-pages-articles.xml.bz2"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw" / "tamil_wiktionary"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DUMP_FILE = DATA_RAW / "tawiktionary-latest.xml.bz2"
DB_FILE = DATA_PROCESSED / "wiktionary_index.db"

def download_dump():
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    
    if DUMP_FILE.exists() and DUMP_FILE.stat().st_size > 1000000:
        print(f"Dump already exists at {DUMP_FILE}")
        return
        
    print(f"Downloading Tamil Wiktionary dump from {DUMP_URL}...")
    print("This may take a few minutes...")
    
    req = urllib.request.Request(
        DUMP_URL, 
        headers={'User-Agent': 'SOL_AI_Dictionary_Builder/1.0 (contact@example.com)'}
    )
    
    with urllib.request.urlopen(req) as response, open(DUMP_FILE, 'wb') as out_file:
        while True:
            chunk = response.read(8192)
            if not chunk:
                break
            out_file.write(chunk)
            
    print("Download complete.")

def clean_wikitext(text):
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'\[http[^\s]+ ([^\]]+)\]', r'\1', text)
    text = re.sub(r'\[http[^\]]+\]', '', text)
    text = re.sub(r'\{\{[^\}]+\}\}', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r"'''?", "", text)
    # Fix missing spaces after periods
    text = re.sub(r'\.(?=[a-zA-Z\u0B80-\u0BFF])', '. ', text)
    return text.strip()

def parse_and_build_index():
    if DB_FILE.exists():
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE definitions (
            headword TEXT,
            pos TEXT,
            meaning TEXT
        )
    ''')
    cur.execute('CREATE INDEX idx_headword ON definitions(headword)')
    
    print("Parsing XML and building database...")
    
    context = ET.iterparse(bz2.BZ2File(DUMP_FILE, 'rb'), events=('end',))
    count = 0
    
    for event, elem in context:
        tag = elem.tag
        if '}' in tag:
            tag = tag.split('}', 1)[1]
            
        if tag == 'page':
            title_elem = None
            text_elem = None
            
            for child in elem:
                child_tag = child.tag
                if '}' in child_tag:
                    child_tag = child_tag.split('}', 1)[1]
                    
                if child_tag == 'title':
                    title_elem = child
                elif child_tag == 'revision':
                    for rev_child in child:
                        rc_tag = rev_child.tag
                        if '}' in rc_tag:
                            rc_tag = rc_tag.split('}', 1)[1]
                        if rc_tag == 'text':
                            text_elem = rev_child
                            break
                            
            if title_elem is not None and text_elem is not None:
                title = title_elem.text
                if title and ":" not in title and text_elem.text:
                    text = text_elem.text
                    
                    meanings = []
                    lines = text.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        # Very relaxed meaning extraction for Wiktionary # bullet points
                        if line.startswith('#') and len(line) > 2 and '{{' not in line:
                            meaning = line.lstrip('#*: ').strip()
                            meaning = clean_wikitext(meaning)
                            # avoid extracting purely english translations like `# [[hello]]` if possible
                            # but for now we take anything
                            if meaning and len(meaning) > 2:
                                meanings.append(meaning)
                    
                    if meanings:
                        for meaning in meanings:
                            cur.execute('INSERT INTO definitions VALUES (?, ?, ?)', (title, None, meaning))
                        count += 1
                        
            elem.clear()
            
    conn.commit()
    conn.close()
    print(f"Successfully indexed {count} words from Tamil Wiktionary.")

def build_index():
    download_dump()
    parse_and_build_index()

if __name__ == "__main__":
    build_index()
