from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    cart_items,
    categories,
    order_items,
    orders,
    products,
    users,
)

router = APIRouter()
router.include_router(cart_items.router, tags=["cart"])
router.include_router(categories.router, tags=["category"])
router.include_router(order_items.router, tags=["order-items"])
router.include_router(orders.router, tags=["orders"])
router.include_router(products.router, tags=["products"])
router.include_router(users.router, tags=["users"])
