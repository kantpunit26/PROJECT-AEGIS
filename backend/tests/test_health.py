def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "PROJECT AEGIS 2.0" in data["system"]
    assert data["database"] == "healthy"
    assert data["primary_organism"] == "Klebsiella pneumoniae"

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert data["api_v1"] == "/api/v1"

