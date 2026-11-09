def test_snp_distance_matrix(client):
    response = client.post("/api/v1/comparative/snp-matrix", json={"reference_genome": "HS11286"})
    assert response.status_code == 200
    data = response.json()
    assert data["isolate_count"] >= 8
    matrix = data["distance_matrix"]
    accessions = data["accessions"]
    assert len(matrix) == len(accessions)
    
    # Symmetrical matrix check: matrix[i][j] == matrix[j][i]
    for i in range(len(matrix)):
        assert matrix[i][i] == 0
        for j in range(len(matrix)):
            assert matrix[i][j] == matrix[j][i]

    # Verify Vadodara micro-outbreak isolates (indices of GCA_013374875.1 and GCA_013374895.1)
    idx1 = accessions.index("GCA_013374875.1")
    idx2 = accessions.index("GCA_013374895.1")
    assert matrix[idx1][idx2] == 6

def test_phylogenetic_tree_newick(client):
    response = client.get("/api/v1/comparative/tree")
    assert response.status_code == 200
    tree = response.json()
    assert "newick_string" in tree
    assert tree["substitution_model"] == "GTR+F+R4"
    assert "GCA_013374875.1" in tree["newick_string"]
    assert "metadata_tracks" in tree

