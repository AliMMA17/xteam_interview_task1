from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .recommendations import get_recommendations
from fastapi import Path
from contextlib import asynccontextmanager
app = FastAPI(title="Product Recommendation System")

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting up the application...")
    models.Base.metadata.create_all(bind=engine)  # Create tables on startup
    yield  # Application runs here
    # Shutdown logic
    print("Shutting down database engine...")
    engine.dispose()


@app.get("/recommendations", response_model=list[schemas.Product])
async def get_product_recommendations(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    recommendations = get_recommendations(db, user_id)
    return recommendations


@app.post("/products/", response_model=schemas.ProductResponse)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product.name,
        category=product.category,
        price=product.price,
        rating=product.rating
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # Get the auto-generated ID
    return new_product  # This will return the new product with the ID


@app.post("/purchase/", response_model=schemas.PurchaseHistoryCreate)
async def add_purchase_history(
    purchase: schemas.PurchaseHistoryCreate, db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == purchase.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = db.query(models.Product).filter(models.Product.id == purchase.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_purchase = models.PurchaseHistory(
        user_id=purchase.user_id,
        product_id=purchase.product_id
    )
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)
    
    return new_purchase

@app.delete("/products/{product_id}", response_model=schemas.ProductResponse)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return product  # Optionally, return the deleted product as confirmation


@app.get("/products/", response_model=list[schemas.ProductResponse])
async def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get("/users/", response_model=list[schemas.UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()