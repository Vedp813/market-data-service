from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.price import PriceOut
from app.schemas.moving_avg import MovingAverageSchema
from app.core.config import get_db
from app.services.price_service import fetch_and_store_price, get_moving_average
from fastapi.concurrency import run_in_threadpool
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prices/latest", response_model=PriceOut, summary="Fetch latest stock price")
async def fetch_price(
    symbol: str = Query(..., description="Stock symbol to fetch the price for"),
    db: Session = Depends(get_db)
):
    """
    Fetches and stores the latest stock price for the given symbol.
    """
    try:
        result = await run_in_threadpool(fetch_and_store_price, symbol, db)
        return result
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {str(e)}")
        raise HTTPException(status_code=400, detail="Could not fetch price.")

@router.get("/prices/movingaverage", response_model=MovingAverageSchema, summary="Get 5-point moving average")
async def fetch_moving_average(
    symbol: str = Query(..., description="Stock symbol to get the moving average for"),
    db: Session = Depends(get_db)
):
    """
    Retrieves the latest 5-point moving average for the given symbol.
    """
    try:
        avg = await run_in_threadpool(get_moving_average, symbol, db)
        if not avg:
            raise HTTPException(status_code=404, detail="No moving average found.")
        return avg
    except Exception as e:
        logger.error(f"Error retrieving moving average for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal error.")
