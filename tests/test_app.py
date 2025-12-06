from app import app


def test_index_route():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from Python Static Site!" in resp.data


def test_health_route():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert json_data["status"] == "ok"
