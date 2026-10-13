import json
import os
import xml.sax.saxutils as saxutils

# Base places
from generate_pizza_maps import PIZZA_PLACES

CRAWLS_META = {
    2026: {
        "year": 2026,
        "roman": "XII",
        "name": 'Crawl XII: "The BKLYN/MHTN Throwdown"',
        "short_name": "Crawl XII (2026)",
        "region_focus": "Brooklyn & Manhattan",
        "winner_id": "cellos",
        "winner_name": "Cello's Pizzeria",
        "winner_score": 4.081,
        "avg_score": 3.953,
        "stops": 5,
        "summary": "High-scoring cross-borough clash featuring 3 pizzerias breaking the 4.0+ barrier."
    },
    2025: {
        "year": 2025,
        "roman": "XI",
        "name": 'Crawl XI: "The Brawl By The Mall"',
        "short_name": "Crawl XI (2025)",
        "region_focus": "Westchester County",
        "winner_id": "johnnys",
        "winner_name": "Johnny's Pizzeria",
        "winner_score": 3.950,
        "avg_score": 3.476,
        "stops": 5,
        "summary": "Suburban showdown across Mount Vernon, Eastchester, White Plains, Yonkers & Mamaroneck."
    },
    2024: {
        "year": 2024,
        "roman": "X",
        "name": 'Crawl X: "The Vote for the G.O.A.T."',
        "short_name": "Crawl X: G.O.A.T. (2024)",
        "region_focus": "Manhattan & Brooklyn Champions",
        "winner_id": "mamas-too",
        "winner_name": "Mama's TOO!",
        "winner_score": 4.039,
        "avg_score": 3.763,
        "stops": 5,
        "summary": "10th Anniversary All-Winners Rematch between past champions to crown the G.O.A.T."
    },
    2023: {
        "year": 2023,
        "roman": "IX",
        "name": 'Crawl IX: "Rumble in the Concrete Jungle"',
        "short_name": "Crawl IX (2023)",
        "region_focus": "Manhattan",
        "winner_id": "mamas-too",
        "winner_name": "Mama's TOO!",
        "winner_score": 3.940,
        "avg_score": 3.438,
        "stops": 5,
        "summary": "New-wave Manhattan slice shops & Nolita thin-crust contenders."
    },
    2022: {
        "year": 2022,
        "roman": "VIII",
        "name": 'Crawl VIII: "One Cheesy Island"',
        "short_name": "Crawl VIII (2022)",
        "region_focus": "Staten Island",
        "winner_id": "joe-and-pats",
        "winner_name": "Joe & Pat's Pizzeria",
        "winner_score": 3.960,
        "avg_score": 3.550,
        "stops": 5,
        "summary": "Tour of Staten Island's legendary tavern thin-crust and neighborhood slice institutions."
    },
    2021: {
        "year": 2021,
        "roman": "VII",
        "name": 'Crawl VII: "Saturday Slice Fever"',
        "short_name": "Crawl VII (2021)",
        "region_focus": "Brooklyn",
        "winner_id": "ff-pizza",
        "winner_name": "F&F Pizzeria",
        "winner_score": 4.100,
        "avg_score": 3.736,
        "stops": 5,
        "summary": "Historic Brooklyn crawl where F&F set the all-time Pizza Crawl record (4.100)."
    },
    2020: {
        "year": 2020,
        "roman": "VI",
        "name": 'Crawl VI: "A Little Slice of Haven"',
        "short_name": "Crawl VI (2020)",
        "region_focus": "New Haven, CT",
        "winner_id": "sallys",
        "winner_name": "Sally's Apizza",
        "winner_score": 3.800,
        "avg_score": 3.248,
        "stops": 5,
        "summary": "Road trip to Connecticut's coal-fired Apizza capital (Wooster Square & West Haven)."
    },
    2019: {
        "year": 2019,
        "roman": "V",
        "name": 'Crawl V: "Da Brawl in Da Bronx"',
        "short_name": "Crawl V (2019)",
        "region_focus": "The Bronx",
        "winner_id": "louie-and-ernies",
        "winner_name": "Louie & Ernie's Pizza",
        "winner_score": 3.850,
        "avg_score": 3.182,
        "stops": 5,
        "summary": "Bronx expedition from Pelham Bay to Arthur Avenue and Fordham."
    },
    2018: {
        "year": 2018,
        "roman": "IV",
        "name": 'Crawl IV: "Fire and Slice"',
        "short_name": "Crawl IV (2018)",
        "region_focus": "Manhattan Coal Ovens",
        "winner_id": "arturos",
        "winner_name": "Arturo's Coal Oven Pizza",
        "winner_score": 4.080,
        "avg_score": 3.816,
        "stops": 5,
        "summary": "All-coal-oven Manhattan showdown featuring America's oldest pizzerias."
    },
    2017: {
        "year": 2017,
        "roman": "III",
        "name": 'Crawl III: "Cheese in Heat"',
        "short_name": "Crawl III (2017)",
        "region_focus": "Manhattan",
        "winner_id": "joes-pizza",
        "winner_name": "Joe's Pizza",
        "winner_score": 3.830,
        "avg_score": 3.272,
        "stops": 5,
        "summary": "Classic Manhattan slice & coal-oven battle from Greenwich Village to East Harlem."
    },
    2016: {
        "year": 2016,
        "roman": "II",
        "name": "Crawl II: \"The Scored Debut\"",
        "short_name": "Crawl II (2016)",
        "region_focus": "Brooklyn",
        "winner_id": "williamsburg-bk",
        "winner_name": "Williamsburg Pizza (Brooklyn)",
        "winner_score": 4.000,
        "avg_score": 3.478,
        "stops": 5,
        "summary": "First scored Crawl, spanning Williamsburg, DUMBO, Midwood, and Coney Island."
    },
    2015: {
        "year": 2015,
        "roman": "I",
        "name": 'Crawl I: "The Inaugural Crawl"',
        "short_name": "Crawl I (2015)",
        "region_focus": "Brooklyn Icons",
        "winner_id": "joes-pizza",
        "winner_name": "Inaugural Crawl",
        "winner_score": 3.850,
        "avg_score": 3.500,
        "stops": 5,
        "summary": "Where it all began: 5 iconic Brooklyn institutions (Di Fara, L&B, Totonno's, Roberta's, Grimaldi's)."
    }
}

