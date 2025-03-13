from .database import SessionLocal, engine  # Relative import
from .models import Base, Product          # Relative import
from sqlalchemy.orm import Session         # Explicitly import Session for type hinting
import random

# Sample data for products
PRODUCTS = [
    {"name": "Smartphone X", "category": "electronics", "price": 599.99, "rating": 4.5},
    {"name": "Laptop Pro", "category": "electronics", "price": 1299.99, "rating": 4.7},
    {"name": "Wireless Earbuds", "category": "electronics", "price": 99.99, "rating": 4.3},
    {"name": "Python Programming Book", "category": "books", "price": 29.99, "rating": 4.8},
    {"name": "Sci-Fi Novel", "category": "books", "price": 19.99, "rating": 4.6},
    {"name": "Cookbook Deluxe", "category": "books", "price": 34.99, "rating": 4.4},
    {"name": "T-Shirt", "category": "clothing", "price": 15.99, "rating": 4.2},
    {"name": "Jeans", "category": "clothing", "price": 49.99, "rating": 4.5},
    {"name": "Sneakers", "category": "clothing", "price": 79.99, "rating": 4.6},
    {"name": "Coffee Maker", "category": "appliances", "price": 89.99, "rating": 4.3},
    {"name": "Blender", "category": "appliances", "price": 59.99, "rating": 4.4},
]

def seed_database():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Open a database session
    db: Session = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Product).count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        # Generate and insert products
        for product_data in PRODUCTS:
            product = Product(
                name=product_data["name"],
                category=product_data["category"],
                price=product_data["price"],
                rating=product_data["rating"]
            )
            db.add(product)

        # Commit the transaction
        db.commit()
        print(f"Successfully seeded database with {len(PRODUCTS)} products.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()