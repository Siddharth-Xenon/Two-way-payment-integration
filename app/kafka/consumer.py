from confluent_kafka import Consumer, KafkaError


def kafka_consumer():
    # Consumer configuration
    conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "stripe-sync-group",
        "auto.offset.reset": "earliest",
    }

    # Create Consumer instance
    consumer = Consumer(**conf)
    consumer.subscribe(["customer_updates"])

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
        print("Received message: {}".format(msg.value().decode("utf-8")))
        # Here you would add the logic to update Stripe

    consumer.close()


# Run the consumer
kafka_consumer()
