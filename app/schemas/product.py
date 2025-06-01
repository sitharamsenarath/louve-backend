from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.schemas.category import CategoryOut

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    stock: int
    category_id: Optional[int] = None
    is_active: Optional[bool] = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    stock: Optional[int]
    category_id: Optional[int]
    is_active: Optional[bool]

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    category: Optional[CategoryOut]

    class Config:
        from_attributes = True

