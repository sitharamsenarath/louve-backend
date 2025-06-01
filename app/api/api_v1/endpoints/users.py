from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user import UserService
from app.dependencies import db

router = APIRouter()
service = UserService()

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(db.get_db)):
    user = service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=List[UserOut])
def get_all_users(db: Session = Depends(db.get_db)):
    # Assuming you add a get_all() method to UserCRUD and UserService
    return service.crud.get_all(db)

@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(db.get_db)):
    existing_user = service.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(db, user_in)

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(db.get_db)):
    user = service.update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/authenticate")
def authenticate_user(email: str, password: str, db: Session = Depends(db.get_db)):
    user = service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Usually you'd return a JWT token here; for now just return user info:
    return {"user_id": user.id, "email": user.email, "name": user.name}
