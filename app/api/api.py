from fastapi import APIRouter

from app.api.routers import customers, stripe

api_router = APIRouter()

# api_router.include_router(app.router, prefix="/app", tags=["app"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(stripe.router, prefix="/stripe", tags=["stripe"])
