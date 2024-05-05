from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.customers import Customer, CustomerInfo
from app.api.controllers.customers import (
    create_customer as create_customer_controller,
    get_customers as get_customers_controller,
    update_customer as update_customer_controller,
    delete_customer as delete_customer_controller,
)
from app.db.db import SessionLocal


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/")
async def create_customer(customer: Customer, db: Session = Depends(get_db)):
    return await create_customer_controller(customer, db=db)


@router.get("/")
async def get_customers(db: Session = Depends(get_db)) -> list[CustomerInfo]:
    return await get_customers_controller(db=db)


@router.patch("/{customer_id}")
async def update_customer(
    customer_id: str, update_data: dict, db: Session = Depends(get_db)
):
    return await update_customer_controller(customer_id, update_data, db=db)


@router.delete("/{customer_id}")
async def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    return await delete_customer_controller(customer_id, db=db)
