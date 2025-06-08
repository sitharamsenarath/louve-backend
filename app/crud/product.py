from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from typing import Optional, List


class ProductCRUD:
    def get(self, db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    def get_all(self, db: Session, skip: int = 0) -> List[Product]:
        return db.query(Product).offset(skip).all()
    
    def get_all_active(self, db: Session, skip: int = 0) -> List[Product]:
        return db.query(Product).filter(Product.is_active == True).offset(skip).all()
    
    def get_by_category(self, db: Session, category_id: int) -> List[Product]:
        return db.query(Product).filter(Product.category_id == category_id).all()
    
    def get_by_category_active(self, db: Session, category_id: int) -> List[Product]:
        return db.query(Product).filter(Product.is_active == True).filter(Product.category_id == category_id).all()

    def create(self, db: Session, product_in: ProductCreate) -> Product:
        product_data = product_in.model_dump()
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update(self, db: Session, product: Product, product_in: ProductUpdate) -> Product:
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        return product

    def delete(self, db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()