from confluent_kafka import Producer
import json
import uuid

producer = Producer({"bootstrap.servers": "localhost:9092"})

def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed:", err)
    else:
        print("Message delivered to", msg.topic(), msg.partition())

def publish_price_event(price_obj):
    event = {
        "symbol": price_obj.symbol,
        "price": price_obj.price,
        "timestamp": price_obj.timestamp.isoformat(),
        "provider": price_obj.provider,
        "raw_response_id": str(uuid.uuid4())
    }

    producer.produce(
        topic="price-events",
        value=json.dumps(event),
        callback=delivery_report
    )
    producer.flush()
