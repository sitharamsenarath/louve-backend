from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services.product import ProductService
from app.dependencies import db

router = APIRouter()
service = ProductService()

@router.get("/products", response_model=List[ProductOut])
def get_all_products(db: Session = Depends(db.get_db)):
    return service.get_all_products(db)

@router.get("/products/active", response_model=List[ProductOut])
def get_all_products_active(db: Session = Depends(db.get_db)):
    return service.get_all_products_active(db)

@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(db.get_db)):
    product = service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products/bycategory/{category_id}", response_model=List[ProductOut])
def get_products_by_category(category_id: int, db: Session = Depends(db.get_db)):
    products = service.get_products_by_category(db, category_id)
    return products

@router.get("/products/bycategory/active/{category_id}", response_model=List[ProductOut])
def get_products_by_category_active(category_id: int, db: Session = Depends(db.get_db)):
    products = service.get_products_by_category_active(db, category_id)
    return products

@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(product_in: ProductCreate, db: Session = Depends(db.get_db)):
    return service.create_product(db, product_in)

@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(db.get_db)):
    updated_product = service.update_product(db, product_id, product_in)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(db.get_db)):
    success = service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return
