import sqlite3

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
for r in conn.execute("SELECT DISTINCT category FROM questions ORDER BY category"):
    print(r['category'])
    