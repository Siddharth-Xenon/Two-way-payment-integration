from confluent_kafka import Producer


def kafka_producer():
    # Configuration for Kafka Producer
    conf = {"bootstrap.servers": "localhost:9092"}

    # Create Producer instance
    producer = Producer(**conf)

    # Function to send messages
    def send_message(topic, message):
        producer.produce(topic, message.encode("utf-8"))
        producer.flush()

    return send_message


# Usage example:
producer = kafka_producer()
producer(
    "customer_updates",
    'New customer added: {name: "John Doe", email: "john.doe@example.com"}',
)
