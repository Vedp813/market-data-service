from sqlalchemy import Column, String, Float, DateTime
from app.models.price import Base
import datetime

class MovingAverage(Base):
    __tablename__ = "symbol_averages"

    symbol = Column(String, primary_key=True)
    moving_avg = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
