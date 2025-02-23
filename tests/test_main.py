from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app import app, get_db, Order

mock_db = MagicMock()

def override_get_db():
    """Override the database dependency with a mock"""
    yield mock_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_order():
    """Test order creation without real DB"""
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    response = client.post("/orders/", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["price"] == 150.0
    assert data["quantity"] == 10
    assert data["order_type"] == "buy"

def test_get_orders():
    """Test fetching orders without real DB"""
    fake_order = Order(symbol="AAPL", price=150.0, quantity=10, order_type="buy")
    mock_db.query.return_value.all.return_value = [fake_order]

    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["symbol"] == "AAPL"
    assert data[0]["price"] == 150.0
    assert data[0]["quantity"] == 10
    assert data[0]["order_type"] == "buy"
