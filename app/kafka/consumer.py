import json
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
import stripe
from app.db.db import SessionLocal
from app.api.utils.customer_utils import (
    fetch_customer_by_id,
    save_customer_to_db,
    update_customer_in_db,
    delete_customer_in_db,
)


# dependency


class OutgoingConsumer:
    kafka_server = "localhost:9092"

    topic = "stripe_outgoing"

    def __init__(self):
        self.admin_client = AdminClient({"bootstrap.servers": self.kafka_server})
        self.create_topic(self.topic)
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.kafka_server,
                "group.id": "stripe-group",
                "auto.offset.reset": "latest",
                "enable.auto.commit": False,
                "allow.auto.create.topics": "True",
            }
        )
        self.consumer.subscribe([self.topic])

    def create_topic(self, topic_name):
        topic_list = [NewTopic(topic_name, num_partitions=1, replication_factor=1)]
        self.admin_client.create_topics(topic_list)

    def sync(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    # print("Listening for messages from local...")
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


class IncomingConsumer:
    kafka_server = "localhost:9092"

    topic = "stripe_incoming"

    def __init__(self):
        self.admin_client = AdminClient({"bootstrap.servers": self.kafka_server})
        self.create_topic(self.topic)
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.kafka_server,
                "group.id": "stripe-group",
                "auto.offset.reset": "latest",
                "enable.auto.commit": False,
                "allow.auto.create.topics": "True",
            }
        )
        self.consumer.subscribe([self.topic])

    def create_topic(self, topic_name):
        topic_list = [NewTopic(topic_name, num_partitions=1, replication_factor=1)]
        self.admin_client.create_topics(topic_list)

    def sync(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    # print("Listening for messages from stripe...")
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
                    # Save to database
                    customer_data = {"id": id, "email": email, "name": name}
                    db = SessionLocal()
                    try:
                        save_customer_to_db(customer_data, db)
                        print(f"Database customer created name: {name}, email: {email}")
                    finally:
                        db.close()

                elif data["method"] == "update":
                    update_fields = {}
                    if email is not None:
                        update_fields["email"] = email
                    if name is not None:
                        update_fields["name"] = name
                    db = SessionLocal()
                    try:
                        customer = fetch_customer_by_id(id, db)
                        if customer:
                            for key, value in update_fields.items():
                                setattr(customer, key, value)
                            update_customer_in_db(customer, db)
                            print(
                                f"Database customer updated name: {customer.name}, email: {customer.email}"
                            )
                    finally:
                        db.close()

                elif data["method"] == "delete":
                    db = SessionLocal()
                    try:
                        customer = fetch_customer_by_id(id, db)
                        if customer:
                            delete_customer_in_db(customer, db)
                        print("Database customer deleted")
                    finally:
                        db.close()

        finally:
            self.consumer.close()


if __name__ == "__main__":
    OutgoingConsumer().sync()
    IncomingConsumer().sync()