EXTRA_DETAILS = {
    "ff-pizza": {"style": "Artisanal NY Slice", "specialty": "Clam Pie, Vodka Slice & Brown Butter Sage", "status": "Open"},
    "cellos": {"style": "Classic NY & Crisp Square", "specialty": "Burrata Slice, Vodka Pesto Square & Plain Cheese", "status": "Open"},
    "arturos": {"style": "Coal-Fired Brick Oven", "specialty": "Classic Coal-Oven Margherita & Sweet Italian Sausage", "status": "Open"},
    "mamas-too": {"style": "Artisanal Square & Round", "specialty": "Cacio e Pepe Square, Pepperoni Hot Honey & Angry Nonna", "status": "Open"},
    "chrissys": {"style": "Artisanal Tavern Thin-Crust", "specialty": "Hot Honey Pepperoni & Shallot Vodka Pie", "status": "Open"},
    "lindustrie": {"style": "New-Wave NY Slice", "specialty": "Burrata Slice & Fig Jam Bacon Slice", "status": "Open"},
    "difaras": {"style": "Legendary Brooklyn Pie", "specialty": "Dom DeMarco's Regular & Square Pie with Fresh Snipped Basil", "status": "Open"},
    "williamsburg-bk": {"style": "Artisanal Slice & Grandma", "specialty": "Apple Bacon Grandma & Brooklyn Tartufo", "status": "Open"},
    "johns-bleecker": {"style": "1929 Coal-Fired Brick Oven", "specialty": "Traditional Coal-Fired Margherita & Cup-Char Pepperoni", "status": "Open"},
    "joe-and-pats": {"style": "Staten Island Thin-Crust", "specialty": "Famous Tri-Pie (Vodka, Pesto, Marinara) & Classic Thin Crust", "status": "Open"},
    "johnnys": {"style": "1942 Thin-Crust Bar Pie", "specialty": "Well-Done Thin Crust Cheese & Hot Oil Pie", "status": "Open"},
    "angelos": {"style": "Coal-Fired Brick Oven", "specialty": "Coal-Baked Margherita with Fresh Mozzarella", "status": "Open"},
    "slicehaus": {"style": "Gourmet NY Slice", "specialty": "Truffle Burrata & Hot Honey Soppressata Slice", "status": "Open"},
    "louie-and-ernies": {"style": "1959 Bronx Neighborhood Pie", "specialty": "Famous Sausage Pie & Calzone", "status": "Open"},
    "joes-pizza": {"style": "Quintessential NY Street Slice", "specialty": "Classic Greenwich Village Fresh Mozzarella & Plain Slice", "status": "Open"},
    "sallys": {"style": "1938 New Haven Coal Apizza", "specialty": "Signature Tomato Sauce & Mozzarella Coal-Fired Apizza", "status": "Open"},
    "deninos": {"style": "1937 Tavern Thin-Crust", "specialty": "M.O.R. Pie (Meatball, Onion, Ricotta) & Clam Pie", "status": "Open"},
    "pugsley": {"style": "Bronx College Slice", "specialty": "Crispy Garlic-Rim Plain Slice & Penne Vodka Slice", "status": "Open"},
    "ceres": {"style": "Sourdough Wood/Gas Fired", "specialty": "Naturally Leavened Margherita & Stracciatella", "status": "Open"},
    "ignazios": {"style": "Brooklyn Brick Oven", "specialty": "Old-School Fresh Mozzarella & Basil Pie", "status": "Open"},
    "totonnos": {"style": "1924 Coal-Fired Brick Oven", "specialty": "Historic Coney Island Coal-Fired Margherita", "status": "Open"},
    "upside": {"style": "Sourdough 90s-Style NY Slice", "specialty": "Norma Sicilian & Sourdough Plain Slice", "status": "Open"},
    "zuppardis": {"style": "1934 West Haven Apizza", "specialty": "Fresh Littleneck Clam Apizza & Housemade Sausage", "status": "Open"},
    "luzzos": {"style": "Coal-Oven Neapolitan", "specialty": "Bufala Margherita (Historic 1st Ave Location)", "status": "Closed"},
    "patsys": {"style": "1933 Coal-Oven Slice", "specialty": "Original East Harlem Coal-Oven Thin Slice", "status": "Open"},
    "giove": {"style": "Wood-Fired Artisanal", "specialty": "Thin-Crust Margherita & Prosciutto Arugula", "status": "Open"},
    "nunzios": {"style": "Classic Staten Island Thin Pie", "specialty": "Traditional Staten Island Thin-Crust Cheese", "status": "Closed"},
    "rubirosa": {"style": "Nolita Thin-Crust", "specialty": "Signature Tie-Dye Pizza (Vodka, Tomato, Pesto)", "status": "Open"},
    "lombardis": {"style": "1905 Coal-Oven Landmark", "specialty": "Original Clam Pie & Coal-Fired Margherita", "status": "Open"},
    "marios": {"style": "1919 Arthur Ave Institution", "specialty": "Old-World Neapolitan Brick-Oven Pie", "status": "Open"},
    "polpettina": {"style": "Wood-Fired Artisanal", "specialty": "Meatball Ricotta Pie & Soppressata Hot Honey", "status": "Open"},
    "luigis": {"style": "1973 Classic Brooklyn Slice", "specialty": "Old-School Plain Slice & Fresh Mozzarella Grandma", "status": "Open"},
    "best-pizza": {"style": "Wood-Fired NY Slice", "specialty": "White Slice with Caramelized Onions & Sesame Crust", "status": "Open"},
    "abatinos": {"style": "Westchester Brick Oven", "specialty": "Crispy Thin-Crust Margherita & Sicilian", "status": "Open"},
    "dunwoodie": {"style": "1953 Yonkers Neighborhood Slice", "specialty": "Classic NY Thin-Crust Cheese Pie", "status": "Open"},
    "scarrs": {"style": "Fresh-Milled Grain NY Slice", "specialty": "Hotboi (Beef Pepperoni, Jalapeño, Hot Honey) & Sicilian", "status": "Open"},
    "prince-street": {"style": "SoHo Sicilian Square", "specialty": "Famous Spicy Spring Pepperoni Square", "status": "Open"},
    "motorino": {"style": "Wood-Fired Neapolitan", "specialty": "Brussels Sprout Pancetta & Soppressata Piccante", "status": "Open"},
    "sals": {"style": "Westchester Slice Institution", "specialty": "Iconic Salad Slice & Thick Sicilian Square", "status": "Open"},
    "williamsburg-mhtn": {"style": "Lower East Side Slice", "specialty": "Grandma Square & Classic NY Slice", "status": "Open"},
    "bar-nh": {"style": "New Haven Brick-Oven Apizza", "specialty": "Famous Mashed Potato & Bacon Apizza", "status": "Open"},
    "frank-pepes": {"style": "1925 New Haven Coal Apizza", "specialty": "World-Famous White Clam Coal-Fired Apizza", "status": "Open"},
    "modern-apizza": {"style": "1934 Oil-Fueled Brick Oven", "specialty": "Italian Bomb Apizza & Classic Mozzarella", "status": "Open"},
    "lees-tavern": {"style": "1940 Staten Island Bar Pie", "specialty": "Clam Pie & Crispy Tavern Bar Pie", "status": "Open"},
    "sauce-pizzeria": {"style": "East Village Thin Slice", "specialty": "Herb-Crusted Plain & Vodka Slice", "status": "Open"},
    "sal-and-carmines": {"style": "1959 Upper West Side Slice", "specialty": "Traditional High-Cheese NY Street Slice", "status": "Open"},
    "3-boys-from-italy": {"style": "Bronx Neighborhood Slice", "specialty": "Classic Bronx Cheese Slice & Sicilian", "status": "Open"},
    "julianas": {"style": "Coal-Fired Brick Oven", "specialty": "Patsy Grimaldi's No. 1 Pie & Classic Margherita", "status": "Open"},
    "napolis-best": {"style": "Bronx Neighborhood Slice", "specialty": "Classic Tremont Street Slice (Historic Stop)", "status": "Closed"},
    "lb-spumoni": {"style": "1939 Brooklyn Sicilian", "specialty": "Iconic Upside-Down Sicilian Square & Spumoni Ice Cream", "status": "Open"},
    "robertas": {"style": "Bushwick Wood-Fired", "specialty": "Bee Sting (Soppressata, Chili, Honey) & Margherita", "status": "Open"},
    "grimaldis": {"style": "DUMBO Coal-Fired Brick Oven", "specialty": "Brooklyn Bridge Coal-Fired Traditional Pie", "status": "Open"},
}

DISPLAY_OFFSETS = {
    "ignazios": (0.00035, -0.00035),
    "julianas": (0.00005, 0.00025),
    "grimaldis": (-0.00030, -0.00015),
    "joes-pizza": (0.00022, 0.00025),
    "slicehaus": (-0.00022, -0.00020),
    "johns-bleecker": (0.00018, -0.00025),
    "arturos": (-0.00015, 0.00015),
    "prince-street": (0.00022, 0.00025),
    "rubirosa": (0.00012, -0.00028),
    "lombardis": (-0.00018, 0.00022),
    "ceres": (-0.00025, -0.00020),
    "cellos": (0.00015, -0.00020),
    "sauce": (-0.00015, 0.00020),
    "luzzos": (0.00020, 0.00015),
    "lindustrie": (0.00018, -0.00020),
    "best": (-0.00018, 0.00020),
    "motorino": (-0.00010, -0.00025),
    "pugsley": (0.00018, -0.00020),
    "marios": (-0.00018, 0.00020),
    "sallys": (0.00012, -0.00025),
    "frank-pepes": (-0.00012, 0.00025),
}

curr_dir_photos = os.path.dirname(os.path.abspath(__file__))
curated_photos_path = os.path.join(curr_dir_photos, "final_curated_photos.json")
if not os.path.exists(curated_photos_path):
    curated_photos_path = r"C:\Users\alexh\.gemini\antigravity\brain\28b0ecdd-8d2a-4cf7-a88b-b0943b78da1f\scratch\final_curated_photos.json"

if os.path.exists(curated_photos_path):
    try:
        curated_photos = json.load(open(curated_photos_path, encoding="utf-8"))
    except Exception:
        curated_photos = {}
else:
    curated_photos = {}

curated_photos["arturos"] = [
    "https://lh3.googleusercontent.com/gps-cs-s/ANWiy9RdrrLkpFLvfeiyHGy8_VayyMRdUVJjHVxYR_pUAPKw8lHsHR6SZ_4BjYshHG4ApImz_zo8_Z10GaDrKqoy982AHh7wDkrJgffFYjCcT3gn04ALqotdep3FCo_GfV7nIwcZ9EtSpV3ghuWM=w500-h360-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/ANWiy9T_Zi7F_3XGMSi4cCTTGyDUfv0rjLviBvJigCbAppb66kmGQ9Qf5O7_TF4JTLw9brgXjJrfcXUZxlGmji7hKXsc4ZQy2tP5ci28DubdzUep-wvBqKatU0qP1Vr8INXh005hw4mNMkRn36g=w500-h360-k-no"
]

# Enrich each place object
for p in PIZZA_PLACES:
    pid = p["id"]
    ext = EXTRA_DETAILS.get(pid, {})
    p["style"] = ext.get("style", "NY Pizzeria")
    p["specialty"] = ext.get("specialty", "Classic Cheese Pie")
    p["status"] = ext.get("status", "Open")
    dlat, dlng = DISPLAY_OFFSETS.get(pid, (0.0, 0.0))
    p["display_lat"] = round(p["lat"] + dlat, 6)
    p["display_lng"] = round(p["lng"] + dlng, 6)
    p["photos"] = curated_photos.get(pid, [
        "https://lh3.googleusercontent.com/gps-cs-s/ANWiy9QCwj8XAzg4-c_FOAlFxrWUtgHaPpTy1fNoIVKeLZ4opMpJG8aAl5OnQZJc2P-zzPBVAKM8HgRQm5w3azfZaETpQ90Lhz1LuXlF8GbrJItsOmUzO2_uVwNHkXQh6Kz_d2pdUhFk=w500-h360-k-no",
        "https://lh3.googleusercontent.com/gps-cs-s/ANWiy9Sx-xcEAIHYV1Juk-D4a4lL5lCF6GQZ4qCol1qYYJSIDXYXsAqVcwxliAtr-QtmFXvRHnn_IZyPq29hX8nIOS4ZQ40ahB0WXGq8WXYu51VaKJqIawcEM_9v-sD_o7Z2o5noKGF1=w500-h360-k-no"
    ])
    p["appearances_count"] = len(p["appearances"])

