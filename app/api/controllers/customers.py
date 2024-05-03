from sqlalchemy.orm import Session
from fastapi import HTTPException
# from app.kafka.producer import kafka_producer
from app.models.customers import Customer
from app.api.utils.stripe_utils import create_stripe_customer
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

    # Send Kafka message
    # producer = kafka_producer()
    # await producer("customer_updates", f"New customer added: {customer_dict}")
    await create_stripe_customer(customer_dict)

    return result

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
        "message": "Customer deleted successfully",
        "customer": delete_customer_in_db(customer, db),
    }
