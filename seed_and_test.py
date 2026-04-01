
import sys
import os
from datetime import datetime, timedelta

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.db.session import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.transaction import Transaction, TransactionType
from app.core.security import get_password_hash
from app.services.dashboard import get_dashboard_summary

def seed_data():
    # Create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Create users
    admin = User(
        full_name="Admin User",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.ADMIN,
        is_active=True
    )
    analyst = User(
        full_name="Analyst User",
        email="analyst@example.com",
        hashed_password=get_password_hash("analyst123"),
        role=UserRole.ANALYST,
        is_active=True
    )
    viewer = User(
        full_name="Viewer User",
        email="viewer@example.com",
        hashed_password=get_password_hash("viewer123"),
        role=UserRole.VIEWER,
        is_active=True
    )
    
    db.add_all([admin, analyst, viewer])
    db.commit()
    db.refresh(admin)
    db.refresh(analyst)
    db.refresh(viewer)
    
    # Create transactions
    t1 = Transaction(
        amount=1000.0,
        type=TransactionType.INCOME,
        category="Salary",
        date=datetime.utcnow() - timedelta(days=5),
        notes="Monthly salary",
        owner_id=admin.id
    )
    t2 = Transaction(
        amount=50.0,
        type=TransactionType.EXPENSE,
        category="Food",
        date=datetime.utcnow() - timedelta(days=3),
        notes="Lunch at restaurant",
        owner_id=admin.id
    )
    t3 = Transaction(
        amount=150.0,
        type=TransactionType.EXPENSE,
        category="Transport",
        date=datetime.utcnow() - timedelta(days=2),
        notes="Monthly pass",
        owner_id=admin.id
    )
    t4 = Transaction(
        amount=500.0,
        type=TransactionType.INCOME,
        category="Freelance",
        date=datetime.utcnow() - timedelta(days=1),
        notes="Small project",
        owner_id=admin.id
    )
    
    db.add_all([t1, t2, t3, t4])
    db.commit()
    
    print("Data seeded successfully!")
    
    # Test dashboard summary
    summary = get_dashboard_summary(db, user_id=None)
    print(f"Summary for Admin (all): {summary}")
    
    summary_user = get_dashboard_summary(db, user_id=admin.id)
    print(f"Summary for Admin (own): {summary_user}")
    
    db.close()

if __name__ == "__main__":
    seed_data()