# Map crawl winners accurately from CRAWLS_META
crawl_winners_map = {}
for yr, meta in CRAWLS_META.items():
    wid = meta.get("winner_id")
    if wid:
        crawl_winners_map.setdefault(wid, []).append(yr)

for p in PIZZA_PLACES:
    w_yrs = sorted(crawl_winners_map.get(p["id"], []))
    p["won_years"] = w_yrs
    p["is_crawl_winner"] = len(w_yrs) > 0

# Assign continuous 1..52 overall ranking based on best_score
scored_places = [p for p in PIZZA_PLACES if p.get("best_score") is not None]
unscored_places = [p for p in PIZZA_PLACES if p.get("best_score") is None]
scored_places.sort(key=lambda x: -x["best_score"])
for rk_idx, p in enumerate(scored_places, 1):
    p["best_rank"] = rk_idx
for rk_idx, p in enumerate(unscored_places, len(scored_places) + 1):
    p["best_rank"] = rk_idx

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>🍕 NYC Pizza Crawl Map & Guide (2015–2026)</title>
  <meta name="description" content="Official interactive guide and leaderboard of all 52 pizzerias across 12 annual Pizza Crawls (2015–2026) in NYC, Westchester & New Haven." />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css" />
  <style>
    :root {
      --bg-dark: #090e17;
      --bg-panel: #0d1524;
      --bg-card: #131c2e;
      --bg-card-hover: #19253c;
      --border: rgba(255, 255, 255, 0.08);
      --border-focus: #f59e0b;
      --text-main: #ffffff;
      --text-sub: #cbd5e1;
      --text-muted: #94a3b8;
      --amber: #f59e0b;
      --amber-light: #fbbf24;
      --blue: #3b82f6;
      --emerald: #10b981;
      --radius-lg: 16px;
      --radius-md: 12px;
      --radius-sm: 8px;
    }
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    html, body {
      margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden;
      background: var(--bg-dark); color: var(--text-main);
      font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    #app-root {
      display: flex; flex-direction: column; width: 100vw; height: 100vh; height: 100dvh; overflow: hidden;
    }

    /* MINIMAL TOP HEADER: Dynamic, Clean & Spacious */
    .top-header {
      background: #0d1524;
      border-bottom: 1px solid var(--border);
      padding: 10px 18px 8px 18px;
      flex-shrink: 0;
      z-index: 40;
    }
    .header-main-row {
      display: flex; align-items: center; justify-content: space-between; gap: 12px;
    }
    .brand-box {
      display: flex; align-items: center; gap: 10px; cursor: pointer; flex-shrink: 0;
    }
    .logo-badge {
      width: 36px; height: 36px; border-radius: 10px;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.4);
      display: flex; align-items: center; justify-content: center;
      font-size: 19px;
    }
    .brand-title {
      font-size: 17px; font-weight: 700; color: #ffffff; margin: 0;
      letter-spacing: -0.01em; line-height: 1.1;
    }
    .brand-subtitle {
      font-size: 11px; font-weight: 400; color: var(--text-muted); margin: 0;
    }

    /* CENTER SEARCH: Sleek Pill */
    .search-wrap {
      flex: 1; max-width: 340px; position: relative; display: flex; align-items: center;
    }
    .search-icon {
      position: absolute; left: 12px; font-size: 13px; color: var(--text-muted); pointer-events: none;
    }
    .search-input {
      width: 100%; padding: 7px 32px 7px 34px;
      background: #141f33; border: 1px solid var(--border); color: #ffffff;
      font-size: 12.5px; font-weight: 400; border-radius: 999px; outline: none;
      font-family: 'Poppins', sans-serif; transition: all 0.18s ease;
    }
    .search-input::placeholder { color: #64748b; }
    .search-input:focus { border-color: var(--amber); background: #18253d; }
    .search-clear {
      position: absolute; right: 9px; background: #26354d; color: #cbd5e1;
      border: none; border-radius: 999px; width: 18px; height: 18px;
      font-size: 11px; cursor: pointer; display: none; align-items: center; justify-content: center;
    }

    /* HEADER ACTIONS */
    .header-actions {
      display: flex; align-items: center; gap: 8px; flex-shrink: 0;
    }
    .action-btn {
      background: #141f33; border: 1px solid var(--border); color: #cbd5e1;
      border-radius: 999px; padding: 6px 13px; font-size: 12px; font-weight: 600;
      cursor: pointer; display: inline-flex; align-items: center; gap: 5px;
      transition: all 0.15s ease; font-family: 'Poppins', sans-serif; text-decoration: none;
    }
    .action-btn:hover { background: #1c2b45; color: #ffffff; border-color: rgba(255,255,255,0.2); }
    .action-btn-share {
      background: #f59e0b; color: #000000; border-color: #f59e0b; font-weight: 700;
    }
    .action-btn-share:hover { background: #fbbf24; color: #000000; }

    /* FILTERS PILL BAR: Clean & Dynamic */
    .filters-bar {
      display: flex; align-items: center; gap: 6px; margin-top: 8px;
      overflow-x: auto; scrollbar-width: none; padding-bottom: 2px;
    }
    .filters-bar::-webkit-scrollbar { display: none; }
    .filter-chip {
      background: #141f33; border: 1px solid var(--border); color: #cbd5e1;
      font-size: 11.5px; font-weight: 500; padding: 5px 12px; border-radius: 999px;
      cursor: pointer; white-space: nowrap; transition: all 0.15s ease;
      font-family: 'Poppins', sans-serif; display: inline-flex; align-items: center; gap: 4px;
    }
    .filter-chip:hover { color: #ffffff; background: #1c2b45; }
    .filter-chip.active {
      background: rgba(245, 158, 11, 0.2); border-color: var(--amber); color: var(--amber-light);
      font-weight: 600;
    }
    .select-pill {
      background: #141f33; border: 1px solid var(--border); color: #cbd5e1;
      font-size: 11.5px; font-weight: 500; padding: 4.5px 10px; border-radius: 999px;
      outline: none; cursor: pointer; font-family: 'Poppins', sans-serif;
    }
    .select-pill:focus { border-color: var(--amber); }

    @media (max-width: 767px) {
      .top-header { padding: 8px 12px 6px 12px; }
      .brand-title { font-size: 15px; }
      .brand-subtitle { display: none; }
      .search-wrap { max-width: 100%; order: 3; width: 100%; margin-top: 6px; }
      .header-main-row { flex-wrap: wrap; }
      .action-btn { padding: 5px 9px; font-size: 11px; }
    }

    /* MAIN CONTENT SPLIT */
    .main-area {
      display: flex; flex: 1; position: relative; overflow: hidden; width: 100%; height: 100%;
    }
    .sidebar {
      width: 410px; background: var(--bg-panel); border-right: 1px solid var(--border);
      display: flex; flex-direction: column; flex-shrink: 0; height: 100%; z-index: 25;
    }
    @media (max-width: 767px) {
      .sidebar {
        position: absolute; inset: 0; width: 100%; display: none; z-index: 30;
      }
      .sidebar.mobile-open { display: flex; }
    }

    .sidebar-top-bar {
      padding: 8px 16px; display: flex; align-items: center; justify-content: space-between;
      font-size: 11.5px; font-weight: 500; color: var(--text-muted); border-bottom: 1px solid var(--border);
    }
    .places-list {
      flex: 1; overflow-y: auto; padding: 10px 12px 90px 12px;
    }
    .places-list::-webkit-scrollbar { width: 5px; }
    .places-list::-webkit-scrollbar-thumb { background: #26354d; border-radius: 999px; }

    /* DYNAMIC MINIMAL PLACE CARD */
    .place-item {
      margin-bottom: 11px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
    }
    .place-item:hover {
      background: var(--bg-card-hover);
      border-color: rgba(255, 255, 255, 0.16);
      transform: translateY(-1px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    .place-item.expanded {
      border-color: rgba(245, 158, 11, 0.55);
      background: #162136;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* CARD PHOTOS: Clean 2-photo spread */
    .card-photos-grid {
      display: grid; grid-template-columns: 1fr 1fr; gap: 4px;
      height: 112px; background: #070b13; padding: 5px 5px 0 5px;
      position: relative;
    }
    .photo-slot {
      position: relative; height: 100%; border-radius: var(--radius-sm);
      overflow: hidden; background: #111a2a;
    }
    .photo-slot img {
      width: 100%; height: 100%; object-fit: cover; display: block;
      transition: transform 0.3s ease;
    }
    .place-item:hover .photo-slot img { transform: scale(1.03); }

    /* MINIMAL BADGES */
    .rank-badge {
      position: absolute; top: 6px; left: 6px;
      font-size: 11px; font-weight: 700; color: #ffffff;
      background: rgba(9, 14, 23, 0.88);
      border: 1px solid rgba(245, 158, 11, 0.8);
      padding: 2px 7px; border-radius: 6px;
      backdrop-filter: blur(4px);
    }
    .winner-badge {
      position: absolute; top: 6px; right: 6px;
      font-size: 10.5px; font-weight: 700; color: #000000;
      background: #fbbf24; padding: 2px 7px; border-radius: 6px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }

    /* CARD SUMMARY (MINIMAL DEFAULT STATE) */
    .card-summary {
      padding: 9px 13px 10px 13px;
      display: flex; align-items: center; justify-content: space-between; gap: 8px;
    }
    .card-info-left { min-width: 0; flex: 1; }
    .card-title {
      font-size: 15.5px; font-weight: 600; color: #ffffff; margin: 0;
      line-height: 1.25; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .card-sub {
      font-size: 12px; font-weight: 400; color: var(--text-muted); margin: 2px 0 0 0;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .card-info-right {
      display: flex; align-items: center; gap: 7px; flex-shrink: 0;
    }
    .card-score-pill {
      font-size: 12.5px; font-weight: 600; color: #fbbf24;
      background: rgba(245, 158, 11, 0.14); border: 1px solid rgba(245, 158, 11, 0.35);
      padding: 2.5px 7px; border-radius: 6px;
      font-variant-numeric: tabular-nums;
    }
    .expand-chevron {
      font-size: 11px; color: var(--text-muted); transition: transform 0.22s ease;
    }
    .place-item.expanded .expand-chevron {
      transform: rotate(180deg); color: var(--amber);
    }

    /* CARD DRAWER: 1 TAP AWAY EXTRA INFO */
    .card-drawer {
      max-height: 0; overflow: hidden;
      transition: max-height 0.25s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s ease;
      opacity: 0; padding: 0 13px;
      border-top: 1px solid transparent;
    }
    .place-item.expanded .card-drawer {
      max-height: 500px; opacity: 1;
      padding: 9px 13px 12px 13px;
      border-top-color: rgba(255, 255, 255, 0.08);
    }

    .drawer-row {
      display: flex; align-items: baseline; gap: 6px; font-size: 12px; margin-bottom: 5px;
    }
    .drawer-row strong { color: var(--amber-light); font-weight: 600; flex-shrink: 0; }
    .drawer-row span { color: #f1f5f9; font-weight: 400; line-height: 1.35; }
    .drawer-style-tag {
      font-size: 10.5px; font-weight: 600; color: #93c5fd; background: rgba(59, 130, 246, 0.16);
      border: 1px solid rgba(59, 130, 246, 0.3); padding: 1px 6px; border-radius: 4px;
      display: inline-block; margin-bottom: 6px;
    }
    .drawer-quote {
      font-size: 11.5px; font-style: italic; color: #cbd5e1;
      background: rgba(245, 158, 11, 0.08); border-left: 2.5px solid var(--amber);
      padding: 5px 8px; border-radius: 0 5px 5px 0; margin: 7px 0 9px 0;
      line-height: 1.35;
    }
    /* QUICK DIRECTIONS PILL ON COMPACT CARD */
    .card-quick-gmaps {
      background: #1a73e8; color: #ffffff !important;
      border: 1px solid #60a5fa;
      font-size: 11px; font-weight: 700;
      padding: 3px 8px; border-radius: 6px;
      text-decoration: none; display: inline-flex;
      align-items: center; gap: 3px; flex-shrink: 0;
      letter-spacing: 0.01em; box-shadow: 0 2px 6px rgba(26, 115, 232, 0.35);
      transition: all 0.15s ease;
      font-family: 'Poppins', sans-serif;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    .card-quick-gmaps:hover {
      background: #1557b0; border-color: #93c5fd;
      box-shadow: 0 3px 8px rgba(26, 115, 232, 0.55);
      transform: translateY(-1px);
    }

    /* EXPANDED CARD DRAWER ACTIONS (PROMINENT & ULTRA-READABLE) */
    .drawer-actions {
      display: flex; flex-direction: column; gap: 7px; margin-top: 10px;
    }
    .drawer-btn {
      width: 100%; box-sizing: border-box;
      padding: 9.5px 14px; border-radius: 9px;
      display: flex; align-items: center; justify-content: center; gap: 7px;
      text-decoration: none; cursor: pointer; border: 1.5px solid transparent;
      font-family: 'Poppins', sans-serif; transition: all 0.15s ease;
      letter-spacing: 0.01em; line-height: 1.25;
    }
    .drawer-btn-gmaps {
      background: #1a73e8 !important; /* Official Google Maps Blue */
      color: #ffffff !important;
      font-size: 13.5px !important;
      font-weight: 700 !important;
      border-color: #60a5fa !important;
      box-shadow: 0 3px 12px rgba(26, 115, 232, 0.45) !important;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
    }
    .drawer-btn-gmaps:hover {
      background: #1557b0 !important;
      border-color: #93c5fd !important;
      box-shadow: 0 4px 16px rgba(26, 115, 232, 0.65) !important;
    }
    .drawer-btn-share {
      background: #141f33;
      color: #cbd5e1;
      font-size: 11.5px;
      font-weight: 600;
      padding: 6.5px 12px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
    }
    .drawer-btn-share:hover {
      background: #1c2b45;
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.25);
    }

    /* MAP AREA */
    .map-wrap { flex: 1; position: relative; width: 100%; height: 100%; }
    #map { width: 100%; height: 100%; z-index: 10; background: #e5e7eb; }

    /* BASEMAP SWITCHER PILL (TOP-LEFT OF MAP) */
    .map-layer-switcher {
      position: absolute; top: 12px; left: 12px; z-index: 20;
      display: flex; gap: 3px; background: rgba(13, 21, 36, 0.94);
      padding: 3px; border-radius: 999px; border: 1px solid rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(8px); box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
    }
    .layer-pill {
      background: transparent; border: none; color: #cbd5e1;
      font-size: 11px; font-weight: 600; padding: 4.5px 10px;
      border-radius: 999px; cursor: pointer; transition: all 0.15s ease;
      font-family: 'Poppins', sans-serif; display: inline-flex; align-items: center; gap: 4px;
    }
    .layer-pill:hover { color: #ffffff; background: rgba(255, 255, 255, 0.1); }
    .layer-pill.active {
      background: #f59e0b; color: #000000; font-weight: 700;
      box-shadow: 0 2px 6px rgba(245, 158, 11, 0.35);
    }

    /* FLOATING MAP CONTROLS */
    .map-floating-tools {
      position: absolute; bottom: 84px; right: 12px; z-index: 20;
      display: flex; flex-direction: column; gap: 6px;
    }
    .map-tool-btn {
      width: 38px; height: 38px; border-radius: 10px;
      background: rgba(13, 21, 36, 0.94); backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15); color: #ffffff;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer; font-size: 16px; box-shadow: 0 4px 14px rgba(0,0,0,0.35);
      transition: all 0.15s ease;
    }
    .map-tool-btn:hover { background: #1c2b45; color: var(--amber); }

    /* MOBILE TOGGLE */
    .mobile-nav-toggle {
      position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%);
      z-index: 35; display: none;
      background: #0d1524; border: 1.5px solid var(--amber);
      color: #ffffff; padding: 9px 20px; border-radius: 999px;
      font-size: 13px; font-weight: 700; cursor: pointer;
      box-shadow: 0 6px 24px rgba(0,0,0,0.65), 0 0 14px rgba(245, 158, 11, 0.35);
      font-family: 'Poppins', sans-serif; align-items: center; gap: 7px;
    }
    @media (max-width: 767px) {
      .mobile-nav-toggle { display: inline-flex; }
    }

    /* LEAFLET POPUP: Dynamic Minimal Style */
        .leaflet-popup-content-wrapper {
      background: #0d1524 !important; color: #ffffff !important;
      border: 1px solid rgba(255, 255, 255, 0.15) !important;
      border-radius: 14px !important; padding: 0 !important;
      overflow: hidden !important; box-shadow: 0 12px 36px rgba(0,0,0,0.6) !important;
      font-family: 'Poppins', sans-serif !important;
    }
    .leaflet-popup-content {
      margin: 0 !important; width: 290px !important; max-width: 86vw !important; overflow: hidden !important;
    }
    .leaflet-popup-scrolled {
      overflow: hidden !important; border-top: none !important; border-bottom: none !important;
    }
    .leaflet-popup-tip { background: #0d1524 !important; }
    .leaflet-container a.leaflet-popup-close-button {
      top: 6px !important; right: 6px !important;
      color: #fff !important; width: 24px !important; height: 24px !important;
      background: rgba(0,0,0,0.7) !important; border-radius: 999px !important;
      display: flex !important; align-items: center !important; justify-content: center !important;
      font-size: 15px !important; z-index: 10 !important;
    }
    .popup-photos {
      display: grid; grid-template-columns: 1fr 1fr; gap: 3px; height: 105px; background: #000;
      overflow: hidden !important; border-radius: 12px 12px 0 0;
    }
    .popup-photos img {
      width: 100%; height: 105px !important; max-height: 105px !important;
      object-fit: cover !important; display: block;
    }
    .popup-inner { padding: 9px 12px 11px 12px; }
    .popup-head { display: flex; align-items: baseline; justify-content: space-between; gap: 6px; }
    .popup-title { font-size: 15px; font-weight: 700; color: #fff; margin: 0; line-height: 1.25; }
    .popup-score {
      font-size: 12.5px; font-weight: 700; color: #fbbf24;
      background: rgba(245,158,11,0.18); border: 1px solid rgba(245,158,11,0.4);
      padding: 1.5px 6px; border-radius: 5px; flex-shrink: 0;
    }
    .popup-location { font-size: 11.5px; color: var(--text-muted); margin: 2px 0 5px 0; }
    .popup-specialty-line {
      font-size: 11.5px; color: #f1f5f9; background: #141f33;
      padding: 5px 8px; border-radius: 6px; margin-bottom: 7px;
      line-height: 1.35; border-left: 2.5px solid var(--amber);
    }
    .popup-specialty-line strong { color: var(--amber-light); }
    .popup-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; }
    .popup-btn {
      padding: 7px 10px; border-radius: 7px; font-size: 12px; font-weight: 700;
      text-align: center; text-decoration: none; cursor: pointer; display: flex;
      align-items: center; justify-content: center; gap: 4px; font-family: 'Poppins', sans-serif;
      border: 1.5px solid transparent; transition: all 0.15s ease;
    }
    .popup-btn-gmaps {
      background: #1a73e8 !important; color: #ffffff !important;
      border-color: #60a5fa !important;
      font-size: 12px !important; font-weight: 700 !important;
      box-shadow: 0 2px 8px rgba(26, 115, 232, 0.4) !important;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
    }
    .popup-btn-gmaps:hover {
      background: #1557b0 !important; border-color: #93c5fd !important;
    }
    .popup-btn-share {
      background: #1c2b45; color: #cbd5e1; border-color: rgba(255,255,255,0.12);
      font-size: 11.5px; font-weight: 600;
    }
    .popup-btn-share:hover { background: #263652; color: #fff; }

/* TOAST */
    .toast {
      position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%) translateY(40px);
      background: #10b981; color: #000000; font-weight: 700; font-size: 13px;
      padding: 8px 18px; border-radius: 999px; box-shadow: 0 6px 20px rgba(0,0,0,0.5);
      z-index: 1000; opacity: 0; pointer-events: none; transition: all 0.22s ease;
      font-family: 'Poppins', sans-serif;
    }
    .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
  </style>
</head>
<body>
  <div id="app-root">
    <!-- TOP HEADER -->
    <header class="top-header">
      <div class="header-main-row">
        <div class="brand-box" id="brandResetBtn" title="Reset all filters">
          <div class="logo-badge">🍕</div>
          <div>
            <h1 class="brand-title">NYC Pizza Crawl</h1>
            <p class="brand-subtitle">52 Legendary Spots • Crawls I–XII (2015–2026)</p>
          </div>
        </div>

        <div class="search-wrap">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="Search pizzeria, style, neighborhood..." autocomplete="off" />
          <button type="button" id="searchClearBtn" class="search-clear">×</button>
        </div>

        <div class="header-actions">
          <button class="action-btn action-btn-share" id="headerShareBtn" title="Share Pizza Crawl Map">
            <span>🔗</span> <span>Share</span>
          </button>
          <button class="action-btn" id="downloadKmlBtn" title="Download for Google Earth & My Maps">
            <span>🗺️</span> <span>KML</span>
          </button>
        </div>
      </div>

      <!-- SLEEK FILTERS PILL BAR -->
      <div class="filters-bar">
        <button class="filter-chip active" data-chip="ALL">All 52</button>
        <button class="filter-chip" data-chip="WINNERS">🏆 Champions (10)</button>
        <button class="filter-chip" data-chip="ELITE">⭐ 4.0+ Elite (8)</button>
        <button class="filter-chip" data-chip="TOP10">🔥 Top 10</button>

        <select id="crawlFilter" class="select-pill">
          <option value="ALL">All Crawls</option>
          <option value="2026">Crawl XII (2026)</option>
          <option value="2025">Crawl XI (2025)</option>
          <option value="2024">Crawl X (2024)</option>
          <option value="2023">Crawl IX (2023)</option>
          <option value="2022">Crawl VIII (2022)</option>
          <option value="2021">Crawl VII (2021)</option>
          <option value="2020">Crawl VI (2020)</option>
          <option value="2019">Crawl V (2019)</option>
          <option value="2018">Crawl IV (2018)</option>
          <option value="2017">Crawl III (2017)</option>
          <option value="2016">Crawl II (2016)</option>
          <option value="2015">Crawl I (2015)</option>
        </select>

        <select id="regionFilter" class="select-pill">
          <option value="ALL">All Regions (52)</option>
          <option value="Manhattan">Manhattan (18)</option>
          <option value="Brooklyn">Brooklyn (14)</option>
          <option value="Bronx">The Bronx (5)</option>
          <option value="Staten Island">Staten Island (5)</option>
          <option value="Westchester">Westchester (5)</option>
          <option value="New Haven, CT">New Haven, CT (5)</option>
        </select>
      </div>
    </header>

    <!-- MAIN AREA -->
    <div class="main-area">
      <!-- SIDEBAR -->
      <aside class="sidebar" id="sidebar">
        <div class="sidebar-top-bar">
          <span id="placesCount">Showing 52 spots</span>
          <span style="color:#64748b">Tap card for details</span>
        </div>
        <div class="places-list" id="placesList">
          <!-- Populated by JS -->
        </div>
      </aside>

      <!-- GOOGLE MAP AREA -->
      <div class="map-wrap">
        <!-- 1-Tap Basemap Switcher -->
        <div class="map-layer-switcher" id="layerSwitcher">
          <button type="button" class="layer-pill active" data-layer="google" title="Official Google Map">🗺️ Google Map</button>
          <button type="button" class="layer-pill" data-layer="sat" title="Google Satellite Imagery">🛰️ Satellite</button>
          <button type="button" class="layer-pill" data-layer="dark" title="Sleek Dark Mode">🌙 Dark Mode</button>
        </div>

        <div id="map"></div>

        <div class="map-floating-tools">
          <button class="map-tool-btn" id="recenterBtn" title="Recenter NYC">🎯</button>
          <button class="map-tool-btn" id="locateBtn" title="My Location">📍</button>
        </div>

        <!-- Mobile Floating Toggle -->
        <button class="mobile-nav-toggle" id="mobileNavToggle">
          <span id="mobileNavIcon">📋</span>
          <span id="mobileNavLabel">List View (52)</span>
        </button>
      </div>
    </div>
  </div>

  <div class="toast" id="toastNotification">Link copied!</div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
  <script>
    const PLACES = __PLACES_JSON__;
    const CRAWLS_META = __CRAWLS_META_JSON__;

    const REGION_COLORS = {
      'Manhattan': '#f59e0b',
      'Brooklyn': '#10b981',
      'Bronx': '#f43f5e',
      'The Bronx': '#f43f5e',
      'Staten Island': '#8b5cf6',
      'Westchester': '#14b8a6',
      'New Haven, CT': '#f97316',
      'Connecticut': '#f97316',
      'Queens': '#3b82f6'
    };

    function showToast(msg) {
      const toast = document.getElementById('toastNotification');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2000);
    }

    window.__copySpotLink = function(pid, btn) {
      const u = new URL(window.location.href);
      u.searchParams.set('place', pid);
      if (navigator.clipboard) {
        navigator.clipboard.writeText(u.toString()).then(() => showToast('Pizzeria link copied!'));
      } else {
        showToast('Link copied!');
      }
    };

    window.__openSpotDrawer = function(pid) {
      if (window.innerWidth < 768) {
        setMobileView(true);
      }
      handlePlaceSelect(pid, false);
      const card = document.querySelector(`.place-item[data-id="${pid}"]`);
      if (card) {
        card.classList.add('expanded');
        setTimeout(() => card.scrollIntoView({ behavior: 'smooth', block: 'center' }), 120);
      }
    };

    let map = null;
    let baseLayers = {};
    let currentBaseLayer = 'google';
    let markersLayer = null;
    let routeLayer = null;
    let markersById = {};
    let selectedPlaceId = null;
    let activeQuickChip = 'ALL';
    let isMobileListOpen = false;

    const mobileToggleBtn = document.getElementById('mobileNavToggle');
    const mobileNavLabel = document.getElementById('mobileNavLabel');
    const mobileNavIcon = document.getElementById('mobileNavIcon');
    const sidebarEl = document.getElementById('sidebar');

    function setMobileView(showList) {
      isMobileListOpen = showList;
      if (showList) {
        sidebarEl.classList.add('mobile-open');
        mobileNavLabel.textContent = 'Map View';
        mobileNavIcon.textContent = '🗺️';
      } else {
        sidebarEl.classList.remove('mobile-open');
        mobileNavLabel.textContent = 'List View (' + PLACES.length + ')';
        mobileNavIcon.textContent = '📋';
        if (map) setTimeout(() => map.invalidateSize(), 100);
      }
    }

    mobileToggleBtn.addEventListener('click', () => {
      setMobileView(!isMobileListOpen);
    });

    // Marker Icon Generator: Strictly styled, displays crawl rank & overall rank when viewing a crawl
    function createMarkerIcon(p, isSelected, activeRank) {
      const color = REGION_COLORS[p.region] || '#f59e0b';
      const isWinner = (p.won_years && p.won_years.length > 0);
      const isCrawlView = (activeRank !== undefined && activeRank !== null && document.getElementById('crawlFilter')?.value !== 'ALL');

      let rankContent;
      let width, height;

      if (isCrawlView) {
        width = isSelected ? 48 : 42;
        height = isSelected ? 44 : 39;
        rankContent = `
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.15">
            <span style="font-size:${isSelected ? '13px' : '11.5px'};font-weight:800;letter-spacing:-0.2px">#${activeRank}</span>
            <span style="font-size:8.5px;font-weight:600;opacity:0.95;letter-spacing:-0.2px;background:rgba(0,0,0,0.35);padding:0.5px 3px;border-radius:3px;margin-top:1px">All #${p.best_rank}</span>
          </div>
        `;
      } else {
        width = isSelected ? 42 : 36;
        height = isSelected ? 42 : 36;
        const rankText = p.best_rank ? ('#' + p.best_rank) : '★';
        rankContent = `<span>${rankText}</span>`;
      }

      const trophy = isWinner ? '<span style="position:absolute;top:-7px;right:-7px;font-size:13px;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.8));z-index:2">🏆</span>' : '';
      const borderW = isSelected ? '3px solid #ffffff' : '2.5px solid #ffffff';

      const html = `
        <div style="position:relative;width:${width}px;height:${height}px">
          <div style="
            width:100%;height:100%;border-radius:10px;
            background:${color};border:${borderW};
            display:flex;align-items:center;justify-content:center;
            color:#ffffff;font-weight:700;font-size:${isSelected ? '14px' : '12px'};
            box-shadow:0 4px 14px rgba(0,0,0,0.65);
            text-shadow: 0 1px 3px rgba(0,0,0,0.9), 0 0 2px #000;
            font-family:'Poppins',sans-serif;
            transform:${isSelected ? 'scale(1.12)' : 'scale(1)'};
            transition:transform 0.15s ease;
          ">
            ${rankContent}
          </div>
          ${trophy}
        </div>
      `;

      return L.divIcon({
        className: 'custom-pizza-marker',
        html: html,
        iconSize: [width, height],
        iconAnchor: [width / 2, height / 2],
        popupAnchor: [0, -height / 2 - 4]
      });
    }

    function render(skipFitBounds) {
      if (markersLayer) markersLayer.clearLayers();
      if (routeLayer) routeLayer.clearLayers();
      markersById = {};

      const crawlVal = document.getElementById('crawlFilter').value;
      const regionVal = document.getElementById('regionFilter').value;
      const query = document.getElementById('searchInput').value.trim().toLowerCase();

      // Filter places
      const filtered = PLACES.filter(p => {
        if (crawlVal !== 'ALL') {
          const hasCrawl = p.appearances.some(a => a.year == crawlVal);
          if (!hasCrawl) return false;
        }
        if (regionVal !== 'ALL') {
          const matchRegion = (p.region === regionVal) || 
            (regionVal === 'Bronx' && (p.region === 'Bronx' || p.region === 'The Bronx')) ||
            (regionVal === 'New Haven, CT' && (p.region === 'New Haven, CT' || p.region === 'Connecticut'));
          if (!matchRegion) return false;
        }

        if (activeQuickChip === 'WINNERS' && (!p.won_years || p.won_years.length === 0)) return false;
        if (activeQuickChip === 'ELITE' && (!p.best_score || p.best_score < 4.0)) return false;
        if (activeQuickChip === 'TOP10' && (!p.best_rank || p.best_rank > 10)) return false;

        if (query) {
          const textMatch = [
            p.name, p.neighborhood, p.address, p.style, p.specialty, p.notes
          ].join(' ').toLowerCase();
          if (!textMatch.includes(query)) return false;
        }
        return true;
      });

      // Sort places
      filtered.sort((a, b) => {
        if (crawlVal !== 'ALL') {
          const appA = a.appearances.find(x => x.year == crawlVal);
          const appB = b.appearances.find(x => x.year == crawlVal);
          const scA = (appA && appA.score !== null) ? appA.score : -1;
          const scB = (appB && appB.score !== null) ? appB.score : -1;
          if (scB !== scA) return scB - scA;
          return (a.best_rank || 999) - (b.best_rank || 999);
        }
        const rA = a.best_rank || 999;
        const rB = b.best_rank || 999;
        if (rA !== rB) return rA - rB;
        return (b.best_score || 0) - (a.best_score || 0);
      });

      document.getElementById('placesCount').textContent = `Showing ${filtered.length} spots`;

      const listEl = document.getElementById('placesList');
      listEl.innerHTML = '';

      const currentBounds = [];
      const routeCoords = [];
      const markersToAdd = [];

      filtered.forEach(p => {
        const isWinner = (p.won_years && p.won_years.length > 0);
        const isClosed = (p.status === 'Closed');

        let activeApp;
        if (crawlVal !== 'ALL') {
          const app = p.appearances.find(a => a.year == crawlVal) || p.appearances[0];
          const crawlRank = filtered.findIndex(x => x.id === p.id) + 1;
          activeApp = { rank: crawlRank, score: app.score };
        } else {
          activeApp = { rank: p.best_rank, score: p.best_score };
        }

        const photo1 = (p.photos && p.photos[0]) ? p.photos[0] : '';
        const photo2 = (p.photos && p.photos[1]) ? p.photos[1] : photo1;

        const latLng = [p.display_lat || p.lat, p.display_lng || p.lng];
        currentBounds.push(latLng);
        routeCoords.push(latLng);

        // Strict Rank Stacking: Higher rank (#1) is in front, lower rank (#52) in back.
        // Each rank has a dedicated 10,000-unit tier. Leaflet pos.y (at most ~2,000) can never violate rank tiers.
        // Selection adds +1,000 and hover adds +500; both are strictly less than 10,000.
        // Rank 10 selected (901,000) is STILL 89,000 units below Rank 1 (990,000).
        // Rank 10 can NEVER overlay Rank 1 (or any higher rank)!
        const effRank = (crawlVal !== 'ALL' && activeApp.rank) ? activeApp.rank : (p.best_rank || activeApp.rank || 99);
        p._activeRank = effRank;
        const baseRankZ = 1000000 - (effRank * 10000);
        const isSel = (selectedPlaceId === p.id);
        const initialZOffset = isSel ? (baseRankZ + 1000) : baseRankZ;

        // Leaflet Marker & Popup
        if (map && markersLayer) {
          const icon = createMarkerIcon(p, selectedPlaceId === p.id, activeApp.rank);

          const crawlRows = p.appearances.map(a => {
            const scStr = a.score !== null ? a.score.toFixed(3) : 'Inaugural';
            const rkStr = a.rank ? ('#' + a.rank) : 'Participant';
            return `
              <div class="popup-crawl-item">
                <span><strong>${a.crawl || 'Crawl ' + a.year}</strong> (${a.year})</span>
                <span style="color:#fbbf24;font-weight:600">⭐ ${scStr} • ${rkStr}</span>
              </div>
            `;
          }).join('');

          const gmapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(p.name + ' ' + p.address)}`;

          const popupHtml = `
            <div class="popup-box">
              <div class="popup-photos">
                <img src="${photo1}" alt="${p.name}" loading="lazy" referrerpolicy="no-referrer" />
                <img src="${photo2}" alt="${p.name}" loading="lazy" referrerpolicy="no-referrer" />
              </div>
              <div class="popup-inner">
                <div class="popup-head">
                  <h3 class="popup-title">${p.name}</h3>
                  <span class="popup-score">⭐ ${activeApp.score !== null ? activeApp.score.toFixed(3) : '2015'}</span>
                </div>
                ${(crawlVal !== 'ALL') ? `
                  <div style="display:flex;gap:6px;margin:3px 0 6px 0;font-size:11px;">
                    <span style="background:rgba(245,158,11,0.22);color:#fbbf24;font-weight:700;padding:2px 7px;border-radius:4px;border:1px solid rgba(245,158,11,0.4)">Crawl Rank #${activeApp.rank}</span>
                    <span style="background:rgba(59,130,246,0.22);color:#93c5fd;font-weight:700;padding:2px 7px;border-radius:4px;border:1px solid rgba(59,130,246,0.4)">Overall Rank #${p.best_rank}</span>
                  </div>
                ` : ''}
                <div class="popup-location">📍 ${p.address} (${p.neighborhood})</div>
                <div class="popup-specialty-line">🍽️ <strong>Specialty:</strong> ${p.specialty}</div>
                <div class="popup-actions">
                  <a href="${gmapsUrl}" target="_blank" rel="noopener" class="popup-btn popup-btn-gmaps">
                    🧭 Directions ↗
                  </a>
                  <button class="popup-btn popup-btn-share" onclick="window.__openSpotDrawer('${p.id}')">
                    📋 Details &amp; Notes
                  </button>
                </div>
              </div>
            </div>
          `;

          const marker = L.marker(latLng, { icon, zIndexOffset: initialZOffset }).bindPopup(popupHtml, {
            maxWidth: 310,
            autoPan: false,
            offset: [0, -10]
          });

          marker.on('mouseover', () => marker.setZIndexOffset(baseRankZ + 500));
          marker.on('mouseout', () => {
            const isCurSel = (selectedPlaceId === p.id);
            marker.setZIndexOffset(isCurSel ? (baseRankZ + 1000) : baseRankZ);
          });

          marker.on('click', (e) => {
            if (e && e.originalEvent) L.DomEvent.stopPropagation(e);
            handlePlaceSelect(p.id, false);
          });

          markersToAdd.push(marker);
          markersById[p.id] = { marker, place: p, latLng, baseRankZ };
        }

        // DYNAMIC MINIMAL CARD (Default Clean View + 1-Tap Expand Drawer)
        const item = document.createElement('div');
        const isExp = (selectedPlaceId === p.id);
        item.className = 'place-item' + (isExp ? ' expanded' : '');
        item.setAttribute('data-id', p.id);

        const isCrawlMode = (crawlVal !== 'ALL');
        const rankPillText = isCrawlMode ? (`#${activeApp.rank} • All-Time #${p.best_rank}`) : (p.best_rank ? ('#' + p.best_rank) : '★');
        const winnerBadgeHtml = isWinner ? '<span class="winner-badge">🏆 Winner</span>' : '';
        const gmapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(p.name + ' ' + p.address)}`;

        const crawlHistoryInline = p.appearances.map(a => {
          const sc = a.score !== null ? a.score.toFixed(3) : 'Inaugural';
          const rk = a.rank ? ('Rank #' + a.rank) : 'Participant';
          return `<div style="font-size:11.5px;padding:2px 0;display:flex;justify-content:space-between"><span>${a.crawl || 'Crawl ' + a.year} (${a.year})</span><span style="color:#fbbf24;font-weight:600">⭐ ${sc} • ${rk}</span></div>`;
        }).join('');

        item.innerHTML = `
          <div class="card-photos-grid">
            <div class="photo-slot">
              <img src="${photo1}" alt="${p.name} Pizza" loading="lazy" referrerpolicy="no-referrer" />
              <span class="rank-badge">${rankPillText}</span>
            </div>
            <div class="photo-slot">
              <img src="${photo2}" alt="${p.name} Pizza" loading="lazy" referrerpolicy="no-referrer" />
              ${winnerBadgeHtml}
            </div>
          </div>
          <!-- MINIMAL CARD SUMMARY -->
          <div class="card-summary">
            <div class="card-info-left">
              <h4 class="card-title">${p.name}</h4>
              <p class="card-sub">${p.neighborhood} • ${p.region}</p>
              ${isCrawlMode ? `
                <div style="display:flex;align-items:center;gap:6px;margin-top:4px;font-size:11px">
                  <span style="background:rgba(245,158,11,0.2);color:#fbbf24;font-weight:700;padding:2px 6px;border-radius:4px;border:1px solid rgba(245,158,11,0.35)">Crawl Rank #${activeApp.rank}</span>
                  <span style="background:rgba(59,130,246,0.2);color:#93c5fd;font-weight:700;padding:2px 6px;border-radius:4px;border:1px solid rgba(59,130,246,0.35)">Overall Rank #${p.best_rank}</span>
                </div>
              ` : ''}
            </div>
            <div class="card-info-right">
              <div class="card-score-pill">⭐ ${activeApp.score !== null ? activeApp.score.toFixed(3) : '2015'}</div>
              <a href="${gmapsUrl}" target="_blank" rel="noopener" class="card-quick-gmaps" onclick="event.stopPropagation()" title="Get Directions in Google Maps">
                🧭 Directions ↗
              </a>
              <span class="expand-chevron">▾</span>
            </div>
          </div>
          <!-- 1-TAP AWAY DETAILS DRAWER -->
          <div class="card-drawer">
            <div class="drawer-style-tag">${p.style}</div>
            ${isCrawlMode ? `
              <div class="drawer-row" style="background:rgba(15,23,42,0.45);padding:6px 8px;border-radius:6px;border:1px solid rgba(255,255,255,0.08);margin-bottom:8px">
                <div style="display:flex;flex-direction:column;gap:3px;width:100%">
                  <div style="display:flex;justify-content:space-between"><span style="color:#94a3b8">🍕 Rank in this Crawl:</span><strong style="color:#fbbf24">#${activeApp.rank}</strong></div>
                  <div style="display:flex;justify-content:space-between"><span style="color:#94a3b8">🏆 All-Time Overall Rank:</span><strong style="color:#60a5fa">#${p.best_rank} of 52</strong></div>
                </div>
              </div>
            ` : ''}
            <div class="drawer-row">
              <strong>🍽️ Specialty:</strong>
              <span>${p.specialty}</span>
            </div>
            <div class="drawer-row">
              <strong>📍 Address:</strong>
              <span>${p.address}</span>
            </div>
            <div style="font-size:11px;font-weight:700;color:var(--amber-light);margin-top:7px;text-transform:uppercase">
              Crawl History (${p.appearances.length}x)
            </div>
            <div style="margin:3px 0 6px 0">${crawlHistoryInline}</div>
            ${p.notes ? `<div class="drawer-quote">“${p.notes}”</div>` : ''}
            <div class="drawer-actions">
              <a href="${gmapsUrl}" target="_blank" rel="noopener" class="drawer-btn drawer-btn-gmaps" onclick="event.stopPropagation()">
                🧭 Get Directions (Google Maps) ↗
              </a>
              <button class="drawer-btn drawer-btn-share" onclick="event.stopPropagation(); window.__copySpotLink('${p.id}', this)">
                🔗 Share Spot Link
              </button>
            </div>
          </div>
        `;

        item.addEventListener('click', () => {
          handlePlaceSelect(p.id, true);
        });

        listEl.appendChild(item);
      });


      // Add markers in reverse rank order: lowest rank first, highest rank last (topmost in DOM)
      if (map && markersLayer && markersToAdd.length > 0) {
        markersToAdd.slice().reverse().forEach(m => markersLayer.addLayer(m));
      }

      // DOM hierarchy guarantee: Sort marker elements in markerPane so lowest rank is first child,
      // and #1 is the final child (topmost visual and paint stack).
      if (map && map.getPanes && map.getPanes().markerPane) {
        const pane = map.getPanes().markerPane;
        const mList = Object.values(markersById);
        mList.sort((a, b) => {
          const rA = a.place._activeRank || a.place.best_rank || 999;
          const rB = b.place._activeRank || b.place.best_rank || 999;
          return rB - rA; // lowest rank first, #1 last
        });
        mList.forEach(item => {
          if (item.marker && item.marker._icon && item.marker._icon.parentNode === pane) {
            pane.appendChild(item.marker._icon);
          }
        });
      }

      if (map && !skipFitBounds && currentBounds.length > 0) {
        if (crawlVal === 'ALL' && regionVal === 'ALL' && activeQuickChip === 'ALL' && !query) {
          map.setView([40.735, -73.965], 11);
        } else if (activeQuickChip === 'WINNERS' && crawlVal === 'ALL' && regionVal === 'ALL' && !query) {
          // Champions view: NYC Metro centered at zoom 11 so all 9 NYC champions have perfect separation
          map.setView([40.735, -73.965], 11);
        } else if (activeQuickChip === 'TOP10' && crawlVal === 'ALL' && regionVal === 'ALL' && !query) {
          // Top 10 view: Centered across Manhattan/Brooklyn/Staten Island at zoom 11
          map.setView([40.718, -73.985], 11);
        } else {
          map.fitBounds(currentBounds, {
            paddingTopLeft: [40, 40],
            paddingBottomRight: [40, 40],
            maxZoom: 15,
            minZoom: 11
          });
        }
      }
      if (map) setTimeout(() => map.invalidateSize(), 80);
    }

    function handlePlaceSelect(pid, fromCardClick) {
      const isAlreadyExpanded = (selectedPlaceId === pid);
      if (isAlreadyExpanded && fromCardClick) {
        // Toggle collapse
        selectedPlaceId = null;
        document.querySelectorAll('.place-item').forEach(el => el.classList.remove('expanded'));
        if (map) {
          Object.values(markersById).forEach(it => it.marker.setZIndexOffset(it.baseRankZ));
          map.closePopup();
        }
        return;
      }

      selectedPlaceId = pid;

      // Update sidebar accordion
      document.querySelectorAll('.place-item').forEach(el => {
        const isMatch = (el.getAttribute('data-id') === pid);
        el.classList.toggle('expanded', isMatch);
        if (isMatch && !fromCardClick) {
          el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      });

      // Update map markers zIndex & popup
      if (map && markersById[pid]) {
        Object.values(markersById).forEach(it => it.marker.setZIndexOffset(it.baseRankZ));
        const activeMarkerObj = markersById[pid];
        activeMarkerObj.marker.setZIndexOffset(activeMarkerObj.baseRankZ + 1000);

        const isMobile = (window.innerWidth < 768);
        if (isMobile && fromCardClick) {
          setMobileView(false);
          map.invalidateSize();
        }

        // Calculate optical target center:
        // Offsetting latitude northward by ~0.0018deg (~125px at zoom 16) places BOTH the popup and marker pin
        // dead-center in the viewport with generous, balanced margins.
        const latOffset = isMobile ? 0.0016 : 0.0018;
        const targetLat = activeMarkerObj.latLng[0] + latOffset;
        const targetLng = activeMarkerObj.latLng[1];

        // Smooth gliding camera transition without conflicting autoPan jerks
        map.flyTo([targetLat, targetLng], 16, {
          animate: true,
          duration: 0.5,
          easeLinearity: 0.25
        });

        setTimeout(() => {
          activeMarkerObj.marker.openPopup();
        }, 120);
      }
    }

    function initMap() {
      if (map) return;
      map = L.map('map', {
        zoomControl: false,
        attributionControl: false,
        minZoom: 10,
        maxZoom: 19
      }).setView([40.735, -73.965], 11);

      L.control.zoom({ position: 'topright' }).addTo(map);

      // Authentic Google Maps Base Layers
      baseLayers = {
        google: L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
          maxZoom: 20,
          subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
          attribution: '&copy; Google Maps'
        }),
        sat: L.tileLayer('https://{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
          maxZoom: 20,
          subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
          attribution: '&copy; Google Maps'
        }),
        dark: L.layerGroup([
          L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', { maxZoom: 16 }),
          L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', { maxZoom: 16, pane: 'overlayPane' })
        ])
      };

      currentBaseLayer = 'google';
      baseLayers.google.addTo(map);

      function switchBaseLayer(name) {
        if (currentBaseLayer === name) return;
        if (currentBaseLayer === 'dark') {
          baseLayers.dark.remove();
        } else {
          map.removeLayer(baseLayers[currentBaseLayer]);
        }
        currentBaseLayer = name;
        if (name === 'dark') {
          baseLayers.dark.addTo(map);
        } else {
          baseLayers[name].addTo(map);
        }
        document.querySelectorAll('.layer-pill').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-layer') === name);
        });
      }

      document.querySelectorAll('.layer-pill').forEach(btn => {
        btn.addEventListener('click', () => {
          const lyr = btn.getAttribute('data-layer');
          switchBaseLayer(lyr);
        });
      });

      markersLayer = L.layerGroup().addTo(map);
      routeLayer = L.layerGroup().addTo(map);

      // Map background click deselects active cards and resets all marker z-indices
      map.on('click', () => {
        selectedPlaceId = null;
        document.querySelectorAll('.place-item').forEach(el => el.classList.remove('expanded'));
        if (markersById) {
          Object.values(markersById).forEach(it => it.marker.setZIndexOffset(it.baseRankZ));
        }
      });

      render();

      const params = new URLSearchParams(window.location.search);
      if (params.get('place')) {
        const pid = params.get('place');
        if (markersById[pid]) {
          setTimeout(() => handlePlaceSelect(pid, false), 350);
        }
      }
    }

    function bootApp() {
      render();

      document.getElementById('crawlFilter').addEventListener('change', () => render());
      document.getElementById('regionFilter').addEventListener('change', () => render());

      const searchInput = document.getElementById('searchInput');
      const searchClearBtn = document.getElementById('searchClearBtn');

      searchInput.addEventListener('input', () => {
        searchClearBtn.style.display = searchInput.value ? 'flex' : 'none';
        render(true);
      });

      searchClearBtn.addEventListener('click', () => {
        searchInput.value = '';
        searchClearBtn.style.display = 'none';
        render(true);
      });

      document.querySelectorAll('.filter-chip').forEach(ch => {
        ch.addEventListener('click', () => {
          document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
          ch.classList.add('active');
          activeQuickChip = ch.getAttribute('data-chip');
          render();
        });
      });

      document.getElementById('brandResetBtn').addEventListener('click', () => {
        document.getElementById('searchInput').value = '';
        document.getElementById('searchClearBtn').style.display = 'none';
        document.getElementById('crawlFilter').value = 'ALL';
        document.getElementById('regionFilter').value = 'ALL';
        document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
        document.querySelector('.filter-chip[data-chip="ALL"]').classList.add('active');
        activeQuickChip = 'ALL';
        selectedPlaceId = null;
        render();
        if (map) {
          map.closePopup();
          map.flyTo([40.735, -73.965], 11, { animate: true, duration: 0.6 });
        }
      });

      document.getElementById('recenterBtn').addEventListener('click', () => {
        if (!map) return;
        map.closePopup();
        const isFilterActive = (activeQuickChip !== 'ALL' || document.getElementById('crawlFilter').value !== 'ALL' || document.getElementById('regionFilter').value !== 'ALL' || !!document.getElementById('searchInput').value);
        if (isFilterActive && currentBounds && currentBounds.length > 0) {
          map.fitBounds(currentBounds, { padding: [50, 50], maxZoom: 15, animate: true });
        } else {
          map.flyTo([40.735, -73.965], 11, { animate: true, duration: 0.6 });
        }
      });

      document.getElementById('locateBtn').addEventListener('click', () => {
        if (!navigator.geolocation) {
          showToast('Geolocation not supported');
          return;
        }
        navigator.geolocation.getCurrentPosition(pos => {
          const lat = pos.coords.latitude;
          const lng = pos.coords.longitude;
          if (map) {
            L.circleMarker([lat, lng], {
              radius: 8, fillColor: '#3b82f6', color: '#ffffff', weight: 3, opacity: 1, fillOpacity: 0.9
            }).addTo(map).bindPopup('📍 You are here!').openPopup();
            map.setView([lat, lng], 14, { animate: true });
          }
        }, () => showToast('Could not get location'));
      });

      document.getElementById('headerShareBtn').addEventListener('click', () => {
        if (navigator.share) {
          navigator.share({
            title: 'NYC Pizza Crawl Official Map (2015-2026)',
            text: 'Explore all 52 champion & contender pizzerias across 12 annual Pizza Crawls!',
            url: window.location.href
          }).catch(() => {});
        } else if (navigator.clipboard) {
          navigator.clipboard.writeText(window.location.href).then(() => {
            showToast('Share link copied!');
          });
        }
      });

      document.getElementById('downloadKmlBtn').addEventListener('click', () => {
        const kmlParts = [
          '<?xml version="1.0" encoding="UTF-8"?>',
          '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
          '<name>Pizza Crawl Official Map (2015-2026)</name>'
        ];
        PLACES.forEach(p => {
          const rk = p.best_rank ? `#${p.best_rank} ` : '';
          const sc = p.best_score ? ` (${p.best_score.toFixed(3)})` : ' (2015 Crawl)';
          const nm = (rk + p.name + sc).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
          const desc = `${p.address} | ${p.style} | ${p.specialty}`.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
          kmlParts.push(`<Placemark><name>${nm}</name><description>${desc}</description><Point><coordinates>${p.lng},${p.lat},0</coordinates></Point></Placemark>`);
        });
        kmlParts.push('</Document></kml>');
        const blob = new Blob([kmlParts.join('\n')], { type: 'application/vnd.google-earth.kml+xml' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'Pizza_Crawl_Google_My_Maps.kml';
        a.click();
      });

      if (typeof L !== 'undefined') {
        initMap();
      } else {
        const s = document.createElement('script');
        s.src = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js';
        s.onload = () => initMap();
        document.head.appendChild(s);
      }
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', bootApp);
    } else {
      bootApp();
    }
  </script>
</body>
</html>
"""



# Replace embedded data for standalone local file
final_standalone_html = (
    HTML_TEMPLATE
    .replace("__PLACES_JSON__", json.dumps(PIZZA_PLACES, ensure_ascii=False))
    .replace("__CRAWLS_META_JSON__", json.dumps(CRAWLS_META, ensure_ascii=False))
)

curr_dir = os.path.dirname(os.path.abspath(__file__))

targets = [
    r"c:\Users\alexh\Desktop\Pizza_Crawl_Google_Map.html",
    r"C:\Users\alexh\.gemini\antigravity\brain\28b0ecdd-8d2a-4cf7-a88b-b0943b78da1f\pizza_crawl_map.html",
    os.path.join(curr_dir, "map.html"),
    os.path.join(curr_dir, "index.html"),
    os.path.join(curr_dir, "github_map.html"),
]

for t in targets:
    try:
        pdir = os.path.dirname(t)
        if pdir:
            os.makedirs(pdir, exist_ok=True)
        with open(t, "w", encoding="utf-8") as f:
            f.write(final_standalone_html)
        print("Wrote map:", len(final_standalone_html), "bytes to", t)
    except Exception as e:
        pass

# Save enriched places JSON
for ppath in [
    r"C:\Users\alexh\.gemini\antigravity\brain\28b0ecdd-8d2a-4cf7-a88b-b0943b78da1f\scratch\places_enriched.json",
    os.path.join(curr_dir, "places_enriched.json"),
    os.path.join(curr_dir, "places.json")
]:
    try:
        pdir = os.path.dirname(ppath)
        if pdir:
            os.makedirs(pdir, exist_ok=True)
        with open(ppath, "w", encoding="utf-8") as f:
            json.dump({"places": PIZZA_PLACES, "crawls": CRAWLS_META}, f, indent=2, ensure_ascii=False)
        print("Saved JSON to", ppath)
    except Exception as e:
        pass
