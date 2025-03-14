# test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Absolute import from app package
from app.database import Base, get_db  # Absolute import from app package
from app.models import Product  # Absolute import from app package
from app.schemas import Product as ProductSchema  # Absolute import from app package
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database URL (using an in-memory SQLite database for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a test client
client = TestClient(app)

# Override the database dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def setup_database():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables after tests
    Base.metadata.drop_all(bind=engine)

def test_get_recommendations_valid_user(setup_database):
    response = client.get("/recommendations?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_recommendations_invalid_user(setup_database):
    response = client.get("/recommendations?user_id=0")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid user ID"

def test_get_recommendations_negative_user(setup_database):
    response = client.get("/recommendations?user_id=-1")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid user ID"

@pytest.fixture
def mock_db_with_data():
    db = TestingSessionLocal()
    product1 = Product(
        id=1,
        name="Test Product 1",
        category="Electronics",
        price=99.99,
        rating=4.5
    )
    product2 = Product(
        id=2,
        name="Test Product 2",
        category="Electronics",
        price=49.99,
        rating=4.0
    )
    db.add(product1)
    db.add(product2)
    db.commit()
    yield db
    db.close()

def test_get_recommendations_with_data(setup_database, mock_db_with_data):
    response = client.get("/recommendations?user_id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    if data:
        assert "id" in data[0]
        assert "name" in data[0]
        assert "category" in data[0]
        assert "price" in data[0]
        assert "rating" in data[0]
        if len(data) > 1:
            assert data[0]["rating"] >= data[1]["rating"]