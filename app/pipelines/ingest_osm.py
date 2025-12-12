
import requests, json, os
OVERPASS = "https://overpass-api.de/api/interpreter"  # public instance

def query_bike_lanes(city="Toronto"):
    # Overpass QL — see Language Guide & examples
    q = f"""
    [out:json][timeout:60];
    area["name"="{city}"]->.a;
    (
      way(area.a)["highway"="cycleway"];
      way(area.a)["cycleway"~"lane|track"];
    );
    out body;
    """
    r = requests.post(OVERPASS, data={"data": q}, timeout=90)
    r.raise_for_status()
    return r.json()

def to_chunks(data):
    for e in data.get("elements", []):
        tags = e.get("tags", {})
        name = tags.get("name", "Unnamed")
        yield {
            "text": f"Bike lane: {name}; tags={tags}",
            "source": "Overpass API (OSM)",
            "type": "bike_lane",
        }

def run(city="Toronto"):
    os.makedirs("data/clean", exist_ok=True)
    d = query_bike_lanes(city)
    with open("data/clean/osm_bikes.jsonl", "w") as f:
        for ch in to_chunks(d):
            f.write(json.dumps(ch) + "\n")

if __name__ == "__main__":
    run("Toronto")
