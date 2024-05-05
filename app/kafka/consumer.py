import json
from confluent_kafka import Consumer, KafkaError
import stripe
from app.db.db import SessionLocal


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OutgoingConsumer:
    kafka_server = "localhost:9092"

    topic = "stripe_outgoing"

    def __init__(self):
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.kafka_server,
                "group.id": "stripe-group",
                "auto.offset.reset": "latest",
                "enable.auto.commit": False,
            }
        )
        self.consumer.subscribe([self.topic])

    def sync(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break

                data = json.loads(msg.value().decode("utf-8"))
                customer = data["Customer"]
                id = customer["id"]
                name = customer.get("name")
                email = customer.get("email")

                if data["method"] == "create":
                    stripeCustomer = stripe.Customer.create(
                        id=id, email=email, name=name
                    )
                    print(
                        f"Stripe customer created name: {stripeCustomer.name}, email: {stripeCustomer.email}"
                    )

                    # customer = Customer(**stripeCustomer)
                    # update_customer_in_db(customer.dict, db= db)

                elif data["method"] == "update":
                    update_fields = {}
                    if email is not None:
                        update_fields["email"] = email
                    if name is not None:
                        update_fields["name"] = name
                    stripeCustomer = stripe.Customer.modify(id, **update_fields)
                    print(
                        f"Stripe customer updated name: {stripeCustomer.name}, email: {stripeCustomer.email}"
                    )

                elif data["method"] == "delete":
                    stripeCustomer = stripe.Customer.delete(id)
                    print("Stripe customer deleted")

        finally:
            self.consumer.close()


if __name__ == "__main__":
    OutgoingConsumer().sync()
