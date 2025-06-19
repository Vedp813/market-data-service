from confluent_kafka import Consumer
import json
from app.core.config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.moving_avg import get_last_n_prices, store_moving_average
from app.utils.average import calculate_moving_average

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def consume_market_data():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'avg-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['price-events'])

    print("🟢 Consumer started...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Kafka error: {msg.error()}")
            continue

        try:
            data = json.loads(msg.value().decode('utf-8'))
            symbol = data["symbol"]

            db = SessionLocal()
            prices = get_last_n_prices(db, symbol)
            avg = calculate_moving_average([p.price for p in prices])
            store_moving_average(db, symbol, avg)
            db.close()

            print(f"✅ Stored moving average for {symbol}: {avg}")
        except Exception as e:
            print(f"Error processing message: {e}")
