
import pandas as pd


REQUIRED_COLUMNS = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]


def standardize_stock_data(
    df: pd.DataFrame,
    symbol: str,
    market: str
) -> pd.DataFrame:

    if df.empty:
        raise ValueError("Stock dataset is empty.")

    # Work on a copy
    df = df.copy()

    # Normalize column names
    df.columns = [
        str(col).strip().title()
        for col in df.columns
    ]

    # Handle common column variations
    aliases = {
        "Datetime": "Date",
        "Timestamp": "Date",
        "Adj Close": "Close",
        "Shares Traded": "Volume",
        "Turnover Volume": "Volume"
    }

    df = df.rename(columns=aliases)

    # Check required columns
    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    # Keep required columns
    df = df[REQUIRED_COLUMNS]

    # Convert dates
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
        utc=True
    ).dt.tz_convert(None)

    # Convert numerical columns
    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Remove invalid rows
    df = df.dropna(
        subset=["Date", "Open", "High", "Low", "Close"]
    )

    # Prices must be positive
    price_columns = [
        "Open", "High", "Low", "Close"
    ]

    df = df[
        (df[price_columns] > 0).all(axis=1)
    ]

    # Volume cannot be negative
    df = df[
        df["Volume"].isna() |
        (df["Volume"] >= 0)
    ]

    # Validate OHLC relationships
    valid_ohlc = (
        (df["High"] >= df[["Open", "Close", "Low"]].max(axis=1))
        &
        (df["Low"] <= df[["Open", "Close", "High"]].min(axis=1))
    )

    df = df[valid_ohlc]

    # Remove duplicate dates
    df = df.drop_duplicates(
        subset=["Date"],
        keep="last"
    )

    # Sort chronologically
    df = df.sort_values("Date")

    # Add metadata
    df["Symbol"] = symbol.upper()
    df["Market"] = market.upper()

    # Reset index
    df = df.reset_index(drop=True)

    return df
