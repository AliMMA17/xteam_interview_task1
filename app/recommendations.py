from sqlalchemy.orm import Session
from .models import Product, PurchaseHistory
from .cache import get_cache, set_cache  # Import Redis caching functions
from typing import List

def get_user_purchase_history(db: Session, user_id: int) -> List[str]:
    # Fetch categories of products the user has purchased
    purchased_products = db.query(Product.category).join(PurchaseHistory).filter(
        PurchaseHistory.user_id == user_id
    ).distinct().all()
    
    return [p[0] for p in purchased_products]

def get_recommendations(db: Session, user_id: int) -> List[Product]:
    cache_key = f"recommendations:{user_id}"
    cached_result = get_cache(cache_key)
    
    if cached_result:
        print(f"Returning cached recommendations for user {user_id}")
        return cached_result  # Return cached recommendations

    # Fetch user purchase history
    user_categories = get_user_purchase_history(db, user_id)

    # Query recommended products
    recommended_products = db.query(Product).filter(
        Product.category.in_(user_categories)
    ).order_by(Product.rating.desc()).limit(5).all()

    # Convert to dict for caching
    result = [{"id": p.id, "name": p.name, "category": p.category, 
              "price": p.price, "rating": p.rating} for p in recommended_products]

    set_cache(cache_key, result)
    return recommended_products
