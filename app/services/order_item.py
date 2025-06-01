from typing import Optional
from sqlalchemy.orm import Session
from app.crud.order_item import OrderItemCRUD
from app.schemas.order_item import OrderItemCreate
from app.models.order_item import OrderItem

class OrderItemService:
    def __init__(self):
        self.crud = OrderItemCRUD()

    def get_order_item(self, db: Session, order_item_id: int) -> Optional[OrderItem]:
        return self.crud.get(db, order_item_id)

    def create_order_item(self, db: Session, order_item_in: OrderItemCreate) -> OrderItem:
        return self.crud.create(db, order_item_in)

    def delete_order_item(self, db: Session, order_item_id: int) -> bool:
        order_item = self.get_order_item(db, order_item_id)
        if not order_item:
            return False
        self.crud.remove(db, order_item_id)
        return True
