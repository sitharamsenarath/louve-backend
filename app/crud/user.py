from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCRUD:
    def get(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
    
    def create(self, db: Session, user_in: UserCreate) -> User:
        user_data = user_in.model_dump(exclude={"password"})

        if user_in.password:
            user_data["password_hash"] = hash_password(user_in.password)
        else:
            user_data["password_hash"] = None  # or leave it out if nullable

        user = User(**user_data)
        print("Final user data to create:", user_data)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
