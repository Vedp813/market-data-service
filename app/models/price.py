from sqlalchemy import Column, String, Float, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Price(Base):
    __tablename__ = "prices"

    symbol = Column(String,nullable=False)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    provider = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint('symbol', 'timestamp'),
    )