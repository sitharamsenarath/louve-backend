from fastapi import APIRouter, Body, Depends, HTTPException, Header, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies.firebase_auth import verify_firebase_token
from app.schemas.auth import FirebaseSyncRequest
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user import UserService
from app.dependencies import db

from firebase_admin import auth as firebase_auth

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

@router.post("/users/firebase-sync", response_model=dict)
def sync_firebase_user(
    request: FirebaseSyncRequest = Body(...),
    db: Session = Depends(db.get_db),
    decoded_token: dict = Depends(verify_firebase_token),
):
    email = decoded_token["email"]
    name = request.name or decoded_token.get("name") or "User"
    provider = "firebase"

    existing_user = service.get_user_by_email(db, email)
    if existing_user:
        return {"message": "User already exists"}

    service.crud.create(db, UserCreate(email=email, name=name, provider=provider))
    return {"message": "User created"}