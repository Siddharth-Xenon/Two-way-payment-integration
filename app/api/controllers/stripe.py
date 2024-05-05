# from fastapi import HTTPException
import stripe
from app.api.utils.stripe_utils import process_stripe_customer


async def process_stripe_event(event: stripe.Event):
    """
    Process stripe event and handle database operations abstractly.
    """
    # Handle the event
    if event["type"] == "customer.created":
        print("New Customer Created: ")
        data = await process_stripe_customer(event["data"]["object"])
        print(data)
        # producer.writeToTopic("create", data)

    elif event["type"] == "customer.updated":
        print("Customer Updated")
        data = await process_stripe_customer(event["data"]["object"])
        print(data)
        # producer.writeToTopic("update", data)

    elif event["type"] == "customer.deleted":
        print("Customer Deleted")
        data = await process_stripe_customer(event["data"]["object"])
        print(data)
        # producer.writeToTopic("delete", data)

    else:
        print("Unhandled event type:", event["type"])
