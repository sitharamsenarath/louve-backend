from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional

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

# @router.post("/auth/login")
# async def firebase_login(
#     request: Request,
#     authorization: Optional[str] = Header(None),
#     db: Session = Depends(db.get_db)
# ):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Invalid token format")

#     token = authorization.split(" ")[1]

#     try:
#         decoded = firebase_auth.verify_id_token(token)
#         email = decoded["email"]
#         firebase_name = decoded.get("name", "")
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid Firebase token")

#     body = await request.json()
#     print("Parsed body:", body)
#     body_name = body.get("name", "")

#     name = body_name or firebase_name or email.split("@")[0]

#     print("Body name:", body_name)
#     print("Firebase name:", firebase_name)
#     print("Final name used:", name)

#     user = UserService.get_user_by_email(db, email)
#     if not user:
#         user = UserService.create_firebase_user(db, email=email, name=name)

#     return {
#         "id": user.id,
#         "email": user.email,
#         "name": user.name,
#         "provider": user.provider
#     }