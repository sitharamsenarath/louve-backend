from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.services.category import CategoryService
from app.dependencies import db

router = APIRouter()
service = CategoryService()

@router.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(db.get_db)):
    category = service.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/categories", response_model=List[CategoryOut])
def get_all_categories(db: Session = Depends(db.get_db)):
    return service.get_all_categories(db)

@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(category_in: CategoryCreate, db: Session = Depends(db.get_db)):
    return service.create_category(db, category_in)

@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(db.get_db)):
    updated_category = service.update_category(db, category_id, category_in)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(db.get_db)):
    success = service.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return
