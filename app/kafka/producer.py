from confluent_kafka import Producer
import json


class OutgoingProducer:
    def __init__(self):
        # Configuration for Kafka Producer
        self.conf = {
            "bootstrap.servers": "localhost:9092",
            "acks": "all",  # Ensure producer receives acknowledgement from all brokers
        }
        self.topic = "stripe_outgoing"
        # Create Producer instance
        self.producer = Producer(**self.conf)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(
                f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
            )

    # Function to send messages
    def write_to_topic(self, method, customer):
        data = {
            "method": method,
            "Customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
            },
        }
        try:
            # Serialize data to JSON format and encode to utf-8
            serialized_data = json.dumps(data).encode("utf-8")
            self.producer.produce(
                self.topic, serialized_data, callback=self.delivery_report
            )

            self.producer.poll(1)
        except Exception as e:
            print(f"Failed to send message: {e}")
        finally:
            self.producer.flush()


# Usage example:
# producer = OutgoingProducer()
# producer.write_to_topic(
#     "create",
#     CustomerDB(id=1, name="John Doe", email="john.doe@example.com"),
# )
