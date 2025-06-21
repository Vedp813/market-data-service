"""
ORM model for storing raw price data per stock symbol, provider, and timestamp.
Composite primary key ensures one unique price per symbol-timestamp.
"""

from sqlalchemy import Column, String, Float, DateTime, PrimaryKeyConstraint, Index
from datetime import datetime
from app.models.base import Base

class Price(Base):
    __tablename__ = "prices"

    symbol = Column(String, nullable=False, doc="Stock symbol (e.g., AAPL)")
    price = Column(Float, nullable=False, doc="Price of the stock at this timestamp")
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, doc="UTC time when the price was recorded")
    provider = Column(String, nullable=False, doc="Source of the price data (e.g., yahoo_finance)")

    __table_args__ = (
        PrimaryKeyConstraint('symbol', 'timestamp'),
        Index("ix_prices_symbol_timestamp", "symbol", "timestamp"),
    )
