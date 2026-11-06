def test_list_isolates(client):
    response = client.get("/api/v1/isolates")
    assert response.status_code == 200
    isolates = response.json()
    assert len(isolates) >= 8
    # Verify primary organism
    assert all(i["organism"] == "Klebsiella pneumoniae" for i in isolates)

def test_filter_isolates_by_amr_gene(client):
    response = client.get("/api/v1/isolates?amr_gene=NDM")
    assert response.status_code == 200
    isolates = response.json()
    assert len(isolates) >= 2
    accessions = [i["accession"] for i in isolates]
    assert "GCA_013374875.1" in accessions

def test_get_isolate_detail(client):
    response = client.get("/api/v1/isolates/GCA_000300435.1")
    assert response.status_code == 200
    data = response.json()
    assert data["strain"] == "HS11286"
    assert len(data["amr_determinants"]) >= 4
    # Check blaKPC-2
    genes = [d["gene_symbol"] for d in data["amr_determinants"]]
    assert "blaKPC-2" in genes
