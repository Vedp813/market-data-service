from sqlalchemy.orm import Session
from app.services.provider_yf import YahooFinanceProvider
from app.services.kafka_service import publish_price_event
from app.models.price import Price
from app.models.moving_avg import MovingAverage
import logging

logger = logging.getLogger(__name__)

def fetch_and_store_price(symbol: str, db: Session) -> Price:
    """
    Fetch the latest stock price for a symbol, store it in the database, and publish it to Kafka.

    Args:
        symbol (str): The stock symbol to fetch the price for (e.g., "AAPL").
        db (Session): SQLAlchemy database session.

    Returns:
        Price: The SQLAlchemy model instance representing the fetched price.

    Raises:
        Exception: If the provider fails or DB operations fail.
    """
    try:
        provider = YahooFinanceProvider()
        price_obj = provider.fetch_price(symbol)
        db.add(price_obj)
        db.commit()
        publish_price_event(price_obj)
        return price_obj
    except Exception as e:
        db.rollback()
        logger.error(f"Error fetching/storing price for {symbol}: {e}")
        raise

def get_moving_average(symbol: str, db: Session) -> MovingAverage | None:
    """
    Retrieve the stored moving average for a given stock symbol.

    Args:
        symbol (str): The stock symbol (e.g., "AAPL").
        db (Session): SQLAlchemy database session.

    Returns:
        MovingAverage | None: The moving average record if found, else None.
    """
    return db.query(MovingAverage).filter(MovingAverage.symbol == symbol.upper()).first()
