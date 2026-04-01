from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def get(db: Session, id: int) -> Optional[Transaction]:
    return db.query(Transaction).filter(Transaction.id == id).first()

def get_multi(
    db: Session, 
    owner_id: Optional[int] = None, 
    skip: int = 0, 
    limit: int = 100,
    type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Transaction]:
    query = db.query(Transaction)
    if owner_id:
        query = query.filter(Transaction.owner_id == owner_id)
    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category == category)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    return query.offset(skip).limit(limit).all()

def create_with_owner(
    db: Session, obj_in: TransactionCreate, owner_id: int
) -> Transaction:
    db_obj = Transaction(**obj_in.model_dump(), owner_id=owner_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, db_obj: Transaction, obj_in: TransactionUpdate
) -> Transaction:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, id: int) -> Transaction:
    obj = db.query(Transaction).get(id)
    db.delete(obj)
    db.commit()
    return obj
