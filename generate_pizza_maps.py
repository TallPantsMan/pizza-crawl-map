import csv
import json
import os
import xml.sax.saxutils as saxutils

# All 52 pizza locations covering all 60 entries across Crawls I - XII (2015-2026)
PIZZA_PLACES = [
    {
        "id": "ff-pizza",
        "name": "F&F Pizzeria",
        "sheet_names": ["F&F Pizza"],
        "address": "459 Court St, Brooklyn, NY 11231",
        "neighborhood": "Carroll Gardens",
        "region": "Brooklyn",
        "lat": 40.6776,
        "lng": -73.9974,
        "best_rank": 1,
        "best_score": 4.100,
        "appearances": [
            {"year": 2021, "crawl": 'Crawl VII: "Saturday Slice Fever"', "score": 4.100, "rank": 1},
            {"year": 2024, "crawl": 'Crawl X: "The Vote for the G.O.A.T."', "score": 3.903, "rank": 15},
        ],
        "notes": "All-time #1 highest score (4.100 in 2021)."
    },
    {
        "id": "cellos",
        "name": "Cello's Pizzeria",
        "sheet_names": ["Cellos"],
        "address": "36 St Marks Pl, New York, NY 10003",
        "neighborhood": "East Village",
        "region": "Manhattan",
        "lat": 40.7287,
        "lng": -73.9882,
        "best_rank": 2,
        "best_score": 4.081,
        "appearances": [
            {"year": 2026, "crawl": 'Crawl XII: "The BKLYN/MHTN Throwdown"', "score": 4.081, "rank": 2},
        ],
        "notes": "Winner of Crawl XII (2026) and #2 all-time score."
    },
    {
        "id": "arturos",
        "name": "Arturo's Coal Oven Pizza",
        "sheet_names": ["Arturo’s"],
        "address": "106 W Houston St, New York, NY 10012",
        "neighborhood": "Greenwich Village / SoHo",
        "region": "Manhattan",
        "lat": 40.7274,
        "lng": -74.0005,
        "best_rank": 3,
        "best_score": 4.080,
        "appearances": [
            {"year": 2018, "crawl": 'Crawl IV: "Fire and Slice"', "score": 4.080, "rank": 3},
            {"year": 2024, "crawl": 'Crawl X: "The Vote for the G.O.A.T."', "score": 4.036, "rank": 5},
        ],
        "notes": "Two-time top-5 finisher (2018 winner & 2024 runner-up)."
    },
    {
        "id": "mamas-too",
        "name": "Mama's TOO!",
        "sheet_names": ["Mama's Too!"],
        "address": "2750 Broadway, New York, NY 10025",
        "neighborhood": "Upper West Side",
        "region": "Manhattan",
        "lat": 40.8008,
        "lng": -73.9675,
        "best_rank": 4,
        "best_score": 4.039,
        "appearances": [
            {"year": 2024, "crawl": 'Crawl X: "The Vote for the G.O.A.T."', "score": 4.039, "rank": 4},
            {"year": 2023, "crawl": 'Crawl IX: "Rumble in the Concrete Jungle"', "score": 3.940, "rank": 13},
        ],
        "notes": "Winner of both Crawl IX (2023) and Crawl X G.O.A.T. (2024)."
    },
    {
        "id": "chrissys",
        "name": "Chrissy's Pizza",
        "sheet_names": ["Chrissy's Pizza"],
        "address": "142 Nassau Ave, Brooklyn, NY 11222",
        "neighborhood": "Greenpoint",
        "region": "Brooklyn",
        "lat": 40.7248,
        "lng": -73.9477,
        "best_rank": 6,
        "best_score": 4.035,
        "appearances": [
            {"year": 2026, "crawl": 'Crawl XII: "The BKLYN/MHTN Throwdown"', "score": 4.035, "rank": 6},
        ],
        "notes": "Scored over 4.0 in the 2026 BKLYN/MHTN Throwdown."
    },
    {
        "id": "lindustrie",
        "name": "L'Industrie Pizzeria",
        "sheet_names": ["L'Industrie Pizzeria"],
        "address": "254 S 2nd St, Brooklyn, NY 11211",
        "neighborhood": "Williamsburg",
        "region": "Brooklyn",
        "lat": 40.7116,
        "lng": -73.9577,
        "best_rank": 7,
        "best_score": 4.031,
        "appearances": [
            {"year": 2026, "crawl": 'Crawl XII: "The BKLYN/MHTN Throwdown"', "score": 4.031, "rank": 7},
        ],
        "notes": "Flagship Williamsburg location (also at 104 Christopher St, West Village)."
    },
    {
        "id": "difaras",
        "name": "Di Fara Pizza",
        "sheet_names": ["DiFara's", "Difara's"],
        "address": "1424 Avenue J, Brooklyn, NY 11230",
        "neighborhood": "Midwood",
        "region": "Brooklyn",
        "lat": 40.6250,
        "lng": -73.9615,
        "best_rank": 8,
        "best_score": 4.000,
        "appearances": [
            {"year": 2021, "crawl": 'Crawl VII: "Saturday Slice Fever"', "score": 4.000, "rank": 8},
            {"year": 2016, "crawl": "Crawl II", "score": 3.880, "rank": 16},
            {"year": 2024, "crawl": 'Crawl X: "The Vote for the G.O.A.T."', "score": 3.270, "rank": 43},
            {"year": 2015, "crawl": "The New York Pizza Crawl", "score": None, "rank": None},
        ],
        "notes": "Most appearances in Crawl history (4 times: 2015, 2016, 2021, 2024)."
    },
    {
        "id": "williamsburg-bk",
        "name": "Williamsburg Pizza (Brooklyn)",
        "sheet_names": ["Williamsburg"],
        "address": "265 Union Ave, Brooklyn, NY 11211",
        "neighborhood": "Williamsburg",
        "region": "Brooklyn",
        "lat": 40.7081,
        "lng": -73.9503,
        "best_rank": 9,
        "best_score": 4.000,
        "appearances": [
            {"year": 2016, "crawl": "Crawl II", "score": 4.000, "rank": 9},
        ],
        "notes": "Winner of Crawl II (2016) with a 4.000 score."
    },
    {
        "id": "johns-bleecker",
        "name": "John's of Bleecker St.",
        "sheet_names": ["John’s", "John's Pizza"],
        "address": "278 Bleecker St, New York, NY 10014",
        "neighborhood": "Greenwich Village",
        "region": "Manhattan",
        "lat": 40.7316,
        "lng": -74.0035,
        "best_rank": 10,
        "best_score": 3.970,
        "appearances": [
            {"year": 2018, "crawl": 'Crawl IV: "Fire and Slice"', "score": 3.970, "rank": 10},
            {"year": 2024, "crawl": 'Crawl X: "The Vote for the G.O.A.T."', "score": 3.567, "rank": 31},
        ],
        "notes": "Iconic 1929 Greenwich Village coal-fired brick oven pizzeria."
    },
    {
        "id": "joe-and-pats",
        "name": "Joe & Pat's Pizzeria",
        "sheet_names": ["Joe & Pat's"],
        "address": "1758 Victory Blvd, Staten Island, NY 10314",
        "neighborhood": "Castleton Corners",
        "region": "Staten Island",
        "lat": 40.6130,
        "lng": -74.1223,
        "best_rank": 11,
        "best_score": 3.960,
        "appearances": [
            {"year": 2022, "crawl": 'Crawl VIII: "One Cheesy Island"', "score": 3.960, "rank": 11},
        ],
        "notes": "Winner of Crawl VIII: One Cheesy Island (2022)."
    },
    {
        "id": "johnnys",
        "name": "Johnny's Pizzeria",
        "sheet_names": ["Johnny's"],
        "address": "30 W Lincoln Ave, Mount Vernon, NY 10550",
        "neighborhood": "Mount Vernon",
        "region": "Westchester",
        "lat": 40.9126,
        "lng": -73.8398,
        "best_rank": 12,
        "best_score": 3.950,
        "appearances": [
            {"year": 2025, "crawl": "Crawl XI: The Brawl By The Mall", "score": 3.950, "rank": 12},
        ],
        "notes": "Winner of Crawl XI: The Brawl By The Mall (2025)."
    },
    {
        "id": "angelos",
        "name": "Angelo's Coal Oven Pizzeria",
        "sheet_names": ["Angelo’s"],
        "address": "117 W 57th St, New York, NY 10019",
        "neighborhood": "Midtown",
        "region": "Manhattan",
        "lat": 40.7647,
        "lng": -73.9781,
        "best_rank": 14,
        "best_score": 3.920,
        "appearances": [
            {"year": 2018, "crawl": 'Crawl IV: "Fire and Slice"', "score": 3.920, "rank": 14},
        ],
        "notes": "3rd place in Crawl IV: Fire and Slice (2018)."
    },
    {
        "id": "slicehaus",
        "name": "Slicehaus Pizzeria",
        "sheet_names": ["Slicehaus Pizzeria"],
        "address": "30 Carmine St, New York, NY 10014",
        "neighborhood": "Greenwich Village",
        "region": "Manhattan",
        "lat": 40.7300,
        "lng": -74.0028,
        "best_rank": 17,
        "best_score": 3.868,
        "appearances": [
            {"year": 2026, "crawl": 'Crawl XII: "The BKLYN/MHTN Throwdown"', "score": 3.868, "rank": 17},
        ],
        "notes": "Featured in Crawl XII (2026)."
    },
    {
        "id": "louie-and-ernies",
        "name": "Louie & Ernie's Pizza",
        "sheet_names": ["Louie & Ernie's"],
        "address": "1300 Crosby Ave, Bronx, NY 10461",
        "neighborhood": "Schuylerville / Pelham Bay",
        "region": "Bronx",
        "lat": 40.8386,
        "lng": -73.8294,
        "best_rank": 18,
        "best_score": 3.850,
        "appearances": [
            {"year": 2019, "crawl": 'Crawl V: "Da Brawl in Da Bronx"', "score": 3.850, "rank": 18},
        ],
        "notes": "Winner of Crawl V: Da Brawl in Da Bronx (2019)."
    },
    {
        "id": "joes-pizza",
        "name": "Joe's Pizza",
        "sheet_names": ["Joe’s"],
        "address": "7 Carmine St, New York, NY 10014",
        "neighborhood": "Greenwich Village",
        "region": "Manhattan",
        "lat": 40.7306,
        "lng": -74.0021,
        "best_rank": 19,
        "best_score": 3.830,
        "appearances": [
            {"year": 2017, "crawl": 'Crawl III: "Cheese in Heat"', "score": 3.830, "rank": 19},
        ],
        "notes": "Winner of Crawl III: Cheese in Heat (2017)."
    },
    {
        "id": "sallys",
        "name": "Sally's Apizza",
        "sheet_names": ["Sally's"],
        "address": "237 Wooster St, New Haven, CT 06511",
        "neighborhood": "Wooster Square",
        "region": "New Haven, CT",
        "lat": 41.3029,
        "lng": -72.9197,
        "best_rank": 20,
        "best_score": 3.800,
        "appearances": [
            {"year": 2020, "crawl": 'Crawl VI: "A Little Slice of Haven"', "score": 3.800, "rank": 20},
        ],
        "notes": "Winner of Crawl VI: A Little Slice of Haven (2020)."
    },
    {
        "id": "deninos",
        "name": "Denino's Pizzeria & Tavern",
        "sheet_names": ["Denino's"],
        "address": "524 Port Richmond Ave, Staten Island, NY 10302",
        "neighborhood": "Port Richmond",
        "region": "Staten Island",
        "lat": 40.6305,
        "lng": -74.1404,
        "best_rank": 21,
        "best_score": 3.770,
        "appearances": [
            {"year": 2022, "crawl": 'Crawl VIII: "One Cheesy Island"', "score": 3.770, "rank": 21},
        ],
        "notes": "Runner-up in Crawl VIII (2022)."
    },
    {
        "id": "pugsley",
        "name": "Pugsley Pizza",
        "sheet_names": ["Pugsley"],
        "address": "590 E 191st St, Bronx, NY 10458",
        "neighborhood": "Belmont / Fordham",
        "region": "Bronx",
        "lat": 40.8594,
        "lng": -73.8860,
        "best_rank": 22,
        "best_score": 3.750,
        "appearances": [
            {"year": 2019, "crawl": 'Crawl V: "Da Brawl in Da Bronx"', "score": 3.750, "rank": 22},
        ],
        "notes": "Runner-up in Crawl V: Da Brawl in Da Bronx (2019)."
    },
    {
        "id": "ceres",
        "name": "Ceres Pizza",
        "sheet_names": ["Ceres Pizza"],
        "address": "164 Mott St, New York, NY 10013",
        "neighborhood": "Little Italy / Nolita",
        "region": "Manhattan",
        "lat": 40.7196,
        "lng": -73.9963,
        "best_rank": 23,
        "best_score": 3.750,
        "appearances": [
            {"year": 2026, "crawl": 'Crawl XII: "The BKLYN/MHTN Throwdown"', "score": 3.750, "rank": 23},
        ],
        "notes": "Featured in Crawl XII (2026)."
    },
    {
        "id": "ignazios",
        "name": "Ignazio's",
        "sheet_names": ["Ignazio's"],
        "address": "4 Water St, Brooklyn, NY 11201",
        "neighborhood": "DUMBO",
        "region": "Brooklyn",
        "lat": 40.7031,
        "lng": -73.9937,
        "best_rank": 24,
        "best_score": 3.640,
        "appearances": [
            {"year": 2021, "crawl": 'Crawl VII: "Saturday Slice Fever"', "score": 3.640, "rank": 24},
        ],
        "notes": "Under the Brooklyn Bridge in DUMBO."
    },
    {
        "id": "totonnos",
        "name": "Totonno's Pizzeria Napolitano",
        "sheet_names": ["Totonno's"],
        "address": "1524 Neptune Ave, Brooklyn, NY 11224",
        "neighborhood": "Coney Island",
        "region": "Brooklyn",
        "lat": 40.5789,
        "lng": -73.9838,
        "best_rank": 25,
        "best_score": 3.620,
        "appearances": [
            {"year": 2016, "crawl": "Crawl II", "score": 3.620, "rank": 25},
            {"year": 2015, "crawl": "The New York Pizza Crawl", "score": None, "rank": None},
        ],
        "notes": "Historic Coney Island coal-oven pizzeria (featured in 2015 & 2016)."
    },
    {
        "id": "upside",
        "name": "Upside Pizza",
        "sheet_names": ["Upside"],
        "address": "598 8th Ave, New York, NY 10018",
        "neighborhood": "Garment District / Midtown",
        "region": "Manhattan",
        "lat": 40.7554,
        "lng": -73.9904,
        "best_rank": 26,
        "best_score": 3.620,
        "appearances": [
            {"year": 2023, "crawl": 'Crawl IX: "Rumble in the Concrete Jungle"', "score": 3.620, "rank": 26},
        ],
        "notes": "Runner-up in Crawl IX: Rumble in the Concrete Jungle (2023)."
    },
    {
        "id": "zuppardis",
        "name": "Zuppardi's Apizza",
        "sheet_names": ["Zuppardi's"],
        "address": "179 Union Ave, West Haven, CT 06516",
        "neighborhood": "West Haven",
        "region": "New Haven, CT",
        "lat": 41.2762,
        "lng": -72.9482,
        "best_rank": 27,
        "best_score": 3.610,
        "appearances": [
            {"year": 2020, "crawl": 'Crawl VI: "A Little Slice of Haven"', "score": 3.610, "rank": 27},
        ],
        "notes": "Runner-up in Crawl VI: A Little Slice of Haven (2020)."
    },
    {
        "id": "luzzos",
        "name": "Luzzo's",
        "sheet_names": ["Luzzo’s"],
        "address": "211 1st Ave, New York, NY 10003",
        "neighborhood": "East Village",
        "region": "Manhattan",
        "lat": 40.7305,
        "lng": -73.9834,
        "best_rank": 28,
        "best_score": 3.600,
        "appearances": [
            {"year": 2018, "crawl": 'Crawl IV: "Fire and Slice"', "score": 3.600, "rank": 28},
        ],
        "notes": "Coal-oven Neapolitan spot in the East Village."
    },
    {
        "id": "patsys",
        "name": "Patsy's Pizzeria",
        "sheet_names": ["Patsy’s"],
        "address": "2287 1st Ave, New York, NY 10035",
        "neighborhood": "East Harlem",
        "region": "Manhattan",
        "lat": 40.7972,
        "lng": -73.9348,
        "best_rank": 29,
        "best_score": 3.590,
        "appearances": [
            {"year": 2017, "crawl": 'Crawl III: "Cheese in Heat"', "score": 3.590, "rank": 29},
        ],
        "notes": "Original 1933 East Harlem coal-oven landmark; runner-up in Crawl III."
    },
    {
        "id": "giove",
        "name": "Pizzeria Giove",
        "sheet_names": ["Pizzeria Giove"],
        "address": "278 New Dorp Ln, Staten Island, NY 10306",
        "neighborhood": "New Dorp",
        "region": "Staten Island",
        "lat": 40.5724,
        "lng": -74.1130,
        "best_rank": 30,
        "best_score": 3.570,
        "appearances": [
            {"year": 2022, "crawl": 'Crawl VIII: "One Cheesy Island"', "score": 3.570, "rank": 30},
        ],
        "notes": "Featured in Crawl VIII: One Cheesy Island (2022)."
    },
    {
        "id": "nunzios",
        "name": "Nunzio's Pizzeria",
        "sheet_names": ["Nunzio's"],
        "address": "2155 Hylan Blvd, Staten Island, NY 10306",
        "neighborhood": "Grant City / Midland Beach",
        "region": "Staten Island",
        "lat": 40.5784,
        "lng": -74.1021,
        "best_rank": 32,
        "best_score": 3.560,
        "appearances": [
            {"year": 2022, "crawl": 'Crawl VIII: "One Cheesy Island"', "score": 3.560, "rank": 32},
        ],
        "notes": "Historic Staten Island pizzeria (featured in Crawl VIII, 2022)."
    },
    {
        "id": "rubirosa",
        "name": "Rubirosa",
        "sheet_names": ["Rubirosa"],
        "address": "235 Mulberry St, New York, NY 10012",
        "neighborhood": "Nolita",
        "region": "Manhattan",
        "lat": 40.7227,
        "lng": -73.9962,
        "best_rank": 33,
        "best_score": 3.530,
        "appearances": [
            {"year": 2023, "crawl": 'Crawl IX: "Rumble in the Concrete Jungle"', "score": 3.530, "rank": 33},
        ],
        "notes": "Famous for thin-crust & tie-dye pizza (founded by Joe & Pat's family)."
    },
    {
        "id": "lombardis",
        "name": "Lombardi's",
        "sheet_names": ["Lombardi’s"],
        "address": "32 Spring St, New York, NY 10012",
        "neighborhood": "Nolita",
        "region": "Manhattan",
        "lat": 40.7216,
        "lng": -73.9956,
        "best_rank": 34,
        "best_score": 3.510,
        "appearances": [
            {"year": 2018, "crawl": 'Crawl IV: "Fire and Slice"', "score": 3.510, "rank": 34},
        ],
        "notes": "Recognized as America's first pizzeria (1905)."
    },
    {
        "id": "marios",
        "name": "Mario's Restaurant",
        "sheet_names": ["Mario's"],
        "address": "2342 Arthur Ave, Bronx, NY 10458",
        "neighborhood": "Belmont (Arthur Ave)",
        "region": "Bronx",
        "lat": 40.8542,
        "lng": -73.8878,
        "best_rank": 35,
        "best_score": 3.500,
        "appearances": [
            {"year": 2019, "crawl": 'Crawl V: "Da Brawl in Da Bronx"', "score": 3.500, "rank": 35},
        ],
        "notes": "Arthur Avenue Little Italy institution since 1919."
    },
    {
        "id": "polpettina",
        "name": "Polpettina",
        "sheet_names": ["Polpettina ", "Polpettina"],
        "address": "102 Fisher Ave, Eastchester, NY 10709",
        "neighborhood": "Eastchester",
        "region": "Westchester",
        "lat": 40.9571,
        "lng": -73.8091,
        "best_rank": 36,
        "best_score": 3.480,
        "appearances": [
            {"year": 2025, "crawl": "Crawl XI: The Brawl By The Mall", "score": 3.480, "rank": 36},
        ],
        "notes": "Runner-up in Crawl XI: The Brawl By The Mall (2025)."
    },
    {
        "id": "luigis",
        "name": "Luigi's Pizza",
        "sheet_names": ["Luigi's"],
        "address": "686 5th Ave, Brooklyn, NY 11215",
        "neighborhood": "South Slope",
        "region": "Brooklyn",
        "lat": 40.6606,
        "lng": -73.9935,
        "best_rank": 37,
        "best_score": 3.470,
        "appearances": [
            {"year": 2021, "crawl": 'Crawl VII: "Saturday Slice Fever"', "score": 3.470, "rank": 37},
        ],
        "notes": "Classic Brooklyn slice shop opened by Giovanni 'Luigi'igher."
    },
    {
        "id": "best-pizza",
        "name": "Best Pizza",
        "sheet_names": ["Best"],
        "address": "33 Havemeyer St, Brooklyn, NY 11211",
        "neighborhood": "Williamsburg",
        "region": "Brooklyn",
        "lat": 40.7152,
        "lng": -73.9541,
        "best_rank": 38,
        "best_score": 3.470,
        "appearances": [
            {"year": 2021, "crawl": 'Crawl VII: "Saturday Slice Fever"', "score": 3.470, "rank": 38},
        ],
        "notes": "Frank Pinello's wood-fired Williamsburg slice shop."
    },
    {
        "id": "abatinos",
        "name": "Abatino's Pizzeria",
        "sheet_names": ["Abatino's"],
        "address": "670 N Broadway, White Plains, NY 10603",
        "neighborhood": "North White Plains",
        "region": "Westchester",
        "lat": 41.0505,
        "lng": -73.7688,
        "best_rank": 39,
        "best_score": 3.460,
        "appearances": [
            {"year": 2025, "crawl": "Crawl XI: The Brawl By The Mall", "score": 3.460, "rank": 39},
        ],
        "notes": "Featured in Crawl XI: The Brawl By The Mall (2025)."
    },
    {
        "id": "dunwoodie",
        "name": "Dunwoodie Pizzeria",
        "sheet_names": ["Dunwoodie"],
        "address": "683 Yonkers Ave, Yonkers, NY 10704",
        "neighborhood": "Dunwoodie / Yonkers",
        "region": "Westchester",
        "lat": 40.9277,
        "lng": -73.8685,
        "best_rank": 40,
        "best_score": 3.360,
        "appearances": [
            {"year": 2025, "crawl": "Crawl XI: The Brawl By The Mall", "score": 3.360, "rank": 40},
        ],
        "notes": "Featured in Crawl XI: The Brawl By The Mall (2025)."
    },
    {
        "id": "scarrs",
        "name": "Scarr's Pizza",
        "sheet_names": ["Scarr's"],
        "address": "35 Orchard St, New York, NY 10002",
        "neighborhood": "Lower East Side / Chinatown",
        "region": "Manhattan",
        "lat": 40.7153,
        "lng": -73.9915,
        "best_rank": 41,
        "best_score": 3.320,
        "appearances": [
            {"year": 2023, "crawl": 'Crawl IX: "Rumble in the Concrete Jungle"', "score": 3.320, "rank": 41},
        ],
        "notes": "Known for milling their own grain in-house on Orchard St."
    },
    {
        "id": "prince-street",
        "name": "Prince Street Pizza",
        "sheet_names": ["Prince Street"],
        "address": "27 Prince St A, New York, NY 10012",
        "neighborhood": "Nolita",
        "region": "Manhattan",
        "lat": 40.7230,
        "lng": -73.9946,
        "best_rank": 42,
        "best_score": 3.280,
        "appearances": [
            {"year": 2017, "crawl": 'Crawl III: "Cheese in Heat"', "score": 3.280, "rank": 42},
        ],
        "notes": "Famous for the Spicy Spring Sicilian pepperoni square."
    },
    {
        "id": "motorino",
        "name": "Motorino Pizza",
        "sheet_names": ["Motorino's"],
        "address": "139 Broadway, Brooklyn, NY 11211",
        "neighborhood": "Williamsburg",
        "region": "Brooklyn",
        "lat": 40.7105,
        "lng": -73.9634,
        "best_rank": 44,
        "best_score": 3.270,
        "appearances": [
            {"year": 2016, "crawl": "Crawl II", "score": 3.270, "rank": 44},
        ],
        "notes": "Neapolitan pizza in Williamsburg (featured in Crawl II, 2016)."
    },
    {
        "id": "sals",
        "name": "Sal's Pizzeria",
        "sheet_names": ["Sal's"],
        "address": "316 Mamaroneck Ave, Mamaroneck, NY 10543",
        "neighborhood": "Mamaroneck",
        "region": "Westchester",
        "lat": 40.9519,
        "lng": -73.7351,
        "best_rank": 45,
        "best_score": 3.130,
        "appearances": [
            {"year": 2025, "crawl": "Crawl XI: The Brawl By The Mall", "score": 3.130, "rank": 45},
        ],
        "notes": "Westchester institution known for slices & Sicilian pies."
    },
    {
        "id": "williamsburg-mhtn",
        "name": "Williamsburg Pizza (Lower East Side)",
        "sheet_names": ["Williamsburg"],
        "address": "277 Broome St, New York, NY 10002",
        "neighborhood": "Lower East Side",
        "region": "Manhattan",
        "lat": 40.7181,
        "lng": -73.9912,
        "best_rank": 46,
        "best_score": 2.990,
        "appearances": [
            {"year": 2017, "crawl": 'Crawl III: "Cheese in Heat"', "score": 2.990, "rank": 46},
        ],
        "notes": "Manhattan outpost featured in Crawl III: Cheese in Heat (2017)."
    },
    {
        "id": "bar-nh",
        "name": "BAR",
        "sheet_names": ["BAR"],
        "address": "254 Crown St, New Haven, CT 06511",
        "neighborhood": "Downtown New Haven",
        "region": "New Haven, CT",
        "lat": 41.3061,
        "lng": -72.9309,
        "best_rank": 47,
        "best_score": 2.970,
        "appearances": [
            {"year": 2020, "crawl": 'Crawl VI: "A Little Slice of Haven"', "score": 2.970, "rank": 47},
        ],
        "notes": "Famous for mashed potato & bacon thin-crust apizza."
    },
    {
        "id": "frank-pepes",
        "name": "Frank Pepe Pizzeria Napoletana",
        "sheet_names": ["Frank Pepe's"],
        "address": "157 Wooster St, New Haven, CT 06511",
        "neighborhood": "Wooster Square",
        "region": "New Haven, CT",
        "lat": 41.3029,
        "lng": -72.9169,
        "best_rank": 48,
        "best_score": 2.950,
        "appearances": [
            {"year": 2020, "crawl": 'Crawl VI: "A Little Slice of Haven"', "score": 2.950, "rank": 48},
        ],
        "notes": "Historic 1925 New Haven coal-fired apizza landmark."
    },
    {
        "id": "modern-apizza",
        "name": "Modern Apizza",
        "sheet_names": ["Modern"],
        "address": "874 State St, New Haven, CT 06511",
        "neighborhood": "East Rock / State St",
        "region": "New Haven, CT",
        "lat": 41.3125,
        "lng": -72.9122,
        "best_rank": 49,
        "best_score": 2.910,
        "appearances": [
            {"year": 2020, "crawl": 'Crawl VI: "A Little Slice of Haven"', "score": 2.910, "rank": 49},
        ],
        "notes": "New Haven 'Big Three' brick-oven apizza icon since 1934."
    },
    {
        "id": "lees-tavern",
        "name": "Lee's Tavern",
        "sheet_names": ["Lee's Tavern"],
        "address": "60 Hancock St, Staten Island, NY 10305",
        "neighborhood": "Dongan Hills",
        "region": "Staten Island",
        "lat": 40.5888,
        "lng": -74.0919,
        "best_rank": 50,
        "best_score": 2.890,
        "appearances": [
            {"year": 2022, "crawl": 'Crawl VIII: "One Cheesy Island"', "score": 2.890, "rank": 50},
        ],
        "notes": "Classic Staten Island tavern bar-pie spot next to Dongan Hills SIR."
    },
    {
        "id": "sauce-pizzeria",
        "name": "Sauce Pizzeria",
        "sheet_names": ["Sauce Pizzeria"],
        "address": "78 E 1st St, New York, NY 10009",
        "neighborhood": "East Village",
        "region": "Manhattan",
        "lat": 40.7237,
        "lng": -73.9881,
        "best_rank": 51,
        "best_score": 2.780,
        "appearances": [
            {"year": 2023, "crawl": 'Crawl IX: "Rumble in the Concrete Jungle"', "score": 2.780, "rank": 51},
        ],
        "notes": "Featured in Crawl IX (2023)."
    },
    {
        "id": "sal-and-carmines",
        "name": "Sal & Carmine Pizza",
        "sheet_names": ["Sal and Carmine’s"],
        "address": "2671 Broadway, New York, NY 10025",
        "neighborhood": "Upper West Side",
        "region": "Manhattan",
        "lat": 40.7982,
        "lng": -73.9689,
        "best_rank": 52,
        "best_score": 2.670,
        "appearances": [
            {"year": 2017, "crawl": 'Crawl III: "Cheese in Heat"', "score": 2.670, "rank": 52},
        ],
        "notes": "Upper West Side neighborhood slice shop since 1959."
    },
    {
        "id": "3-boys-from-italy",
        "name": "3 Boys From Italy",
        "sheet_names": ["3 Boys from Italy"],
        "address": "704 E Burke Ave, Bronx, NY 10467",
        "neighborhood": "Williamsbridge / Olinville",
        "region": "Bronx",
        "lat": 40.8715,
        "lng": -73.8654,
        "best_rank": 53,
        "best_score": 2.630,
        "appearances": [
            {"year": 2019, "crawl": 'Crawl V: "Da Brawl in Da Bronx"', "score": 2.630, "rank": 53},
        ],
        "notes": "Featured in Crawl V: Da Brawl in Da Bronx (2019)."
    },
    {
        "id": "julianas",
        "name": "Juliana's Pizza",
        "sheet_names": ["Julianna's"],
        "address": "19 Old Fulton St, Brooklyn, NY 11201",
        "neighborhood": "DUMBO",
        "region": "Brooklyn",
        "lat": 40.7027,
        "lng": -73.9934,
        "best_rank": 54,
        "best_score": 2.620,
        "appearances": [
            {"year": 2016, "crawl": "Crawl II", "score": 2.620, "rank": 54},
        ],
        "notes": "Patsy Grimaldi's coal-fired DUMBO pizzeria."
    },
    {
        "id": "napolis-best",
        "name": "Napoli's Best Pizza",
        "sheet_names": ["Napoli's Best"],
        "address": "521 E Tremont Ave, Bronx, NY 10457",
        "neighborhood": "Tremont",
        "region": "Bronx",
        "lat": 40.8468,
        "lng": -73.8981,
        "best_rank": 55,
        "best_score": 2.180,
        "appearances": [
            {"year": 2019, "crawl": 'Crawl V: "Da Brawl in Da Bronx"', "score": 2.180, "rank": 55},
        ],
        "notes": "Featured in Crawl V: Da Brawl in Da Bronx (2019)."
    },
    {
        "id": "lb-spumoni",
        "name": "L&B Spumoni Gardens",
        "sheet_names": ["L&B"],
        "address": "2725 86th St, Brooklyn, NY 11223",
        "neighborhood": "Gravesend",
        "region": "Brooklyn",
        "lat": 40.5947,
        "lng": -73.9815,
        "best_rank": None,
        "best_score": None,
        "appearances": [
            {"year": 2015, "crawl": "The New York Pizza Crawl", "score": None, "rank": None},
        ],
        "notes": "Inaugural 2015 New York Pizza Crawl stop; famous for upside-down Sicilian squares."
    },
    {
        "id": "robertas",
        "name": "Roberta's",
        "sheet_names": ["Roberta's"],
        "address": "261 Moore St, Brooklyn, NY 11206",
        "neighborhood": "Bushwick",
        "region": "Brooklyn",
        "lat": 40.7051,
        "lng": -73.9336,
        "best_rank": None,
        "best_score": None,
        "appearances": [
            {"year": 2015, "crawl": "The New York Pizza Crawl", "score": None, "rank": None},
        ],
        "notes": "Inaugural 2015 New York Pizza Crawl stop in Bushwick."
    },
    {
        "id": "grimaldis",
        "name": "Grimaldi's Pizzeria",
        "sheet_names": ["Grimaldi's"],
        "address": "1 Front St, Brooklyn, NY 11201",
        "neighborhood": "DUMBO",
        "region": "Brooklyn",
        "lat": 40.7025,
        "lng": -73.9932,
        "best_rank": None,
        "best_score": None,
        "appearances": [
            {"year": 2015, "crawl": "The New York Pizza Crawl", "score": None, "rank": None},
        ],
        "notes": "Inaugural 2015 New York Pizza Crawl stop in DUMBO."
    }
]

