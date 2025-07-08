def test_sentiment_positive(client):
    data = {"text": "I feel good about my grades"}
    response = client.post("/sentiment/", json=data)
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"

def test_sentiment_negative(client):
    data = {"text": "I feel bad about my grades"}
    response = client.post("/sentiment/", json=data)
    assert response.status_code == 200
    assert response.json()["sentiment"] == "negative"