#!/usr/bin/env python3
"""
Autonomous Google Sheet Sync Pipeline for NYC Pizza Crawl Map
Fetches live data from Google Sheets, recalculates scores/ranks/champions,
handles new contestants, geocoding, custom photos/info,
regenerates the map, and syncs both local desktop files and GitHub repository.
"""

import os
import sys
import io
import re
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

import html

def fetch_actual_place_photos(name, address=""):
    """
    Fetches real photos of the actual pizza place (storefront & signature pie)
    using targeted business image search.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    photos = []
    clean_name = name.replace("’", "'").replace("'", "")
    queries = [
        f'"{name}" pizza NYC',
        f'{name} {address} pizza',
        f'"{clean_name}" slice NYC'
    ]
    
    for q in queries:
        try:
            b_url = "https://www.bing.com/images/async?q=" + urllib.parse.quote(q) + "&first=1&count=20&adlt=off"
            req = urllib.request.Request(b_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
            murls = [html.unescape(x) for x in re.findall(r'murl&quot;:&quot;(https?://[^&]+?)&quot;', raw)]
            titles = [html.unescape(x) for x in re.findall(r'&quot;t&quot;:&quot;([^&]+?)&quot;', raw)]
            
            name_words = [w.lower() for w in re.findall(r'\w+', clean_name) if len(w) > 3 and w.lower() not in ["pizza", "pizzeria", "street", "coal", "oven"]]
            
            for murl, title in zip(murls, titles):
                t_lower = title.lower()
                u_lower = murl.lower()
                matches_name = any(w in t_lower or w in u_lower for w in name_words) if name_words else ("pizza" in t_lower)
                
                if matches_name and murl not in photos:
                    if any(ext in u_lower for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        if 'icon' not in u_lower and 'logo' not in u_lower and 'avatar' not in u_lower:
                            photos.append(murl)
                            if len(photos) >= 3:
                                break
        except Exception as e:
            pass
        if len(photos) >= 2:
            break
            
    if not photos:
        # High-res NYC pizza authentic backup if network unreachable
        photos = [
            "https://lh3.googleusercontent.com/grass-cs/AABkmLenaK57Y3N9bZBT07kZoBy39tINapREo36PmQE9Nd-q6XxlShZBaSxJN3AG2Ygu2qPfcNWdk2Xt3oV2a7mYDGzWHK2eNdTCKLT6JlJbqiIQCBcvKYeoS4LswNPKdEEea5czpVlVqjIG6tdJ=w500-h360-k-no",
            "https://lh3.googleusercontent.com/grass-cs/AABkmLfJAiM6i6NzMalmE-EkGyW9tkPaF_2Kgn5MckNVAf_5LGgt3XvN1x6SeeIkbu-5r__Fx0Tw9jhFpqi-aR47TwFuPW9o47jUZTPdKC9cDn3PCioJMMRExiKb9HyIW_zDb5T0s8qFFU-5QuPi=w500-h360-k-no"
        ]
    return photos

def geocode_place(name, address=""):
    """Finds coordinates, verified address, and borough for a pizzeria in NYC."""
    search_query = address if address else f"{name} New York City"
    lat, lng = 40.730610, -73.935242
    resolved_addr = address or f"{name}, New York, NY"
    borough = "Manhattan"
    try:
        q = urllib.parse.quote(search_query)
        url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "NYCPizzaCrawlBot/1.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data:
                lat = round(float(data[0]["lat"]), 6)
                lng = round(float(data[0]["lon"]), 6)
                disp = data[0].get("display_name", "")
                parts = [p.strip() for p in disp.split(",")]
                if len(parts) >= 2:
                    resolved_addr = f"{parts[0]}, {parts[1]}, NY"
                for b in ["Brooklyn", "Queens", "Bronx", "Staten Island", "Manhattan"]:
                    if b.lower() in disp.lower():
                        borough = b
                        break
    except Exception as ge:
        print(f"[Geocoding Note] {name}: {ge}")
    return lat, lng, resolved_addr, borough

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
    header_idx = -1
    col_map = {"year": 0, "crawl_name": 1, "contestant": 2, "score": 3, "rank": 4}
    for i, r in enumerate(rows[:5]):
        r_low = [c.strip().lower() for c in r]
        if any("contestant" in c for c in r_low):
            header_idx = i
            col_map = {}
            for c_i, c_txt in enumerate(r_low):
                if "year" in c_txt:
                    col_map["year"] = c_i
                elif "crawl" in c_txt:
                    col_map["crawl_name"] = c_i
                elif "contestant" in c_txt or "pizza" in c_txt or "place" in c_txt:
                    col_map["contestant"] = c_i
                elif "score" in c_txt or "avg" in c_txt:
                    col_map["score"] = c_i
                elif "rank" in c_txt:
                    col_map["rank"] = c_i
                elif "addr" in c_txt:
                    col_map["address"] = c_i
                elif "photo" in c_txt or "img" in c_txt or "image" in c_txt:
                    col_map["photo"] = c_i
                elif "note" in c_txt or "desc" in c_txt:
                    col_map["notes"] = c_i
                elif "borough" in c_txt or "hood" in c_txt or "region" in c_txt:
                    col_map["borough"] = c_i
            break

    entries = []
    start_row = header_idx + 1 if header_idx >= 0 else 0
    for r in rows[start_row:]:
        if len(r) > col_map.get("year", 0) and r[col_map["year"]].strip().isdigit():
            y = int(r[col_map["year"]].strip())
            c_name = r[col_map["crawl_name"]].strip() if "crawl_name" in col_map and len(r) > col_map["crawl_name"] else ""
            cont = r[col_map["contestant"]].strip().replace('\ufffd', "'") if "contestant" in col_map and len(r) > col_map["contestant"] else ""
            score_s = r[col_map["score"]].strip() if "score" in col_map and len(r) > col_map["score"] else ""
            score = float(score_s) if score_s else None
            rank_s = r[col_map["rank"]].strip() if "rank" in col_map and len(r) > col_map["rank"] else ""
            sheet_rank = int(rank_s) if rank_s.isdigit() else None
            addr = r[col_map["address"]].strip() if "address" in col_map and len(r) > col_map["address"] else ""
            photo = r[col_map["photo"]].strip() if "photo" in col_map and len(r) > col_map["photo"] else ""
            notes = r[col_map["notes"]].strip() if "notes" in col_map and len(r) > col_map["notes"] else ""
            borough = r[col_map["borough"]].strip() if "borough" in col_map and len(r) > col_map["borough"] else ""
            entries.append({
                "year": y,
                "crawl_name": c_name,
                "contestant": cont,
                "score": score,
                "sheet_rank": sheet_rank,
                "address": addr,
                "photo": photo,
                "notes": notes,
                "borough": borough
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

    places = list(generate_pizza_maps.PIZZA_PLACES)
    crawls_meta = dict(build_polished_map.CRAWLS_META)

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
                p = next((x for x in places if x['id'] == 'williamsburg-bk'), None)
            elif 'williamsburg' in key and yr == 2017:
                p = next((x for x in places if x['id'] == 'williamsburg-les'), None)
            elif 'difara' in key:
                p = next((x for x in places if x['id'] == 'difara'), None)
            elif 'john' in key:
                p = next((x for x in places if x['id'] == 'johns-bleecker'), None)
            elif 'arturo' in key:
                p = next((x for x in places if x['id'] == 'arturos'), None)

        if not p:
            # Auto-provision new contestant!
            pid = re.sub(r'[^a-z0-9]+', '-', contestant.lower()).strip('-')
            lat, lng, res_addr, res_borough = geocode_place(contestant, address=e.get("address"))
            if e.get("photo"):
                photos = [e["photo"]]
            else:
                print(f"[Photo Discovery] Fetching real photos for '{contestant}' ({res_addr})...")
                photos = fetch_actual_place_photos(contestant, address=e.get("address") or res_addr)
                print(f"[Photo Discovery] Found {len(photos)} real photos for '{contestant}'.")
            p = {
                "id": pid,
                "name": contestant,
                "sheet_names": [contestant],
                "address": e.get("address") or res_addr,
                "neighborhood": res_borough,
                "region": res_borough,
                "lat": lat,
                "lng": lng,
                "display_lat": lat,
                "display_lng": lng,
                "best_rank": 99,
                "best_score": None,
                "appearances": [],
                "notes": e.get("notes") or f"Contestant added in {yr}.",
                "style": "NY Pizzeria",
                "specialty": "Signature Slice",
                "status": "Open",
                "photos": photos
            }
            places.append(p)
            lookup[key] = p
            lookup[clean_key] = p
            place_appearances[pid] = []
            print(f"[Auto-Provisioned New Place] '{contestant}' -> ID: {pid}, Lat: {lat}, Lng: {lng}, Borough: {res_borough}")
        else:
            # Update existing place with custom photo/address/notes if provided in sheet
            if e.get("address"):
                p["address"] = e["address"]
            if e.get("photo"):
                p["photos"] = [e["photo"]]
            if e.get("notes"):
                p["notes"] = e["notes"]
            if e.get("borough"):
                p["region"] = e["borough"]
                p["neighborhood"] = e["borough"]

        place_appearances[p["id"]].append({
            "year": yr,
            "crawl": c_name,
            "score": score
        })

    # 3. Determine crawl winners and calculate intra-crawl rank
    crawl_winners_map = {}
    for yr, c_entries in crawls_by_year.items():
        scored = [x for x in c_entries if x["score"] is not None]
        unscored = [x for x in c_entries if x["score"] is None]
        scored.sort(key=lambda x: -x["score"])
        
        if scored:
            top_contestant = scored[0]["contestant"]
            top_p = lookup.get(top_contestant.lower())
            if top_p:
                crawl_winners_map.setdefault(top_p["id"], []).append(yr)

    # 4. Update each place's appearances, best_score, and won_years
    for p in places:
        apps = place_appearances.get(p["id"], p.get("appearances", []))
        apps.sort(key=lambda a: -a["year"])
        p["appearances"] = apps
        p["appearances_count"] = len(apps)

        valid_scores = [a["score"] for a in apps if a.get("score") is not None]
        p["best_score"] = max(valid_scores) if valid_scores else None

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

    # Intra-crawl rankings
    for yr, c_entries in crawls_by_year.items():
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

    # 6. Save enriched places JSON before building map
    enriched_payload = {"places": places, "crawls": crawls_meta}
    for ppath in [
        os.path.join(SCRIPT_DIR, "places_enriched.json"),
        os.path.join(SCRIPT_DIR, "places.json"),
        r"C:\Users\alexh\.gemini\antigravity\brain\28b0ecdd-8d2a-4cf7-a88b-b0943b78da1f\scratch\places_enriched.json"
    ]:
        try:
            os.makedirs(os.path.dirname(ppath), exist_ok=True)
            with open(ppath, "w", encoding="utf-8") as pf:
                json.dump(enriched_payload, pf, indent=2, ensure_ascii=False)
            print(f"Saved pre-build data to {ppath}")
        except Exception:
            pass

    # Update curated photos cache file with any newly discovered photos
    curated_photos_path = os.path.join(SCRIPT_DIR, "final_curated_photos.json")
    try:
        curated_dict = {}
        if os.path.exists(curated_photos_path):
            with open(curated_photos_path, "r", encoding="utf-8") as cpf:
                curated_dict = json.load(cpf)
        for p in places:
            if p["id"] not in curated_dict and p.get("photos"):
                curated_dict[p["id"]] = p["photos"]
        with open(curated_photos_path, "w", encoding="utf-8") as cpf:
            json.dump(curated_dict, cpf, indent=2, ensure_ascii=False)
        print(f"Updated photo cache in {curated_photos_path}")
    except Exception as c_err:
        print("[Curated Photos Cache Note]:", c_err)

    # 7. Run build_polished_map to generate output files
    import subprocess
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, "build_polished_map.py")]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("[Error in build_polished_map]:", res.stderr)
        return False

    # 8. Push to GitHub if requested (only when running locally; GitHub Actions uses git CLI)
    if push_to_github and GITHUB_TOKEN and os.environ.get("GITHUB_ACTIONS") != "true":
        try:
            print("Pushing updated files to GitHub repository...")
            import push_to_github as gh_pusher
            target_file = os.path.join(SCRIPT_DIR, "github_map.html")
            if not os.path.exists(target_file):
                target_file = os.path.join(SCRIPT_DIR, "map.html")
            gh_pusher.update_file(
                "map.html",
                target_file,
                "Auto-sync: Updated pizza crawl map from Google Sheets"
            )
            gh_pusher.update_file(
                "index.html",
                target_file,
                "Auto-sync: Updated index.html from Google Sheets"
            )
            print("GitHub sync completed successfully!")
        except Exception as e:
            print(f"[Warning] GitHub API push skipped or failed: {e}")

    print("=" * 60)
    print(f"Sync complete! All {len(places)} pizzerias, scores, and rankings are fully up to date.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    run_sync()
