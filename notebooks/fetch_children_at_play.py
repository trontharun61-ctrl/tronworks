"""
Fetch "Children at Play" sign locations in the US from OpenStreetMap.

Searches for nodes with relevant tags:
- traffic_sign containing "children" references
- warning signs for children/playground zones
- hazard=children or similar tags
"""

import csv
import json
import time
import urllib.request
import urllib.parse

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

QUERIES = [
    # traffic_sign tags mentioning children at play
    """[out:json][timeout:180];
    (
      node["traffic_sign"~"children|child_at_play|children_at_play|W15-1",i](24.5,-125.0,49.5,-66.9);
      node["traffic_sign:supplementary"~"children|child",i](24.5,-125.0,49.5,-66.9);
    );
    out body;""",

    # warning=children or hazard=children tags
    """[out:json][timeout:180];
    (
      node["hazard"~"children",i](24.5,-125.0,49.5,-66.9);
      node["warning"~"children",i](24.5,-125.0,49.5,-66.9);
    );
    out body;""",

    # highway=traffic_sign with children-related values
    """[out:json][timeout:180];
    (
      node["traffic_sign"~"playground|play_area|slow.*children|children.*play",i](24.5,-125.0,49.5,-66.9);
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

output_file = "notebooks/children_at_play_us.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["osm_id", "latitude", "longitude", "traffic_sign", "all_tags"])
    for n in results:
        tags = n.get("tags", {})
        writer.writerow([
            n["id"],
            n["lat"],
            n["lon"],
            tags.get("traffic_sign", tags.get("warning", tags.get("hazard", ""))),
            json.dumps(tags),
        ])

print(f"CSV written to {output_file}")
