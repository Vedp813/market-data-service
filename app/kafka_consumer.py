from confluent_kafka import Consumer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from app.core.config import DATABASE_URL
from app.models.price import Price
from app.models.moving_average import MovingAverage
import json
import datetime

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "ma-computer",
    "auto.offset.reset": "earliest"
})

consumer.subscribe(["price-events"])

def calculate_moving_average(prices):
    return sum(prices) / len(prices) if prices else 0

def consume_market_data():
    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue

        event = json.loads(msg.value())
        symbol = event["symbol"]

        db = SessionLocal()
        try:
            last_prices = db.query(Price).filter(Price.symbol == symbol)\
                            .order_by(desc(Price.timestamp)).limit(5).all()

            avg = calculate_moving_average([p.price for p in last_prices])

            ma_entry = MovingAverage(
                symbol=symbol,
                moving_avg=avg,
                timestamp=datetime.datetime.utcnow()
            )

            db.merge(ma_entry)
            db.commit()
        except Exception as e:
            print("Error in consumer:", e)
        finally:
            db.close()
