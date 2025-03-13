from sqlalchemy.orm import Session
from .models import Product
from .cache import get_cache, set_cache
from typing import List

def get_user_purchase_history(db: Session, user_id: int) -> List[str]:
    # Mock implementation - in real scenario, this would query user purchase history
    # For demo, return some hardcoded categories
    return ["electronics", "books"]

def get_recommendations(db: Session, user_id: int) -> List[Product]:
    cache_key = f"recommendations:{user_id}"
    cached_result = get_cache(cache_key)
    print(f"cached_result {cached_result}" )
    
    if cached_result:
        return cached_result

    # Get user's purchased categories
    user_categories = get_user_purchase_history(db, user_id)
    
    # Query products from same categories
    recommended_products = db.query(Product).filter(
        Product.category.in_(user_categories)
    ).order_by(Product.rating.desc()).limit(5).all()
    
    # Convert to dict for caching
    result = [{"id": p.id, "name": p.name, "category": p.category, 
              "price": p.price, "rating": p.rating} for p in recommended_products]
    
    set_cache(cache_key, result)
    return recommended_products