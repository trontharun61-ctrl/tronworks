"""
Fetch locations of physical "2-WAY" stop sign plaques from OpenStreetMap.

Searches for nodes tagged with traffic_sign values containing:
- "2-WAY" or "2_way" or "two_way" (sign text)
- MUTCD codes like R1-3aP (2-WAY plaque designation)

Also searches for highway=stop nodes where stop=minor or stop=2-way
"""

import csv
import json
import time
import urllib.request
import urllib.parse

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Multiple queries to cast a wide net for 2-WAY plaques in the US
QUERIES = [
    # traffic_sign tag containing 2-way references
    """[out:json][timeout:180];
    (
      node["traffic_sign"~"2.way|2.WAY|two.way",i](24.5,-125.0,49.5,-66.9);
      node["traffic_sign:supplementary"~"2.way|2.WAY|two.way",i](24.5,-125.0,49.5,-66.9);
    );
    out body;""",

    # MUTCD sign code for 2-WAY plaque
    """[out:json][timeout:180];
    (
      node["traffic_sign"~"R1-3a|R1-4",i](24.5,-125.0,49.5,-66.9);
      node["traffic_sign:supplementary"~"R1-3a|R1-4",i](24.5,-125.0,49.5,-66.9);
    );
    out body;""",

    # stop=2-way or stop=minor explicit tags
    """[out:json][timeout:180];
    (
      node["highway"="stop"]["stop"="minor"](24.5,-125.0,49.5,-66.9);
      node["highway"="stop"]["stop"~"2",i](24.5,-125.0,49.5,-66.9);
    );
    out body;""",
]

all_nodes = {}

for i, query in enumerate(QUERIES):
    print(f"Running query {i+1}/{len(QUERIES)}...")
    try:
        req = urllib.request.Request(
            OVERPASS_URL,
            data=f"data={urllib.parse.quote(query)}".encode(),
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=240)
        nodes = json.loads(resp.read())["elements"]
        print(f"  -> {len(nodes)} results")
        for n in nodes:
            all_nodes[n["id"]] = n
    except Exception as e:
        print(f"  -> ERROR: {e}")
    time.sleep(10)

results = list(all_nodes.values())
print(f"\nTotal unique nodes: {len(results)}")

output_file = "notebooks/two_way_stops_us.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["osm_id", "latitude", "longitude", "traffic_sign", "stop_tag", "all_tags"])
    for n in results:
        tags = n.get("tags", {})
        writer.writerow([
            n["id"],
            n["lat"],
            n["lon"],
            tags.get("traffic_sign", tags.get("traffic_sign:supplementary", "")),
            tags.get("stop", ""),
            json.dumps(tags),
        ])

print(f"CSV written to {output_file}")
