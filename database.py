# perfume-bot/database.py
# SQLite operations and fuzzy search for originals

import sqlite3
from rapidfuzz import process, fuzz

def get_connection(path="data/perfumes.db"):
    """Return sqlite3.Connection. check_same_thread=False for multithreaded bot environment."""
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_originals(conn):
    """Return all rows from OriginalPerfume."""
    cur = conn.cursor()
    cur.execute("SELECT id, brand, name, price_eur, url FROM OriginalPerfume")
    return cur.fetchall()

def find_best_originals(conn, query, limit=3, score_cutoff=60):
    """
    Fuzzy search for originals by query string.
    Returns a list of dicts: {id, brand, name, score}.
    score_cutoff — minimum acceptable similarity (0-100).
    """
    rows = fetch_all_originals(conn)
    choices = []
    ids = []
    for r in rows:
        brand = r["brand"] or ""
        name = r["name"] or ""
        display = (brand + " " + name).strip()
        if not display:
            continue
        choices.append(display)
        ids.append(r["id"])

    if not choices:
        return []

    # Use token_set_ratio — good for word rearrangements and typos
    raw_matches = process.extract(query, choices, scorer=fuzz.token_set_ratio, limit=limit)
    results = []
    for choice_text, score, idx in raw_matches:
        if score >= score_cutoff:
            r = next((x for x in rows if x["id"] == ids[idx]), None)
            if r:
                results.append({"id": ids[idx], "brand": r["brand"], "name": r["name"], "score": score})
    return results

def get_original_by_id(conn, original_id):
    cur = conn.cursor()
    cur.execute("SELECT id, brand, name, price_eur, url FROM OriginalPerfume WHERE id = ?", (original_id,))
    return cur.fetchone()

def get_copies_by_original_id(conn, original_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, original_id, brand, name, price_eur, url, notes, saved_amount FROM CopyPerfume WHERE original_id = ?",
        (original_id,),
    )
    return cur.fetchall()
