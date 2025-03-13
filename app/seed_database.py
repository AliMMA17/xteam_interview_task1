from .database import SessionLocal, engine  # Relative import
from .models import Base, Product, User, PurchaseHistory  # Updated imports
from sqlalchemy.orm import Session
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

# Sample users
USERS = [
    {"name": "Alice"},
    {"name": "Bob"},
    {"name": "Charlie"},
]

def seed_database():
    """Seed the database with sample data"""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Open a database session
    db: Session = SessionLocal()

    try:
        # Check if products already exist
        if db.query(Product).count() == 0:
            for product_data in PRODUCTS:
                product = Product(
                    name=product_data["name"],
                    category=product_data["category"],
                    price=product_data["price"],
                    rating=product_data["rating"]
                )
                db.add(product)
            db.commit()
            print(f"Seeded {len(PRODUCTS)} products.")

        # Check if users already exist
        if db.query(User).count() == 0:
            for user_data in USERS:
                user = User(name=user_data["name"])
                db.add(user)
            db.commit()
            print(f"Seeded {len(USERS)} users.")

        # Check if purchase history exists
        if db.query(PurchaseHistory).count() == 0:
            users = db.query(User).all()
            products = db.query(Product).all()

            # Assign random purchases to each user
            for user in users:
                purchased_products = random.sample(products, k=3)  # Each user buys 3 products
                for product in purchased_products:
                    purchase = PurchaseHistory(user_id=user.id, product_id=product.id)
                    db.add(purchase)

            db.commit()
            print(f"Seeded purchase history for {len(users)} users.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
