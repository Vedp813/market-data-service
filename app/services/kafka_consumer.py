import time
import logging
import json
from confluent_kafka import Consumer, KafkaError
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import SessionLocal
from app.services.moving_avg_service import get_last_n_prices, store_moving_average
from app.utils.average import calculate_moving_average

logger = logging.getLogger(__name__)

def consume_market_data():
    """
    Consumes price events from Kafka topic 'price-events', calculates
    moving averages from recent prices, and stores the results into the database.

    Uses a Kafka consumer with 'earliest' offset reset, continuously polling.
    For each message:
        - Deserialize JSON payload.
        - Extract symbol.
        - Fetch last 5 prices for the symbol from DB.
        - Calculate moving average.
        - Store moving average in DB.
    """
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'avg-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,  # disable auto commit for manual control
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe(['price-events'])
    logger.info("Kafka consumer started and subscribed to 'price-events'")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue  # no message received, keep polling
            if msg.error():
                # Log and handle errors appropriately
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"End of partition reached {msg.topic()} [{msg.partition()}]")
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                continue

            try:
                data = json.loads(msg.value().decode('utf-8'))
                symbol = data.get("symbol")
                if not symbol:
                    logger.warning("Received message without symbol field")
                    consumer.commit(msg)  # commit offset anyway to avoid reprocessing bad message
                    continue

                # Wait briefly for DB commits (optional, may be removed with proper transaction handling)
                time.sleep(0.1)

                with SessionLocal() as db:
                    prices = get_last_n_prices(db, symbol)
                    logger.debug(f"Fetched {len(prices)} prices for symbol {symbol}")
                    price_values = [p.price for p in reversed(prices)]  # oldest to newest
                    avg = calculate_moving_average(price_values)
                    logger.info(f"Calculated moving average for {symbol}: {avg}")

                    store_moving_average(db, symbol, avg)
                    db.commit()  # ensure commit in this scope

                consumer.commit(msg)  # manually commit offset after processing message

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse Kafka message or missing keys: {e}")
                consumer.commit(msg)  # commit offset to skip bad message
            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                # optionally decide whether to commit or not based on error severity
            except Exception as e:
                logger.error(f"Unexpected error processing message: {e}")

    except KeyboardInterrupt:
        logger.info("Consumer shutting down on interrupt")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed")
