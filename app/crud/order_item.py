from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate

class OrderItemCRUD:
    def get(self, db: Session, order_item_id: int) -> Optional[OrderItem]:
        return db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    def get_all_by_order(self, db: Session, order_id: int) -> List[OrderItem]:
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    def create(self, db: Session, order_item_in: OrderItemCreate) -> OrderItem:
        order_item = OrderItem(**order_item_in.model_dump())
        db.add(order_item)
        db.commit()
        db.refresh(order_item)
        return order_item

    def delete(self, db: Session, order_item: OrderItem) -> None:
        db.delete(order_item)
        db.commit()
