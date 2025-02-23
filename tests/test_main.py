from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app  
from schemas import OrderResponse

client = TestClient(app)

def test_create_order():
    """Test order creation (route functionality)"""
    with patch("main.db.add") as mock_add, patch("main.db.commit") as mock_commit, patch("main.db.refresh") as mock_refresh:
        response = client.post(
            "/orders/",
            json={"symbol": "AAPL", "price": 150.0, "quantity": 10, "order_type": "buy"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert data["price"] == 150.0
        assert data["quantity"] == 10
        assert data["order_type"] == "buy"
        assert "id" in data 

        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once()

def test_get_orders():
    """Test fetching orders (route functionality)"""
    fake_orders = [
        OrderResponse(id=1, symbol="AAPL", price=150.0, quantity=10, order_type="buy"),
        OrderResponse(id=2, symbol="GOOG", price=2500.0, quantity=5, order_type="sell"),
    ]

    with patch("main.db.query") as mock_query:
        mock_query.return_value.all.return_value = fake_orders

        response = client.get("/orders/")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["symbol"] == "AAPL"
        assert data[1]["symbol"] == "GOOG"