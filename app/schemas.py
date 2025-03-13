from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    rating: float

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Updated from 'orm_mode' to 'from_attributes'