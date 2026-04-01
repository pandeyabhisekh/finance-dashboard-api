from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.db.session import Base

class TransactionType(str, enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String, index=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(String, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="transactions")