desktop_dir = r"c:\Users\alexh\Desktop"

# 1. Generate CSV for Google My Maps
csv_path = os.path.join(desktop_dir, "Pizza_Crawl_Google_My_Maps.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Name", "Best Rank", "Best Score", "Address", "Neighborhood", "Region",
        "Latitude", "Longitude", "Crawl Appearances", "Latest Year", "Notes", "Google Maps Link"
    ])
    for p in PIZZA_PLACES:
        apps_str = " | ".join([
            f"{a['year']} {a['crawl']} (Rank #{a['rank']}, Score: {a['score']:.3f})"
            if a['score'] is not None else f"{a['year']} {a['crawl']} (Inaugural Crawl)"
            for a in p["appearances"]
        ])
        latest_year = max(a["year"] for a in p["appearances"])
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={p['name'].replace(' ', '+')}+{p['address'].replace(' ', '+')}"
        writer.writerow([
            p["name"],
            f"#{p['best_rank']}" if p["best_rank"] else "2015 Inaugural",
            f"{p['best_score']:.3f}" if p["best_score"] else "N/A",
            p["address"],
            p["neighborhood"],
            p["region"],
            p["lat"],
            p["lng"],
            apps_str,
            latest_year,
            p["notes"],
            gmaps_url
        ])

# 2. Generate KML for Google My Maps (with color-coded styles and folders by Region or Tier)
kml_path = os.path.join(desktop_dir, "Pizza_Crawl_Google_My_Maps.kml")
kml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<kml xmlns="http://www.opengis.net/kml/2.2">',
    '  <Document>',
    '    <name>Pizza Crawl Winners &amp; Contestants (2015–2026)</name>',
    '    <description>All 52 pizza places across Crawls I–XII (60 total appearances) with rankings and average scores.</description>',
    '    <Style id="tier-elite"><IconStyle><color>ff00b5ff</color><scale>1.1</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/ylw-stars.png</href></Icon></IconStyle></Style>',
    '    <Style id="tier-great"><IconStyle><color>ff34a853</color><scale>1.0</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/grn-circle.png</href></Icon></IconStyle></Style>',
    '    <Style id="tier-solid"><IconStyle><color>ff4285f4</color><scale>1.0</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/blu-circle.png</href></Icon></IconStyle></Style>',
    '    <Style id="tier-classic"><IconStyle><color>ffea4335</color><scale>1.0</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href></Icon></IconStyle></Style>',
    '    <Folder>',
    '      <name>All Pizza Crawl Contestants (Ranked)</name>'
]

