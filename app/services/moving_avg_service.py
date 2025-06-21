# services/moving_avg_service.py

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.models.price import Price
from app.models.moving_avg import MovingAverage
from app.utils.average import calculate_moving_average

logger = logging.getLogger(__name__)

def get_last_n_prices(db: Session, symbol: str, n: int = 5) -> List[Price]:
    """
    Fetch the latest N price records for a given stock symbol.

    Args:
        db (Session): SQLAlchemy session instance.
        symbol (str): The stock symbol (e.g., 'AAPL').
        n (int): Number of latest prices to fetch (default is 5).

    Returns:
        List[Price]: A list of Price ORM objects ordered by timestamp DESC.
    """
    try:
        return (
            db.query(Price)
            .filter(Price.symbol == symbol)
            .order_by(Price.timestamp.desc())
            .limit(n)
            .all()
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching prices for {symbol}: {e}")
        return []

def store_moving_average(db: Session, symbol: str, average: float) -> Optional[MovingAverage]:
    """
    Store or update the moving average for a given symbol in the database.

    Args:
        db (Session): SQLAlchemy session instance.
        symbol (str): Stock symbol (e.g., 'AAPL').
        average (float): The calculated moving average value.

    Returns:
        Optional[MovingAverage]: The stored MovingAverage instance if successful, else None.
    """
    try:
        avg = MovingAverage(
            symbol=symbol,
            moving_avg=average,
            timestamp=datetime.utcnow()
        )
        db.merge(avg)  # Performs UPSERT based on primary key (symbol).
        db.commit()
        logger.info(f"Stored moving average for {symbol}: {average}")
        return avg
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to store moving average for {symbol}: {e}")
        return None
