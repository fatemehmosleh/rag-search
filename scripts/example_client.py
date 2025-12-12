"""Small example client to test /health, /search and /rag endpoints.

Usage:
  python scripts/example_client.py --host http://localhost:8000

It prints JSON responses and HTTP status codes.
"""
import argparse
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="http://localhost:8000", help="Base URL of the server")
args = parser.parse_args()

base = args.host.rstrip("/")

print('Health:')
r = requests.get(f"{base}/health")
print(r.status_code, r.json())

print('\nSearch:')
r = requests.post(f"{base}/search/", json={"query": "Where are bike lanes near downtown?"})
print(r.status_code)
try:
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception:
    print(r.text)

print('\nRAG (may be slow / require Ollama):')
r = requests.post(f"{base}/rag/", json={"query": "Where are bike lanes near downtown and what is PM2.5 there now?"})
print(r.status_code)
try:
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception:
    print(r.text)
