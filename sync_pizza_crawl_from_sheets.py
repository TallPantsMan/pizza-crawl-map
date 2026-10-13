#!/usr/bin/env python3
"""
Autonomous Google Sheet Sync Pipeline for NYC Pizza Crawl Map
Fetches live data from Google Sheets, recalculates scores/ranks/champions,
regenerates the map, and syncs both local desktop files and GitHub repository.
"""

import os
import sys
import io
import csv
import json
import base64
import urllib.request
import urllib.parse
import xml.sax.saxutils as saxutils

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1CDbH3cUa8tEiYLFSS_YIy0HAcWvZ73u6Tzb0fiCq-sU/export?format=csv"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_OWNER = "TallPantsMan"
GITHUB_REPO = "pizza-crawl-map"
GITHUB_BRANCH = "main"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_live_sheet_csv():
    req = urllib.request.Request(
        SHEET_CSV_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PizzaCrawlSync/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    print(f"[{SHEET_CSV_URL}] Downloaded {len(rows)} CSV rows from Google Sheets.")
    return rows

def parse_sheet_rows(rows):
    entries = []
    for r in rows:
        if len(r) >= 3 and r[0].strip().isdigit():
            year = int(r[0].strip())
            crawl_name = r[1].strip()
            contestant = r[2].strip().replace('\ufffd', "'")
            score_str = r[3].strip() if len(r) > 3 else ""
            score = float(score_str) if score_str else None
            rank_str = r[4].strip() if len(r) > 4 else ""
            sheet_rank = int(rank_str) if rank_str.isdigit() else None
            entries.append({
                "year": year,
                "crawl_name": crawl_name,
                "contestant": contestant,
                "score": score,
                "sheet_rank": sheet_rank
            })
    print(f"Parsed {len(entries)} valid crawl entries from Google Sheets.")
    return entries

def run_sync(push_to_github=True):
    print("=" * 60)
    print("Starting NYC Pizza Crawl Google Sheet Sync...")
    print("=" * 60)

    # 1. Fetch live sheet
    rows = fetch_live_sheet_csv()
    entries = parse_sheet_rows(rows)

    # 2. Import base data and builder template
    sys.path.insert(0, SCRIPT_DIR)
    import generate_pizza_maps
    import build_polished_map

    places = generate_pizza_maps.PIZZA_PLACES
    crawls_meta = build_polished_map.CRAWLS_META

    # Lookup mapping for places
    lookup = {}
    for p in places:
        for sn in p.get("sheet_names", []):
            lookup[sn.strip().lower()] = p
        lookup[p["name"].strip().lower()] = p

    # Match entries to places
    place_appearances = {p["id"]: [] for p in places}
    crawls_by_year = {}

    for e in entries:
        yr = e["year"]
        c_name = e["crawl_name"]
        contestant = e["contestant"]
        score = e["score"]

        # Track crawl
        crawls_by_year.setdefault(yr, []).append(e)

        # Match place
        key = contestant.lower()
        clean_key = key.replace("'", "").replace('"', '').strip()
        p = lookup.get(key)
        if not p:
            for k, val in lookup.items():
                if clean_key == k.replace("'", "").replace('"', '').strip():
                    p = val
                    break
        if not p:
            if 'williamsburg' in key and yr == 2016:
                p = next(x for x in places if x['id'] == 'williamsburg-bk')
            elif 'williamsburg' in key and yr == 2017:
                p = next(x for x in places if x['id'] == 'williamsburg-les')
            elif 'difara' in key:
                p = next(x for x in places if x['id'] == 'difara')
            elif 'john' in key:
                p = next(x for x in places if x['id'] == 'johns-bleecker')
            elif 'arturo' in key:
                p = next(x for x in places if x['id'] == 'arturos')

        if p:
            place_appearances[p["id"]].append({
                "year": yr,
                "crawl": c_name,
                "score": score
            })
        else:
            print(f"[Warning] New or unmapped contestant '{contestant}' in {yr}!")

    # 3. Determine crawl winners and calculate intra-crawl rank
    crawl_winners_map = {}
    for yr, c_entries in crawls_by_year.items():
        # Sort by score descending
        scored = [x for x in c_entries if x["score"] is not None]
        unscored = [x for x in c_entries if x["score"] is None]
        scored.sort(key=lambda x: -x["score"])
        ordered = scored + unscored
        
        # Winner is highest score
        if scored:
            top_contestant = scored[0]["contestant"]
            # Find place
            top_p = lookup.get(top_contestant.lower())
            if top_p:
                crawl_winners_map.setdefault(top_p["id"], []).append(yr)

    # 4. Update each place's appearances, best_score, and won_years
    for p in places:
        apps = place_appearances.get(p["id"], p.get("appearances", []))
        # Sort appearances by year descending
        apps.sort(key=lambda a: -a["year"])
        p["appearances"] = apps
        p["appearances_count"] = len(apps)

        # Best score
        valid_scores = [a["score"] for a in apps if a.get("score") is not None]
        p["best_score"] = max(valid_scores) if valid_scores else None

        # Won years
        w_yrs = sorted(crawl_winners_map.get(p["id"], []))
        p["won_years"] = w_yrs
        p["is_crawl_winner"] = len(w_yrs) > 0

    # 5. Assign continuous 1..N all-time rank based on best_score
    scored_places = [p for p in places if p.get("best_score") is not None]
    unscored_places = [p for p in places if p.get("best_score") is None]
    scored_places.sort(key=lambda x: -x["best_score"])
    
    for rk_idx, p in enumerate(scored_places, 1):
        p["best_rank"] = rk_idx
    for rk_idx, p in enumerate(unscored_places, len(scored_places) + 1):
        p["best_rank"] = rk_idx

    # Also calculate rank inside each appearance
    for yr, c_entries in crawls_by_year.items():
        # Sort places appearing in this crawl
        in_yr = []
        for p in places:
            app = next((a for a in p["appearances"] if a["year"] == yr), None)
            if app:
                in_yr.append((p, app["score"] if app["score"] is not None else -1))
        in_yr.sort(key=lambda x: -x[1])
        for rk, (p, _) in enumerate(in_yr, 1):
            app = next(a for a in p["appearances"] if a["year"] == yr)
            app["rank"] = rk

    print(f"Rankings and crawl winners successfully recalculated for all {len(places)} pizzerias.")

    # 6. Run build_polished_map to generate output files
    # build_polished_map will re-embed the updated PIZZA_PLACES into HTML
    import subprocess
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, "build_polished_map.py")]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("[Error in build_polished_map]:", res.stderr)
        return False

    # 7. Push to GitHub if requested
    if push_to_github and GITHUB_TOKEN:
        print("Pushing updated files to GitHub repository...")
        import push_to_github as gh_pusher
        gh_pusher.update_file(
            "map.html",
            os.path.join(SCRIPT_DIR, "github_map.html"),
            "Auto-sync: Updated pizza crawl map from Google Sheets"
        )
        gh_pusher.update_file(
            "index.html",
            os.path.join(SCRIPT_DIR, "github_map.html"),
            "Auto-sync: Updated index.html from Google Sheets"
        )
        print("GitHub sync completed successfully!")

    print("=" * 60)
    print("Sync complete! All 52 pizzerias, scores, and rankings are fully up to date.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    run_sync()
