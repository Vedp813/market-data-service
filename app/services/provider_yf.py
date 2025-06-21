import yfinance as yf
from datetime import datetime, timezone
from app.models.price import Price
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class YahooFinanceProvider:
    """
    Provider class to fetch latest stock price data using yfinance.

    Attributes:
        name (str): Identifier for this data provider.
    """

    name = "yahoo_finance"

    def fetch_price(self, symbol: str) -> Optional[Price]:
        """
        Fetch the latest closing price for a given stock symbol.

        Args:
            symbol (str): Stock symbol to fetch data for.

        Returns:
            Price: ORM Price object containing symbol, price, timestamp, and provider.

        Raises:
            ValueError: If no price data is found for the symbol.
            Exception: For any other unexpected errors during data fetch.
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if data.empty:
                logger.warning(f"No data found for symbol: {symbol}")
                raise ValueError(f"No data found for symbol: {symbol}")
            
            latest = data.iloc[-1]
            price_obj = Price(
                symbol=symbol.upper(),
                price=float(latest["Close"]),
                timestamp=datetime.now(timezone.utc),
                provider=self.name
            )
            logger.info(f"Fetched price for {symbol}: {price_obj.price} at {price_obj.timestamp}")
            return price_obj
        
        except Exception as e:
            logger.error(f"Failed to fetch price for {symbol}: {e}")
            raise
