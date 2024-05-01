from fastapi import APIRouter

from app.api.routers import (
    customers,
)

api_router = APIRouter()

# api_router.include_router(app.router, prefix="/app", tags=["app"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
