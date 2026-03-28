"""Search OSM for any tag value containing '4-way' — small area first to discover tags."""

import json, urllib.request, urllib.parse

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Small bbox: Chicago area
query = """[out:json][timeout:60];
(
  node[~"."~"4.way|4.WAY|4_way",i](41.6,-88.0,42.1,-87.5);
);
out body;"""

print("Searching Chicago area for any tag with '4-way'...")
req = urllib.request.Request(
    OVERPASS_URL,
    data=f"data={urllib.parse.quote(query)}".encode(),
    method="POST",
)
resp = urllib.request.urlopen(req, timeout=120)
nodes = json.loads(resp.read())["elements"]
print(f"Got {len(nodes)} nodes\n")

for n in nodes[:30]:
    tags = n.get("tags", {})
    matching = {k: v for k, v in tags.items() if "4" in v.lower() and "way" in v.lower()}
    print(f"  {n['lat']}, {n['lon']} -> {matching}  (all: {tags})")
