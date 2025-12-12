
import zipfile, csv, json, os

def parse_gtfs_zip(path):
    z = zipfile.ZipFile(path)
    stops = {row["stop_id"]: row for row in csv.DictReader(z.open("stops.txt").read().decode().splitlines())}
    trips = {row["trip_id"]: row for row in csv.DictReader(z.open("trips.txt").read().decode().splitlines())}
    out = []
    for row in csv.DictReader(z.open("stop_times.txt").read().decode().splitlines()):
        stop = stops.get(row["stop_id"], {})
        trip = trips.get(row["trip_id"], {})
        out.append({
            "text": f"Route {trip.get('route_id')} Trip {row['trip_id']} Stop {stop.get('stop_name')} at {row['arrival_time']}",
            "source": "GTFS static",
            "type": "transit_schedule",
            "stop_name": stop.get("stop_name"),
            "arrival_time": row["arrival_time"],
        })
    return out

def run(path="data/raw/gtfs.zip"):
    os.makedirs("data/clean", exist_ok=True)
    chunks = parse_gtfs_zip(path)
    with open("data/clean/gtfs_schedule.jsonl", "w") as f:
        for ch in chunks:
            f.write(json.dumps(ch) + "\n")

if __name__ == "__main__":
    run()
