# from fastapi import HTTPException
from app.kafka.producer import OutgoingProducer
import stripe
from app.api.utils.stripe_utils import process_stripe_customer
from app.api.utils.customer_utils import fetch_customer_by_id
from app.db.db import SessionLocal

producer = OutgoingProducer()


async def process_stripe_event(event: stripe.Event):
    """
    Process stripe event and handle database operations abstractly.
    """
    # Handle the event
    if event["type"] == "customer.created":
        data = await process_stripe_customer(event["data"]["object"])
        db = SessionLocal()
        try:
            existing_customer = fetch_customer_by_id(data["id"], db)
            if existing_customer:
                print("Customer already exists in database")
            else:
                producer.write_to_topic("stripe_incoming", "create", data)
        except Exception as e:
            print(e)
        finally:
            db.close()

    elif event["type"] == "customer.updated":
        print("Customer Updated")
        data = await process_stripe_customer(event["data"]["object"])
        print(data)
        producer.write_to_topic("stripe_incoming", "update", data)

    elif event["type"] == "customer.deleted":
        print("Customer Deleted")
        data = await process_stripe_customer(event["data"]["object"])
        print(data)
        producer.write_to_topic("stripe_incoming", "delete", data)

    else:
        print("Unhandled event type:", event["type"])
