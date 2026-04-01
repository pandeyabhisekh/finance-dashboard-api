from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_user
from app.models.user import User, UserRole
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user
    """
    return current_user

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.RoleChecker([UserRole.ADMIN])),
) -> Any:
    """
    Retrieve users
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.RoleChecker([UserRole.ADMIN])),
) -> Any:
    """
    Create new user
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return crud_user.create(db, obj_in=user_in)

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.RoleChecker([UserRole.ADMIN])),
) -> Any:
    """
    Update a user
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: str = Body(None),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user
    """
    current_user_data = UserUpdate(
        password=password, full_name=full_name, email=email
    )
    user = crud_user.update(db, db_obj=current_user, obj_in=current_user_data)
    return user
