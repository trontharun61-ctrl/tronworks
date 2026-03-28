"""Try more ArcGIS sources for 4-way stops."""
import json, urllib.request, urllib.parse

# Check Phoenix traffic restrictions
print("Checking Phoenix...")
try:
    url = "https://maps.phoenix.gov/pub/rest/services/Public/TrafficRestrictions/MapServer/0?f=json"
    resp = urllib.request.urlopen(url, timeout=30)
    meta = json.loads(resp.read())
    for f in meta.get("fields", []):
        print(f"  {f['name']}: {f['type']} - {f.get('alias','')}")
except Exception as e:
    print(f"  Error: {e}")

# Check Madison WI intersection control
print("\nChecking Madison WI...")
try:
    url = "https://maps.cityofmadison.com/arcgis/rest/services/Public/TrafficControl/MapServer/0?f=json"
    resp = urllib.request.urlopen(url, timeout=30)
    meta = json.loads(resp.read())
    for f in meta.get("fields", []):
        print(f"  {f['name']}: {f['type']} - {f.get('alias','')}")
except Exception as e:
    print(f"  Error: {e}")

# Try San Antonio
print("\nChecking San Antonio...")
try:
    # Search for their open data
    url = "https://gis.sanantonio.gov/server/rest/services?f=json"
    resp = urllib.request.urlopen(url, timeout=30)
    data = json.loads(resp.read())
    for svc in data.get("services", [])[:20]:
        if "traffic" in svc["name"].lower() or "sign" in svc["name"].lower() or "intersection" in svc["name"].lower():
            print(f"  {svc['name']} ({svc['type']})")
except Exception as e:
    print(f"  Error: {e}")
