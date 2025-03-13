import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
from app.models import Product

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_get_recommendations(client, test_db):
    # Add sample products
    products = [
        Product(name="Phone", category="electronics", price=599.99, rating=4.5),
        Product(name="Book", category="books", price=29.99, rating=4.8),
    ]
    test_db.add_all(products)
    test_db.commit()

    response = client.get("/recommendations?user_id=1")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert all(p["category"] in ["electronics", "books"] for p in response.json())

def test_invalid_user_id(client):
    response = client.get("/recommendations?user_id=-1")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid user ID"