# tests/test_app.py
import os
import sys

# Add project root (/app in container) to PYTHONPATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app


def test_index_route():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"testing pr" in resp.data   # change expectation



def test_health_route():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert json_data["status"] == "ok"
