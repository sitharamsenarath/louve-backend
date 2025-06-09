from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.cart_item import CartItemCreate, CartItemReceive, CartItemUpdate, CartItemOut
from app.schemas.order_item import OrderItemCreate
from app.services.cart_item import CartItemService
from app.services.user import UserService
from app.dependencies import db

router = APIRouter()
service = CartItemService()

@router.get("/cart/items/{item_id}", response_model=CartItemOut)
def get_cart_item(item_id: int, db: Session = Depends(db.get_db)):
    item = service.get_cart_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item

@router.get("/cart/user/{user_id}/items", response_model=List[CartItemOut])
def get_user_cart_items(user_id: int, only_active: bool = False, db: Session = Depends(db.get_db)):
    return service.get_user_cart_items(db, user_id, only_active)

@router.post("/cart/items", response_model=CartItemOut, status_code=201)
def add_to_cart(item_in: CartItemReceive, db: Session = Depends(db.get_db)):
    try:
        return service.add_to_cart_from_receive(db, item_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/cart/items/{item_id}", response_model=CartItemOut)
def update_cart_item(item_id: int, item_in: CartItemUpdate, db: Session = Depends(db.get_db)):
    updated_item = service.update_cart_item(db, item_id, item_in)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_item

@router.delete("/cart/items/{item_id}", status_code=204)
def remove_cart_item(item_id: int, db: Session = Depends(db.get_db)):
    service.remove_cart_item(db, item_id)
    return

@router.get("/cart/user/{user_id}/total", response_model=float)
def calculate_cart_total(user_id: int, db: Session = Depends(db.get_db)):
    total = service.calculate_cart_total(db, user_id)
    return float(total)
