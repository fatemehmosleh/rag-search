
# app/pipelines/ingest_openaq.py
import os
import json
import requests

API_BASE = "https://api.openaq.org/v3"

def _require_key():
    api_key = os.getenv("OPENAQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing OPENAQ_API_KEY. Set it in your environment or .env. "
            "Docs: https://docs.openaq.org/using-the-api/api-key"
        )
    return api_key

def fetch_locations_bbox(bbox, limit=1000):
    """
    Fetch locations within a bounding box using OpenAQ v3.
    bbox: [west, south, east, north]
    """
    api_key = _require_key()
    params = {
        "bbox": ",".join(map(str, bbox)),
        "limit": str(limit),
    }
    headers = {"X-API-Key": api_key}
    url = f"{API_BASE}/locations"
    r = requests.get(url, params=params, headers=headers, timeout=30)
    # 401 if key missing/invalid; 404 if path wrong; see errors doc
    # https://docs.openaq.org/errors/about
    r.raise_for_status()
    return r.json()

def to_location_chunks(data):
    """
    Convert /v3/locations results to RAG-friendly chunks.
    """
    for loc in data.get("results", []):
        name = loc.get("name")
        coords = loc.get("coordinates")
        country = (loc.get("country") or {}).get("name")
        timezone = loc.get("timezone")
        parameters = []
        # sensors describe parameters; some feeds expose them at location level
        for s in loc.get("sensors", []):
            p = s.get("parameter", {})
            if p:
                parameters.append(p.get("name"))
        param_list = ", ".join(sorted(set(parameters))) if parameters else "unknown"

        text = (
            f"Air quality location: {name} in {country}; "
            f"coords={coords}; timezone={timezone}; parameters={param_list}"
        )
        yield {
            "text": text,
            "source": "OpenAQ v3 /locations",
            "type": "air_quality_location",
            "location_id": loc.get("id"),
            "location_name": name,
            "country": country,
            "coordinates": coords,
            "timezone": timezone,
            "parameters": parameters
        }

# Optional: fetch recent measurements per sensor (commented by default)
def fetch_sensor_measurements(sensor_id, limit=100):
    """
    GET /v3/sensors/{sensor_id}/measurements
    """
    api_key = _require_key()
    headers = {"X-API-Key": api_key}
    url = f"{API_BASE}/sensors/{sensor_id}/measurements"
    params = {"limit": str(limit)}
    r = requests.get(url, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def to_measurement_chunks(sensor_id, data):
    for m in data.get("results", []):
        param = m.get("parameter")
        val = m.get("value")
        unit = m.get("unit")
        ts = m.get("datetime", {}).get("utc") or m.get("lastUpdated")
        text = f"Sensor {sensor_id}: {param}={val} {unit} at {ts}"
        yield {
            "text": text,
            "source": "OpenAQ v3 /sensors/{id}/measurements",
            "type": "air_quality_measurement",
            "sensor_id": sensor_id,
            "parameter": param,
            "value": val,
            "unit": unit,
            "timestamp_utc": ts
        }

def run(bbox):
    os.makedirs("data/clean", exist_ok=True)
    # Step 1: locations by bbox
    locations = fetch_locations_bbox(bbox)
    loc_out = "data/clean/openaq_locations.jsonl"
    with open(loc_out, "w", encoding="utf-8") as f:
        for ch in to_location_chunks(locations):
            f.write(json.dumps(ch, ensure_ascii=False) + "\n")
    print(f"✅ Wrote location chunks to {loc_out}")

    # Step 2 (optional): expand with sensor measurements
    # Uncomment the lines below to pull recent values for each sensor
    # meas_out = "data/clean/openaq_measurements.jsonl"
    # count = 0
    # with open(meas_out, "w", encoding="utf-8") as f:
    #     for loc in locations.get("results", []):
    #         for s in loc.get("sensors", []):
    #             sid = s.get("id")
    #             if sid:
    #                 data = fetch_sensor_measurements(sid, limit=50)
    #                 for ch in to_measurement_chunks(sid, data):
    #                     f.write(json.dumps(ch, ensure_ascii=False) + "\n")
    #                     count += 1
    # print(f"🔎 Wrote {count} sensor measurement chunks to {meas_out}")

if __name__ == "__main__":
    # Example bbox — change to your city
    # Docs show bbox usage against /v3/locations. [1](https://github.com/google/transit/blob/master/gtfs-realtime/spec/en/README.md)
    run([-79.6, 43.6, -79.2, 43.8])
