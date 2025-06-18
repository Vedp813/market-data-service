import yfinance as yf
from datetime import datetime
from app.models.price import Price

class YahooFinanceProvider:
    name = "yahoo_finance"

    def fetch_price(self, symbol: str) -> Price:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            raise ValueError("No data found for symbol")
        latest = data.iloc[-1]
        return Price(
            symbol=symbol.upper(),
            price=float(latest["Close"]),
            timestamp=datetime.utcnow(),
            provider=self.name
        )