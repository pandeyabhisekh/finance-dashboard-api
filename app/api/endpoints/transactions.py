from datetime import datetime
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_transaction
from app.models.transaction import TransactionType
from app.models.user import User, UserRole
from app.schemas.transaction import Transaction as TransactionSchema, TransactionCreate, TransactionUpdate

router = APIRouter()

@router.get("/", response_model=List[TransactionSchema])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.ANALYST, UserRole.VIEWER])),
) -> Any:
    """
    Retrieve transactions
    """
    # If the user is an Admin or Analyst, they can see all transactions (optional logic)
    # For now, let's keep it restricted to own data unless the requirement says otherwise.
    # The requirement says Viewer "Can only view dashboard data", Analyst "Can view records and access insights".
    # This usually means seeing all transactions in a finance dashboard scenario.
    
    owner_id = None if current_user.role in [UserRole.ADMIN, UserRole.ANALYST] else current_user.id
    
    transactions = crud_transaction.get_multi(
        db=db, 
        owner_id=owner_id, 
        skip=skip, 
        limit=limit,
        type=type,
        category=category,
        start_date=start_date,
        end_date=end_date
    )
    return transactions

@router.post("/", response_model=TransactionSchema)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: TransactionCreate,
    current_user: User = Depends(deps.RoleChecker([UserRole.ADMIN])),
) -> Any:
    """
    Create new transaction
    """
    transaction = crud_transaction.create_with_owner(
        db=db, obj_in=transaction_in, owner_id=current_user.id
    )
    return transaction

@router.put("/{id}", response_model=TransactionSchema)
def update_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    transaction_in: TransactionUpdate,
    current_user: User = Depends(deps.RoleChecker([UserRole.ADMIN])),
) -> Any:
    """
    Update a transaction
    """
    transaction = crud_transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if transaction.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    transaction = crud_transaction.update(db=db, db_obj=transaction, obj_in=transaction_in)
    return transaction

@router.delete("/{id}", response_model=TransactionSchema)
def delete_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.RoleChecker([UserRole.ADMIN])),
) -> Any:
    """
    Delete a transaction
    """
    transaction = crud_transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if transaction.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    transaction = crud_transaction.remove(db=db, id=id)
    return transaction
