
import yfinance as yf

from backend.data.preprocessing.cleaner import (
    standardize_stock_data
)


def fetch_us_stock_data(
    symbol: str,
    period: str = "5y",
    interval: str = "1d"
):

    ticker = yf.Ticker(symbol)

    df = ticker.history(
        period=period,
        interval=interval,
        auto_adjust=False
    )

    if df.empty:
        raise ValueError(
            f"No historical data found for {symbol}"
        )

    # Move Date from index into a column
    df = df.reset_index()

    # Remove timezone information if present
    if "Date" in df.columns:
        df["Date"] = df["Date"].dt.tz_localize(
            None
        ) if df["Date"].dt.tz is not None else df["Date"]

    return standardize_stock_data(
        df=df,
        symbol=symbol,
        market="US"
    )
