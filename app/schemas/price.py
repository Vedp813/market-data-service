from pydantic import BaseModel
from datetime import datetime

class PriceOut(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
    provider: str

    class Config:
        from_attributes = True