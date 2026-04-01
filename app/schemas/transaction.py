from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="The amount must be greater than 0")
    type: TransactionType
    category: str = Field(..., min_length=1)
    date: Optional[datetime] = None
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    category_totals: dict
    monthly_summary: list
    recent_activity: list[Transaction]
