from pydantic import BaseModel
from typing import Optional
class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    rating: float

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Updated from 'orm_mode' to 'from_attributes'

class ProductResponse(ProductBase):
    id: int  # Include the ID in the response

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    rating: Optional[float] = None  # Optional rating

class PurchaseHistoryBase(BaseModel):
    user_id: int
    product_id: int

class PurchaseHistoryCreate(PurchaseHistoryBase):
    pass

class PurchaseHistoryResponse(PurchaseHistoryBase):
    id: int  # Include ID in response

    class Config:
        from_attributes = True