from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import db
from app.schemas.order import OrderOut, OrderUpdate
from app.services.order import OrderService

router = APIRouter()
service = OrderService()

@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(db.get_db)):
    order = service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders/user/{user_id}", response_model=List[OrderOut])
def get_user_orders(user_id: int, db: Session = Depends(db.get_db)):
    return service.get_orders_by_user(db, user_id)

@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(user_id: int, items: List[dict], db: Session = Depends(db.get_db)):
    """
    `items` should be a list of dicts like:
    [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1}
    ]
    """
    try:
        return service.create_order(db, user_id, items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_in: OrderUpdate, db: Session = Depends(db.get_db)):
    order = service.update_order(db, order_id, order_in)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders/{order_id}/cancel", status_code=204)
def cancel_order(order_id: int, db: Session = Depends(db.get_db)):
    success = service.cancel_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found or already cancelled")
    return