for p in PIZZA_PLACES:
    score = p["best_score"]
    if score and score >= 4.0:
        style = "#tier-elite"
    elif score and score >= 3.6:
        style = "#tier-great"
    elif score and score >= 3.2:
        style = "#tier-solid"
    else:
        style = "#tier-classic"

    rank_label = f"#{p['best_rank']} " if p["best_rank"] else ""
    score_label = f" ({p['best_score']:.3f})" if p["best_score"] else " (2015 Crawl)"
    title = saxutils.escape(f"{rank_label}{p['name']}{score_label}")
    apps_html = "<br/>".join([
        saxutils.escape(
            f"• {a['year']} {a['crawl']}: Rank #{a['rank']} ({a['score']:.3f})"
            if a['score'] is not None else f"• {a['year']} {a['crawl']} (Inaugural)"
        )
        for a in p["appearances"]
    ])
    best_rank_str = f"#{p['best_rank']}" if p['best_rank'] else "N/A"
    best_score_str = f"{score:.3f}" if score else "Unscored (2015)"
    desc = (
        f"<![CDATA["
        f"<b>Address:</b> {saxutils.escape(p['address'])}<br/>"
        f"<b>Neighborhood:</b> {saxutils.escape(p['neighborhood'])} ({saxutils.escape(p['region'])})<br/>"
        f"<b>Best Score:</b> {best_score_str}<br/>"
        f"<b>Best Overall Ranking:</b> {best_rank_str}<br/><br/>"
        f"<b>Crawl History:</b><br/>{apps_html}<br/><br/>"
        f"<i>{saxutils.escape(p['notes'])}</i>"
        f"]]>"
    )
    kml_lines.extend([
        '      <Placemark>',
        f'        <name>{title}</name>',
        f'        <description>{desc}</description>',
        f'        <styleUrl>{style}</styleUrl>',
        '        <Point>',
        f'          <coordinates>{p["lng"]},{p["lat"]},0</coordinates>',
        '        </Point>',
        '      </Placemark>'
    ])

kml_lines.extend([
    '    </Folder>',
    '  </Document>',
    '</kml>'
])

with open(kml_path, "w", encoding="utf-8") as f:
    f.write("\n".join(kml_lines))

print(f"Saved CSV ({len(PIZZA_PLACES)} places) to {csv_path}")
print(f"Saved KML ({len(PIZZA_PLACES)} places) to {kml_path}")
