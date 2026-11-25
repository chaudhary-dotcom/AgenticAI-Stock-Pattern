
import numpy as np
import pandas as pd


def normalize_price_sequence(
    prices: list | np.ndarray
) -> np.ndarray:
    """
    Normalize a price sequence relative to its first value.

    This makes price movements comparable across stocks
    with different price levels.
    """

    prices = np.asarray(prices, dtype=float)

    if len(prices) == 0:
        raise ValueError("Price sequence cannot be empty.")

    if not np.all(np.isfinite(prices)):
        raise ValueError("Prices must contain only finite values.")

    if prices[0] == 0:
        raise ValueError("First price cannot be zero.")

    normalized = (prices / prices[0]) - 1

    return normalized


def extract_price_sequences(
    df: pd.DataFrame,
    window_size: int = 20,
    step_size: int = 1
) -> list[dict]:
    """
    Extract overlapping windows from closing prices.
    Each window represents one historical price movement.
    """

    if "Close" not in df.columns:
        raise ValueError("DataFrame must contain a Close column.")

    if window_size < 2:
        raise ValueError("window_size must be at least 2.")

    if step_size < 1:
        raise ValueError("step_size must be at least 1.")

    close_prices = df["Close"].to_numpy(dtype=float)

    if not np.all(np.isfinite(close_prices)):
        raise ValueError("Closing prices must be finite.")

    sequences = []

    for start in range(
        0,
        len(close_prices) - window_size + 1,
        step_size
    ):

        end = start + window_size

        prices = close_prices[start:end]

        normalized = normalize_price_sequence(prices)

        sequences.append({
            "Start_Index": start,
            "End_Index": end - 1,
            "Start_Date": df.iloc[start]["Date"] if "Date" in df.columns else None,
            "End_Date": df.iloc[end - 1]["Date"] if "Date" in df.columns else None,
            "Original_Prices": prices,
            "Normalized_Prices": normalized
        })

    return sequences
