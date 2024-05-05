from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.kafka.producer import OutgoingProducer
from app.models.customers import Customer, CustomerInfo
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
    Process customer data, save to the database, and send a Kafka message
    """

    customer_dict = customer.dict()
    result = save_customer_to_db(customer_dict, db)
    if result:
        OutgoingProducer().write_to_topic("create", result)

    return result


async def get_customers(db: Session) -> list[CustomerInfo]:
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
    result = update_customer_in_db(customer, db)
    if result:
        OutgoingProducer().write_to_topic("update", result)
    return result


async def delete_customer(customer_id: str, db: Session):
    """
    Delete a customer from the database
    """
    customer = fetch_customer_by_id(customer_id, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    OutgoingProducer().write_to_topic("delete", customer)
    return {
        "message": "Customer deleted successfully",
        "customer": delete_customer_in_db(customer, db),
    }
