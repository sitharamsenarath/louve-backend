from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from app.schemas.order_item import OrderItemOut

class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderBase(BaseModel):
    user_id: int
    total_amount: Decimal
    status: Optional[OrderStatus] = OrderStatus.pending

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    total_amount: Optional[Decimal] = None

class OrderOut(OrderBase):
    id: int
    created_at: datetime
    order_items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
