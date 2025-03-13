from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .recommendations import get_recommendations

app = FastAPI(title="Product Recommendation System")

models.Base.metadata.create_all(bind=engine)

@app.get("/recommendations", response_model=list[schemas.Product])
async def get_product_recommendations(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    recommendations = get_recommendations(db, user_id)
    return recommendations