import sqlite3

DB_PATH = "data/perfumes.db"  # path to your database

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

brand = "Tom Ford"
cur.execute("SELECT * FROM OriginalPerfume WHERE brand = ?", (brand,))
rows = cur.fetchall()

if rows:
    print(f"The database contains perfumes from brand {brand}:")
    for r in rows:
        print(f"- {r['brand']}: {r['name']}")
else:
    print(f"The database does not contain perfumes from brand {brand}.")

conn.close()
