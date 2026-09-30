import json
import time
from kafka import KafkaProducer

KAFKA_SERVER = "kafka:9092"
TOPIC = "orders"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

orders = [
    {
        "order_id": 101,
        "product": "Laptop",
        "amount": 55000
    },
    {
        "order_id": 102,
        "product": "Mouse",
        "amount": 1200
    },
    {
        "order_id": 103,
        "product": "Keyboard",
        "amount": 2500
    }
]

for order in orders:
    producer.send(TOPIC, value=order)
    print(f"Sent: {order}")
    time.sleep(2)

producer.flush()
producer.close()

print("All orders sent successfully!")