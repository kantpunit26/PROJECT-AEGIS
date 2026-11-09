def test_spatial_clusters(client):
    response = client.get("/api/v1/surveillance/spatial-clusters")
    assert response.status_code == 200
    clusters = response.json()
    assert len(clusters) >= 8
    # Coordinate validity
    for c in clusters:
        assert -90.0 <= c["latitude"] <= 90.0
        assert -180.0 <= c["longitude"] <= 180.0

def test_natural_language_spatial_query(client):
    query_payload = {
        "query": "Show all K. pneumoniae isolates with blaNDM within 50 km of Vadodara"
    }
    response = client.post("/api/v1/surveillance/nl-query", json=query_payload)
    assert response.status_code == 200
    res = response.json()
    assert res["interpreted_query"]["target_location"] == "Vadodara"
    assert res["interpreted_query"]["radius_km"] == 50.0
    assert res["total_matched"] == 2
    matched = res["matched_isolates"]
    for m in matched:
        assert m["distance_km"] <= 50.0
        assert any("NDM" in gene for gene in m["carbapenemases"])

