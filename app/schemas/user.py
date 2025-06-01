from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    password: str  # plain password for creation only

class UserUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
