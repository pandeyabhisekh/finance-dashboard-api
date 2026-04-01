from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base

class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    ANALYST = "Analyst"
    VIEWER = "Viewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(Enum(UserRole), default=UserRole.VIEWER)

    transactions = relationship("Transaction", back_populates="owner")
