import sqlite3
import sys

conn = sqlite3.connect('data/raw/thani_thamizh_akarathi/agarathi/ThokKappiyam.db')
tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print('Tables:', tables)

cur = conn.cursor()
if tables:
    cur.execute(f'SELECT * FROM "{tables[0]}" LIMIT 2')
    print('Columns:', [col[0] for col in cur.description])
    print('Data:', cur.fetchall())
