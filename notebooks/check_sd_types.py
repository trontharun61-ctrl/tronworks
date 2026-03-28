import json, urllib.request, urllib.parse

url = "https://sdgis.sd.gov/dot/rest/services/TIM/DOT_Intersections_viewer/MapServer/0/query"
stats = json.dumps([{"statisticType": "count", "onStatisticField": "OBJECTID", "outStatisticFieldName": "cnt"}])
params = {
    "where": "1=1",
    "groupByFieldsForStatistics": "TRAFFIC_CONTROL_TYPE",
    "outStatistics": stats,
    "f": "json",
}
qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
resp = urllib.request.urlopen(f"{url}?{qs}", timeout=30)
data = json.loads(resp.read())
for f in data.get("features", []):
    a = f["attributes"]
    print(f"  Type {a['TRAFFIC_CONTROL_TYPE']}: {a['cnt']} intersections")
