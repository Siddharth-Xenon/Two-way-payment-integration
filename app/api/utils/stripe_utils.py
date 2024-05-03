import stripe
from fastapi import HTTPException
from app.core.config import StripeConfig
# from app.models.customers import CustomerDB

stripe.api_key = StripeConfig.STRIPE_API_KEY


def create_stripe_customer(customer_data: dict):
    """
    Asynchronously create a customer on Stripe.

    Args:
    customer_data (dict): Dictionary containing customer data.

    Returns:
    stripe.Customer: The created Stripe customer object.
    """
    try:
        stripe_customer = stripe.Customer.create(**customer_data)
        return stripe_customer
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


def retrieve_stripe_customer(stripe_customer_id: str):
    """
    Retrieve a customer from Stripe.

    Args:
    stripe_customer_id (str): Stripe customer ID.

    Returns:
    dict: Stripe customer data.
    """
    try:
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
        return stripe_customer
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=404, detail=str(e))


def update_stripe_customer(stripe_customer_id: str, update_data: dict):
    """
    Update a customer on Stripe.

    Args:
    stripe_customer_id (str): Stripe customer ID.
    update_data (dict): Dictionary containing data to update.

    Returns:
    dict: Updated Stripe customer data.
    """
    try:
        stripe_customer = stripe.Customer.modify(stripe_customer_id, **update_data)
        return stripe_customer
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_stripe_customer(stripe_customer_id: str):
    """
    Delete a customer from Stripe.

    Args:
    stripe_customer_id (str): Stripe customer ID.

    Returns:
    dict: Stripe deletion confirmation.
    """
    try:
        stripe_customer = stripe.Customer.delete(stripe_customer_id)
        return stripe_customer
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
