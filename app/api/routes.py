from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas.price import PriceOut
from app.services.provider_yf import YahooFinanceProvider
from app.models.price import Price
from app.core.config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = APIRouter()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

yf_provider = YahooFinanceProvider()

@router.get("/prices/latest", response_model=PriceOut)
def get_latest_price(symbol: str):
    db: Session = SessionLocal()
    try:
        price_obj = yf_provider.fetch_price(symbol)
        db.merge(price_obj)  # upsert
        db.commit()
        return price_obj
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        db.close()