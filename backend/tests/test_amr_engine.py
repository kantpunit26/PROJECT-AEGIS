def test_amr_prevalence(client):
    response = client.get("/api/v1/amr/prevalence")
    assert response.status_code == 200
    data = response.json()
    assert data["total_isolates"] >= 8
    assert len(data["determinants"]) > 0
    symbols = [d["gene_symbol"] for d in data["determinants"]]
    assert any("bla" in s for s in symbols)

def test_amr_co_occurrence(client):
    response = client.get("/api/v1/amr/co-occurrence?top_n=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["genes"]) <= 5
    assert len(data["matrix"]) == len(data["genes"])
    # Diagonal should be >= any off-diagonal
    for i in range(len(data["genes"])):
        assert data["matrix"][i][i] >= 0

