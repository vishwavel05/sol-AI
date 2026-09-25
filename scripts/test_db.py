import sqlite3
import sys

conn = sqlite3.connect('data/processed/wiktionary_index.db')
cur = conn.cursor()
res = cur.execute("SELECT * FROM definitions WHERE headword LIKE '%வீரம்%' LIMIT 10").fetchall()
for r in res:
    print(r)
