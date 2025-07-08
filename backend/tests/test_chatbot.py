def test_chatbot_greeting(client):
    data = {"student_id": "student456", "message": "Hello"}
    response = client.post("/chatbot/", json=data)
    assert response.status_code == 200
    reply = response.json()["reply"]
    assert "Hello" in reply or "help" in reply

def test_chatbot_distress(client):
    data = {"student_id": "student456", "message": "I feel hopeless"}
    response = client.post("/chatbot/", json=data)
    assert response.status_code == 200
    reply = response.json()["reply"]
    assert "sorry" in reply or "support" in reply