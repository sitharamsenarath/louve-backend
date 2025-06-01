from typing import List, Optional
from sqlalchemy.orm import Session
from decimal import Decimal
from app.crud.order import OrderCRUD
from app.crud.order_item import OrderItemCRUD
from app.crud.product import ProductCRUD
from app.schemas.order import OrderCreate, OrderUpdate
from app.models.order import Order

class OrderService:
    def __init__(self):
        self.order_crud = OrderCRUD()
        self.order_item_crud = OrderItemCRUD()
        self.product_crud = ProductCRUD()

    def get_order(self, db: Session, order_id: int) -> Optional[Order]:
        return self.order_crud.get(db, order_id)

    def get_orders_by_user(self, db: Session, user_id: int) -> List[Order]:
        return self.order_crud.get_by_user(db, user_id)

    def create_order(self, db: Session, user_id: int, items: List[dict]) -> Order:
        """
        Create an order with items.

        `items` is a list of dicts with keys:
        - product_id
        - quantity
        """
        total_amount = Decimal(0)
        order_items_data = []

        # Calculate total and prepare order items
        for item in items:
            product = self.product_crud.get(db, item["product_id"])
            if not product or product.stock < item["quantity"]:
                raise ValueError(f"Product {item['product_id']} unavailable or insufficient stock")

            price_at_purchase = product.price
            total_amount += price_at_purchase * item["quantity"]

            order_items_data.append({
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price_at_purchase": price_at_purchase,
            })

        # Create the order
        order_in = OrderCreate(user_id=user_id, total_amount=total_amount)
        order = self.order_crud.create(db, order_in)

        # Create order items and update product stock
        for oi in order_items_data:
            oi_in = self.order_item_crud.create(db, {
                "order_id": order.id,
                "product_id": oi["product_id"],
                "quantity": oi["quantity"],
                "price_at_purchase": oi["price_at_purchase"],
            })
            product = self.product_crud.get(db, oi["product_id"])
            product.stock -= oi["quantity"]
            self.product_crud.update(db, product, {"stock": product.stock})

        return order

    def update_order(self, db: Session, order_id: int, order_in: OrderUpdate) -> Optional[Order]:
        order = self.get_order(db, order_id)
        if not order:
            return None
        return self.order_crud.update(db, order, order_in)

    def cancel_order(self, db: Session, order_id: int) -> bool:
        order = self.get_order(db, order_id)
        if not order:
            return False
        # Set status to cancelled
        self.order_crud.update(db, order, {"status": "cancelled"})
        # Optionally restore product stock here
        return True
