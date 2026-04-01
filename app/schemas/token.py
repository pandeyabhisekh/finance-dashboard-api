from typing import Optional
from pydantic import BaseModel
from app.models.user import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    role: Optional[UserRole] = None
