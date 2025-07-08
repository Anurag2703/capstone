def test_burnout_prediction(client):
    data = {
        "student_id": "student123",
        "login_frequency": 2,
        "forum_activity": 1,
        "assignment_delay_days": 3,
        "missed_classes": 4
    }
    response = client.post("/burnout/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "risk_score" in result
    assert "risk_level" in result