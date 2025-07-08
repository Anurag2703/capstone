def test_gita_recommendation(client):
    data = {"student_id": "student789", "sentiment": "negative"}
    response = client.post("/gita/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "verse" in result
    assert isinstance(result["chapter"], int)