from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.VIEWER

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
