from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import DashboardSummary

def get_dashboard_summary(db: Session, user_id: Optional[int] = None) -> DashboardSummary:
    query = db.query(Transaction)
    if user_id:
        query = query.filter(Transaction.owner_id == user_id)

    # Total Income
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == TransactionType.INCOME
    )
    if user_id:
        total_income = total_income.filter(Transaction.owner_id == user_id)
    total_income = total_income.scalar() or 0.0

    # Total Expense
    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == TransactionType.EXPENSE
    )
    if user_id:
        total_expense = total_expense.filter(Transaction.owner_id == user_id)
    total_expense = total_expense.scalar() or 0.0

    # Net Balance
    net_balance = total_income - total_expense

    # Category Totals
    category_totals = {}
    categories_query = db.query(
        Transaction.category,
        func.sum(Transaction.amount)
    )
    if user_id:
        categories_query = categories_query.filter(Transaction.owner_id == user_id)
    
    categories = categories_query.group_by(Transaction.category).all()
    
    for cat, total in categories:
        category_totals[cat] = total

    # Monthly Summary (Last 6 months)
    monthly_summary = []
    current_date = datetime.utcnow()
    for i in range(5, -1, -1):
        # Calculate the first day of the month i months ago
        year = current_date.year
        month = current_date.month - i
        while month <= 0:
            month += 12
            year -= 1
        
        start_date = datetime(year, month, 1)
        # Next month
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1
        end_date = datetime(next_year, next_month, 1)
        
        month_income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.type == TransactionType.INCOME,
            Transaction.date >= start_date,
            Transaction.date < end_date
        )
        if user_id:
            month_income = month_income.filter(Transaction.owner_id == user_id)
            
        month_expense = db.query(func.sum(Transaction.amount)).filter(
            Transaction.type == TransactionType.EXPENSE,
            Transaction.date >= start_date,
            Transaction.date < end_date
        )
        if user_id:
            month_expense = month_expense.filter(Transaction.owner_id == user_id)

        monthly_summary.append({
            "month": start_date.strftime("%B"),
            "income": month_income.scalar() or 0.0,
            "expense": month_expense.scalar() or 0.0
        })

    # Recent Activity
    recent_activity = query.order_by(Transaction.date.desc()).limit(5).all()
    
    return DashboardSummary(
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        category_totals=category_totals,
        monthly_summary=monthly_summary,
        recent_activity=recent_activity
    )
