from pydantic import BaseModel, Field
from datetime import datetime

class PriceOut(BaseModel):
    """
    Response schema for a price record.

    Attributes:
        symbol (str): The stock ticker symbol (e.g., 'AAPL').
        price (float): The recorded price of the stock.
        timestamp (datetime): The datetime when the price was recorded.
        provider (str): The data provider that supplied this price.
    """
    symbol: str = Field(..., example="AAPL", description="Ticker symbol for the stock.")
    price: float = Field(..., example=150.23, description="Current or historical stock price.")
    timestamp: datetime = Field(..., example="2025-06-21T12:34:56", description="Timestamp of the price data.")
    provider: str = Field(..., example="yahoo_finance", description="Source of the price information.")

    model_config = {
        "from_attributes": True  # Enables creation from ORM objects like SQLAlchemy rows
    }
