def test_ast_concordance_metrics(client):
    response = client.get("/api/v1/ast/concordance")
    assert response.status_code == 200
    metrics = response.json()
    assert len(metrics) > 0
    mero = next((m for m in metrics if m["antibiotic"] == "Meropenem"), None)
    assert mero is not None
    assert mero["total_tested"] >= 8
    assert mero["sensitivity"] >= 90.0
    assert mero["concordance_rate"] >= 85.0
    assert "confusion_matrix" in mero

