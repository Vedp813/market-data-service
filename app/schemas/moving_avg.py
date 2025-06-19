from pydantic import BaseModel
from datetime import datetime

class MovingAverageSchema(BaseModel):
    symbol: str
    moving_avg: float
    timestamp: datetime

    # Enable loading from SQLAlchemy models
    model_config = {
        "from_attributes": True  # replaces `orm_mode = True` in Pydantic v2
    }
