import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.execute("DELETE FROM questions WHERE category = 'Krishna Leela'")
print(f'Deleted {cur.rowcount} stale rows')
conn.commit()
conn.close()
