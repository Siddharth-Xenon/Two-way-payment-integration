from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.customers import Customer
from app.api.utils.customer_utils import (
    save_customer_to_db,
    fetch_all_customers,
    fetch_customer_by_id,
    update_customer_in_db,
    delete_customer_in_db,
)
from app.db.db import SessionLocal


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_customer(customer: Customer, db: Session):
    """
    Process customer data and save to the database
    """
    customer_dict = customer.dict()
    return save_customer_to_db(customer_dict, db)


async def get_customers(db: Session) -> list[Customer]:
    """
    Fetch all customers from the database
    """
    return fetch_all_customers(db)


async def update_customer(customer_id: str, update_data: dict, db: Session):
    """
    Update customer data in the database
    """
    customer = fetch_customer_by_id(customer_id, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in update_data.items():
        setattr(customer, key, value)
    return update_customer_in_db(customer, db)


async def delete_customer(customer_id: str, db: Session):
    """
    Delete a customer from the database
    """
    customer = fetch_customer_by_id(customer_id, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {
        "message": f"Customer deleted successfully",
        "customer": delete_customer_in_db(customer, db),
    }
