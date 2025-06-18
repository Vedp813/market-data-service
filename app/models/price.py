from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Price(Base):
    __tablename__ = "prices"

    symbol = Column(String, primary_key=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    provider = Column(String)