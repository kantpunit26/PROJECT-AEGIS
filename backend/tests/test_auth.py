def test_auth_login_success(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "researcher",
        "password": "aegis_research_2026"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "researcher"

def test_auth_login_failure(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "researcher",
        "password": "incorrect_password"
    })
    assert response.status_code == 401

