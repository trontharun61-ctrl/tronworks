"""
Fetch railroad crossing sign locations in the US from OpenStreetMap.
OSM tag: railway=level_crossing (road crosses rail at grade)
These are the locations with the crossbuck / railroad crossing signs.
"""

import csv
import json
import time
import urllib.request
import urllib.parse

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
TARGET = 2000

# Query regions to avoid timeout on full US
REGIONS = [
    ("Midwest",    39.0, -90.0, 43.0, -84.0),
    ("Plains",     38.0, -100.0, 43.0, -94.0),
    ("Southeast",  32.0, -88.0, 36.0, -82.0),
    ("Texas",      29.0, -99.0, 33.0, -95.0),
    ("Northeast",  40.0, -76.0, 43.0, -72.0),
    ("West",       34.0, -120.0, 38.0, -115.0),
    ("NW",         45.0, -123.0, 48.0, -117.0),
]

all_nodes = {}

for name, south, west, north, east in REGIONS:
    if len(all_nodes) >= TARGET:
        break
    need = TARGET - len(all_nodes)
    query = f"""[out:json][timeout:120];
node["railway"="level_crossing"]({south},{west},{north},{east});
out body {need + 500};"""

    print(f"[{name}] Querying (have {len(all_nodes)}, need {need})...")
    try:
        req = urllib.request.Request(
            OVERPASS_URL,
            data=f"data={urllib.parse.quote(query)}".encode(),
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=180)
        nodes = json.loads(resp.read())["elements"]
        print(f"  -> {len(nodes)} results")
        for n in nodes:
            all_nodes[n["id"]] = n
    except Exception as e:
        print(f"  -> ERROR: {e}")
    time.sleep(5)

results = list(all_nodes.values())[:TARGET]
print(f"\nTotal: {len(results)} railroad crossing locations")

output_file = "notebooks/rail_crossings_us.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["osm_id", "latitude", "longitude", "all_tags"])
    for n in results:
        tags = n.get("tags", {})
        writer.writerow([n["id"], n["lat"], n["lon"], json.dumps(tags)])

print(f"CSV written to {output_file}")
