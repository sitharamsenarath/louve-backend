from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    is_admin: Optional[bool] = False

class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = ""
    name: Optional[str] = ""

class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None
    password: Optional[str] = None  # Firebase users won’t have this
    provider: Optional[str] = "firebase"

class UserUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
