# perfume-bot/check.py
# Quick integrity check for the database (tables and counters)

import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "data/perfumes.db")

def table_exists(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", (name,))
    return cur.fetchone() is not None

def main():
    if not os.path.exists(DB_PATH):
        print("DB not found:", DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    for t in ("OriginalPerfume", "CopyPerfume"):
        print(f"{t}: {'OK' if table_exists(conn, t) else 'MISSING'}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM OriginalPerfume")
        print("Originals:", cur.fetchone()[0])
    except Exception as e:
        print("Originals: error", e)
    try:
        cur.execute("SELECT COUNT(*) FROM CopyPerfume")
        print("Copies:", cur.fetchone()[0])
    except Exception as e:
        print("Copies: error", e)

    # Approximate check: copies with empty saved_amount while prices exist
    try:
        cur.execute("""
            SELECT COUNT(*) FROM CopyPerfume c
            JOIN OriginalPerfume o ON c.original_id = o.id
            WHERE c.saved_amount IS NULL AND c.price_eur IS NOT NULL AND o.price_eur IS NOT NULL
        """)
        print("Missing saved_amount but prices present:", cur.fetchone()[0])
    except Exception:
        pass

    conn.close()

if __name__ == "__main__":
    main()
