def test_healthcheck(client):
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
