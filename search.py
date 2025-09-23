# perfume-bot/search.py
# Perfume search logic: flexible search with exact match priority

from rapidfuzz import fuzz                 # for fuzzy search
from utils import normalize_for_match      # text normalization function
from database import fetch_all_originals   # function to get all originals from DB

# Global catalog variables
CATALOG = None
BRAND_MAP = None
NAME_MAP = None

def load_catalog(conn):
    """Load all originals into memory and prepare dictionaries for search"""
    rows = fetch_all_originals(conn)
    catalog, brand_map, name_map = [], {}, {}
    for r in rows:
        item = {
            "id": r["id"],
            "brand": r["brand"] or "",
            "name": r["name"] or "",
            "brand_norm": normalize_for_match(r["brand"]),
            "name_norm": normalize_for_match(r["name"]),
            "display_norm": normalize_for_match(f"{r['brand']} {r['name']}"),
        }
        catalog.append(item)
        brand_map.setdefault(item["brand_norm"], []).append(item)
        name_map.setdefault(item["name_norm"], []).append(item)
    return catalog, brand_map, name_map

def init_catalog(conn):
    """Initialize global catalog variables"""
    global CATALOG, BRAND_MAP, NAME_MAP
    CATALOG, BRAND_MAP, NAME_MAP = load_catalog(conn)

def find_original(conn, user_text):
    global CATALOG, BRAND_MAP, NAME_MAP

    if not user_text or not user_text.strip():
        return {"ok": False, "message": "Empty query. Send in format: 'Brand Name'."}

    if not CATALOG:
        init_catalog(conn)

    user_norm = normalize_for_match(user_text)

    # 1. First, exact match of brand + name (display_norm)
    for c in CATALOG:
        if c["display_norm"] == user_norm:
            return {"ok": True, "original": c}

    # 2. Fuzzy search by display_norm
    best, score = None, 0
    for c in CATALOG:
        s = fuzz.ratio(user_norm, c["display_norm"])
        if s > score:
            best, score = c, s
    if best and score >= 90:  # threshold can be adjusted
        return {"ok": True, "original": best}

    # 3. Fuzzy search only by name
    best, score = None, 0
    for c in CATALOG:
        s = fuzz.ratio(user_norm, c["name_norm"])
        if s > score:
            best, score = c, s
    if best and score >= 90:
        return {"ok": True, "original": best}

    return {"ok": False, "message": "Couldn't find what you were looking for. Please try again. 😅"}
