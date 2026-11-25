
import numpy as np
import pandas as pd

from scipy.signal import find_peaks


def detect_swing_points(
    df: pd.DataFrame,
    distance: int = 5,
    prominence: float | None = None
) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame(
            columns=["Index", "Date", "Type", "Price"]
        )

    highs = df["High"].to_numpy(dtype=float)
    lows = df["Low"].to_numpy(dtype=float)

    # Detect local high points
    high_indices, _ = find_peaks(
        highs,
        distance=distance,
        prominence=prominence
    )

    # Detect local low points
    low_indices, _ = find_peaks(
        -lows,
        distance=distance,
        prominence=prominence
    )

    points = []

    for idx in high_indices:
        points.append({
            "Index": int(idx),
            "Date": df.iloc[idx]["Date"],
            "Type": "HIGH",
            "Price": float(highs[idx])
        })

    for idx in low_indices:
        points.append({
            "Index": int(idx),
            "Date": df.iloc[idx]["Date"],
            "Type": "LOW",
            "Price": float(lows[idx])
        })

    result = pd.DataFrame(points)

    if result.empty:
        return pd.DataFrame(
            columns=["Index", "Date", "Type", "Price"]
        )

    result = result.sort_values("Index")

    return result.reset_index(drop=True)
