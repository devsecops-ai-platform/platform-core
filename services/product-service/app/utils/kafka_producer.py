from kafka import KafkaProducer
import json

producer = None

try:

    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print("Kafka connected successfully")

except Exception as e:

    print(f"Kafka connection failed: {e}")


def publish_product_created_event(product):

    if producer:

        producer.send(
            'product-created',
            product
        )

        producer.flush()

        print("Product created event published")

    else:

        print("Kafka producer unavailable")