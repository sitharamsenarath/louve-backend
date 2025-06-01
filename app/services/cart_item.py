from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
from decimal import Decimal

from app.models.cart_item import CartItem
from app.schemas.cart_item import CartItemCreate, CartItemUpdate
from app.crud.cart_item import CartItemCRUD


class CartItemService:
    def __init__(self):
        self.crud = CartItemCRUD()

    def get_cart_item(self, db: Session, item_id: int) -> Optional[CartItem]:
        return self.crud.get(db, item_id)

    def get_user_cart_items(self, db: Session, user_id: int, only_active: bool = False) -> List[CartItem]:
        query = select(CartItem).where(CartItem.user_id == user_id)
        if only_active:
            query = query.where(CartItem.is_active == True)
        return db.scalars(query).all()

    def add_to_cart(self, db: Session, item_in: CartItemCreate) -> CartItem:
        return self.crud.create(db, item_in)

    def update_cart_item(self, db: Session, item_id: int, item_in: CartItemUpdate) -> Optional[CartItem]:
        cart_item = self.get_cart_item(db, item_id)
        if not cart_item:
            return None
        return self.crud.update(db, cart_item, item_in)

    def remove_cart_item(self, db: Session, item_id: int) -> None:
        self.crud.remove(db, item_id)

    def calculate_cart_total(self, db: Session, user_id: int) -> Decimal:
        return self.crud.calculate_user_active_total(db, user_id)
