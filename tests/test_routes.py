from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_latest_price():
    response = client.get("/prices/latest?symbol=AAPL")
    assert response.status_code == 200
    data = response.json()
    assert "symbol" in data
    assert "price" in data
    assert data["symbol"] == "AAPL"
