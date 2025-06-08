from typing import Optional
from sqlalchemy.orm import Session
from app.crud.user import UserCRUD
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import hash_password, verify_password  # assuming you have these utils

class UserService:
    def __init__(self):
        self.crud = UserCRUD()

    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        return self.crud.get(db, user_id)

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return self.crud.get_by_email(db, email)

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        hashed_password = hash_password(user_in.password)
        user_data = user_in.model_dump()
        user_data['password_hash'] = hashed_password
        user_data.pop('password', None)
        return self.crud.create(db, user_data)

    def update_user(self, db: Session, user_id: int, user_in: UserUpdate) -> Optional[User]:
        user = self.get_user(db, user_id)
        if not user:
            return None
        return self.crud.update(db, user, user_in)

    def create_firebase_user(self, db: Session, email: str, name: str):
        user_data = UserCreate(email=email, name=name, password="")
        print("Creating Firebase user with name:", name)
        return self.crud.create(db, user_data)