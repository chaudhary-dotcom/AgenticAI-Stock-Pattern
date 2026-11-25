
import pandas as pd
from scipy.signal import find_peaks


def detect_swing_points(
    df: pd.DataFrame,
    distance: int = 5,
    prominence: float = 0.02
):
    """
    Detect swing highs and swing lows in stock price data.
    """

    swing_highs, _ = find_peaks(
        df["High"].values,
        distance=distance,
        prominence=prominence
    )

    swing_lows, _ = find_peaks(
        -df["Low"].values,
        distance=distance,
        prominence=prominence
    )

    highs = pd.DataFrame({
        "Index": swing_highs,
        "Date": df.iloc[swing_highs]["Date"].values,
        "Price": df.iloc[swing_highs]["High"].values,
        "Type": "HIGH"
    })

    lows = pd.DataFrame({
        "Index": swing_lows,
        "Date": df.iloc[swing_lows]["Date"].values,
        "Price": df.iloc[swing_lows]["Low"].values,
        "Type": "LOW"
    })

    return highs, lows
