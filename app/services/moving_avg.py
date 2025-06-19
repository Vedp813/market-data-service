from app.utils.average import calculate_moving_average
from app.models.price import Price
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.moving_avg import MovingAverage  
from datetime import datetime

def store_moving_average(db: Session, symbol: str, average: float):
    avg = MovingAverage(
        symbol=symbol,
        moving_avg=average,
        timestamp=datetime.utcnow()
    )
    db.merge(avg)
    db.commit()


def get_last_n_prices(db: Session, symbol: str, n: int = 5):
    return (
        db.query(Price)
        .filter(Price.symbol == symbol)
        .order_by(Price.timestamp.desc())
        .limit(n)
        .all()
    )
