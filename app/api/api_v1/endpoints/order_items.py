from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.order_item import OrderItemCreate, OrderItemOut
from app.services.order_item import OrderItemService
from app.dependencies import db

router = APIRouter()
service = OrderItemService()

@router.get("/order-items/{order_item_id}", response_model=OrderItemOut)
def get_order_item(order_item_id: int, db: Session = Depends(db.get_db)):
    order_item = service.get_order_item(db, order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item

@router.post("/order-items", response_model=OrderItemOut, status_code=201)
def create_order_item(order_item_in: OrderItemCreate, db: Session = Depends(db.get_db)):
    return service.create_order_item(db, order_item_in)

@router.delete("/order-items/{order_item_id}", status_code=204)
def delete_order_item(order_item_id: int, db: Session = Depends(db.get_db)):
    success = service.delete_order_item(db, order_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order item not found")
    return
