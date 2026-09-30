import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_SERVER = "kafka:9092"
TOPIC = "orders"

while True:
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="order-processors",
            value_deserializer=lambda v: json.loads(v.decode("utf-8"))
        )
        break
    except NoBrokersAvailable:
        print("Kafka is not ready. Retrying...")
        time.sleep(3)

print("Consumer started. Waiting for orders...")

for message in consumer:
    order = message.value

    print("\nReceived Order:")
    print(f"Order ID: {order['order_id']}")
    print(f"Product: {order['product']}")
    print(f"Amount: ₹{order['amount']}")
    print("Status: PROCESSED")