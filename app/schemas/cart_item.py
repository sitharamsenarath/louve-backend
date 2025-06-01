from typing import Optional
from pydantic import BaseModel

class CartItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1
    is_active: Optional[bool] = True

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None  # Allow partial updates

    class Config:
        from_attributes = True

class CartItemOut(CartItemBase):
    id: int

    class Config:
        from_attributes = True
