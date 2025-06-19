from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.schemas.price import PriceOut
from app.services.provider_yf import YahooFinanceProvider
from app.models.price import Price
from app.core.config import DATABASE_URL
from app.services.kafka_producer import publish_price_event

router = APIRouter()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

yf_provider = YahooFinanceProvider()

@router.get("/prices/latest", response_model=PriceOut)
def get_latest_price(symbol: str, db: Session = Depends(get_db)):
    try:
        price_obj = yf_provider.fetch_price(symbol)
        db.merge(price_obj)  # upsert
        db.commit()

        # Publish to Kafka
        publish_price_event(price_obj)

        return price_obj
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
