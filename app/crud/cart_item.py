from decimal import Decimal
from typing import List, Optional
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart_item import CartItemCreate, CartItemUpdate

    
class CartItemCRUD:
    def get(self, db: Session, cart_item_id: int) -> Optional[CartItem]:
        return db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    def get_all_by_user(self, db: Session, user_id: int) -> List[CartItem]:
        return db.query(CartItem).filter(CartItem.user_id == user_id).all()

    def create(self, db: Session, cart_item_in: CartItemCreate) -> CartItem:
        cart_item = CartItem(**cart_item_in.model_dump())
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

    def update(self, db: Session, cart_item: CartItem, cart_item_in: CartItemUpdate) -> CartItem:
        update_data = cart_item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cart_item, field, value)
        db.commit()
        db.refresh(cart_item)
        return cart_item

    def delete(self, db: Session, cart_item: CartItem) -> None:
        db.delete(cart_item)
        db.commit()

    def calculate_user_active_total(self, db: Session, user_id: int) -> Decimal:
        stmt = (
            select(func.sum(Product.price * CartItem.quantity))
            .join(Product, CartItem.product_id == Product.id)
            .where(CartItem.user_id == user_id, CartItem.is_active == True)
        )
        result = db.execute(stmt).scalar()
        return result or Decimal("0.00")