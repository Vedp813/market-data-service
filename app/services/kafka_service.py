# services/kafka_service.py

import json
import uuid
import logging
from confluent_kafka import Producer
from pydantic import BaseModel
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Kafka Producer Configuration
producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "linger.ms": 10,
    "acks": "all",
    "retries": 3
})

class PriceEvent(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
    provider: str

def publish_price_event(price_event: PriceEvent):
    """Publish a price event to Kafka topic 'price-events'.

    Args:
        price_event (PriceEvent): The event containing symbol, price, timestamp, provider.

    Raises:
        Exception: If Kafka message fails to deliver.
    """
    event_payload = {
        "symbol": price_event.symbol,
        "price": price_event.price,
        "timestamp": price_event.timestamp.isoformat(),
        "provider": price_event.provider,
        "raw_response_id": str(uuid.uuid4())
    }

    def delivery_report(err, msg):
        if err:
            logger.error(f"Delivery failed for {price_event.symbol}: {err}")
        else:
            logger.info(f"Delivered {price_event.symbol} to {msg.topic()} [partition {msg.partition()}]")

    try:
        producer.produce(
            topic="price-events",
            key=price_event.symbol,  # Key for better partitioning
            value=json.dumps(event_payload),
            callback=delivery_report
        )
        producer.flush()
    except Exception as e:
        logger.exception(f"Failed to produce message: {e}")
        raise
