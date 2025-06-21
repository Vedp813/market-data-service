"""
SQLAlchemy ORM model for storing moving averages of stock prices.
Each symbol is stored once and updated as new data is processed.
"""

from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from app.models.base import Base

class MovingAverage(Base):
    __tablename__ = "symbol_averages"

    symbol = Column(String, primary_key=True, index=True, doc="Stock ticker symbol (e.g., AAPL)")
    moving_avg = Column(Float, nullable=False, doc="5-point moving average for the stock")
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, doc="Last update time (UTC)")
