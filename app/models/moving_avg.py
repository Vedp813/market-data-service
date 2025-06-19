from sqlalchemy import Column, String, Float, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MovingAverage(Base):
    __tablename__ = "symbol_averages"

    symbol = Column(String, index=True, nullable=False)
    moving_avg = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        PrimaryKeyConstraint('symbol', 'timestamp'),
    )