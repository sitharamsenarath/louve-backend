from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.category import CategoryCRUD
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category

class CategoryService:
    def __init__(self):
        self.crud = CategoryCRUD()

    def get_category(self, db: Session, category_id: int) -> Optional[Category]:
        return self.crud.get(db, category_id)

    def get_all_categories(self, db: Session) -> List[Category]:
        return self.crud.get_all(db)

    def create_category(self, db: Session, category_in: CategoryCreate) -> Category:
        return self.crud.create(db, category_in)

    def update_category(self, db: Session, category_id: int, category_in: CategoryUpdate) -> Optional[Category]:
        category = self.get_category(db, category_id)
        if not category:
            return None
        return self.crud.update(db, category, category_in)

    def delete_category(self, db: Session, category_id: int) -> bool:
        category = self.get_category(db, category_id)
        if not category:
            return False
        self.crud.remove(db, category_id)
        return True
