from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.product import ProductCRUD
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product

class ProductService:
    def __init__(self):
        self.crud = ProductCRUD()

    def get_product(self, db: Session, product_id: int) -> Optional[Product]:
        return self.crud.get(db, product_id)

    def get_all_products(self, db: Session) -> List[Product]:
        return self.crud.get_all(db)

    def create_product(self, db: Session, product_in: ProductCreate) -> Product:
        return self.crud.create(db, product_in)

    def update_product(self, db: Session, product_id: int, product_in: ProductUpdate) -> Optional[Product]:
        product = self.get_product(db, product_id)
        if not product:
            return None
        return self.crud.update(db, product, product_in)

    def delete_product(self, db: Session, product_id: int) -> bool:
        product = self.get_product(db, product_id)
        if not product:
            return False
        self.crud.remove(db, product_id)
        return True
