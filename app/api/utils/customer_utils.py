import stripe
import json
from fastapi import HTTPException
from confluent_kafka import Consumer, KafkaError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app.models.customers import CustomerDB, CustomerInfo
from app.db.db import SessionLocal


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_customer_to_db(customer_data: dict, db: Session) -> dict:
    """
    Save a new customer to the database using SQLAlchemy session.

    Args:
    db (Session): SQLAlchemy session object to handle transactions.
    customer_data (dict): Dictionary containing customer data.

    Returns:
    dict: Dictionary representation of the newly created customer database object.
    """

    try:
        new_customer = CustomerDB(**customer_data)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to save customer: {str(e)}"
        )

    return {
        "id": new_customer.id,
        "name": new_customer.name,
        "email": new_customer.email,
    }


def fetch_all_customers(db: Session) -> list[CustomerInfo]:
    """
    Fetch all customers from the database using SQLAlchemy session.

    Args:
    db (Session): SQLAlchemy session object to handle transactions.

    Returns:
    list[CustomerInfo]: List of all customer database objects.
    """

    return db.query(CustomerDB).all()


def fetch_customer_by_id(customer_id: str, db: Session) -> dict:
    """
    Fetch a customer by ID from the database using SQLAlchemy session and return as a dictionary.

    Args:
    db (Session): SQLAlchemy session object to handle transactions.
    customer_id (str): ID of the customer to fetch.

    Returns:
    dict: Dictionary representation of the customer database object.
    """

    customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if customer:
        return {"id": customer.id, "name": customer.name, "email": customer.email}
    return {}


def update_customer_in_db(customer: dict, db: Session) -> dict:
    """
    Update a customer in the database using SQLAlchemy session.

    Args:
    db (Session): SQLAlchemy session object to handle transactions.
    customer (CustomerDB): The customer database object to update.

    Returns:
    CustomerDB: The updated customer database object.
    """

    try:
        db.commit()
        db.refresh(customer)
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, UniqueViolation):
            error_message = f"Failed to update customer with ID {customer.id}: Email {customer.email} already exists."
        else:
            error_message = (
                f"Failed to update customer with ID {customer.id}: {str(e.orig)}"
            )
        raise HTTPException(status_code=400, detail=error_message)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update customer with ID {customer.id}: {str(e)}",
        )

    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
    }


def delete_customer_in_db(customer: CustomerDB, db: Session):
    """
    Delete a customer from the database using SQLAlchemy session.

    Args:
    db (Session): SQLAlchemy session object to handle transactions.
    customer (CustomerDB): The customer database object to delete.

    Returns:
    CustomerDB: The deleted customer database object.
    """

    try:
        db.delete(customer)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete customer with ID {customer.id}: {str(e)}",
        )

    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
    }


def update_stripe_customer():
    # Consumer configuration
    conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "stripe-sync-group",
        "auto.offset.reset": "earliest",
    }

    # Create Consumer instance
    consumer = Consumer(**conf)
    consumer.subscribe(["customer_updates"])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(
                        "End of partition reached {0}/{1}".format(
                            msg.topic(), msg.partition()
                        )
                    )
                else:
                    print(msg.error())
                continue

            # Message processing
            customer_data = json.loads(msg.value().decode("utf-8"))
            stripe.Customer.modify(**customer_data)
    finally:
        consumer.close()
