from pydantic import BaseModel, Field
from datetime import datetime

class MovingAverageSchema(BaseModel):
    """
    Schema for representing the moving average of a stock symbol.

    Attributes:
        symbol (str): The stock ticker symbol (e.g., "AAPL").
        moving_avg (float): The computed 5-point moving average price.
        timestamp (datetime): The last update time for the moving average.
    """
    symbol: str = Field(..., description="Stock ticker symbol")
    moving_avg: float = Field(..., gt=0, description="5-point moving average price")
    timestamp: datetime = Field(..., description="Timestamp of the moving average update")

    model_config = {
        "from_attributes": True,  # Allows Pydantic to parse ORM objects (e.g., SQLAlchemy models)
        "populate_by_name": True,  # Accept alias fields if needed
    }
