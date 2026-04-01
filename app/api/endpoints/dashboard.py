from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, UserRole
from app.services import dashboard
from app.schemas.transaction import DashboardSummary

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get dashboard summary for current user
    """
    # If the user is an Admin or Analyst, they can see the whole summary
    user_id = None if current_user.role in [UserRole.ADMIN, UserRole.ANALYST] else current_user.id
    return dashboard.get_dashboard_summary(db=db, user_id=user_id)
