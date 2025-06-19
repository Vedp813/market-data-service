from fastapi import FastAPI
from app.api.routes import router
from app.models.price import Base
from app.core.config import DATABASE_URL
from sqlalchemy import create_engine
import threading
from app.kafka_consumer import consume_market_data
from app.models.moving_average import MovingAverage




app = FastAPI(title="Market Data Service")
app.include_router(router)

# Initialize database
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)
MovingAverage.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Market Data Service running"}

@app.on_event("startup")
def startup_event():
    threading.Thread(target=consume_market_data, daemon=True).start()