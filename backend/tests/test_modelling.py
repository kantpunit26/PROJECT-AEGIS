def test_seir_simulation(client):
    payload = {
        "total_population": 1000.0,
        "initial_susceptible": 990.0,
        "initial_colonized": 8.0,
        "initial_infected": 2.0,
        "initial_recovered": 0.0,
        "beta_transmission": 0.30,
        "simulation_days": 60,
        "time_step": 0.5
    }
    response = client.post("/api/v1/modelling/seir/simulate", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["r0"] > 1.0
    assert len(res["days"]) > 50
    assert len(res["infected"]) == len(res["days"])
    assert res["peak_infected_count"] >= 2.0

