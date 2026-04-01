from fastapi import APIRouter
from app.api.endpoints import login, users, transactions, dashboard

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
