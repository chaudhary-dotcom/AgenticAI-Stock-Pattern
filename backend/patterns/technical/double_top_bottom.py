
import pandas as pd

from backend.patterns.technical.swing_points import (
    detect_swing_points
)


def detect_double_patterns(
    df: pd.DataFrame,
    tolerance: float = 0.03,
    min_separation: int = 5,
    max_separation: int = 80,
    breakout_window: int = 20
) -> list[dict]:

    if df.empty:
        return []

    swings = detect_swing_points(
        df,
        distance=3
    )

    highs = swings[
        swings["Type"] == "HIGH"
    ].reset_index(drop=True)

    lows = swings[
        swings["Type"] == "LOW"
    ].reset_index(drop=True)

    results = []

    def price_similarity(a, b):
        return abs(a - b) / ((a + b) / 2)

    # ==================================
    # DOUBLE TOP
    # ==================================

    for i in range(len(highs) - 1):

        first = highs.iloc[i]
        second = highs.iloc[i + 1]

        first_idx = int(first["Index"])
        second_idx = int(second["Index"])

        separation = second_idx - first_idx

        if not min_separation <= separation <= max_separation:
            continue

        similarity = price_similarity(
            first["Price"],
            second["Price"]
        )

        if similarity > tolerance:
            continue

        middle_lows = lows[
            (lows["Index"] > first_idx)
            & (lows["Index"] < second_idx)
        ]

        if middle_lows.empty:
            continue

        neckline_row = middle_lows.loc[
            middle_lows["Price"].idxmin()
        ]

        neckline = float(neckline_row["Price"])

        # Search for neckline breakdown
        search_end = min(
            second_idx + breakout_window + 1,
            len(df)
        )

        breakout = None

        for j in range(second_idx + 1, search_end):

            if df.iloc[j]["Close"] < neckline:
                breakout = j
                break

        if breakout is None:
            continue

        confidence = max(
            0.0,
            min(
                1.0,
                0.85 - (similarity / tolerance) * 0.15
            )
        )

        results.append({
            "Pattern": "Double Top",
            "Direction": "BEARISH",
            "Start_Index": first_idx,
            "End_Index": breakout,
            "Second_Index": second_idx,
            "Second_Date": second["Date"],
            "Peak_1": float(first["Price"]),
            "Peak_2": float(second["Price"]),
            "Neckline": neckline,
            "Start_Date": first["Date"],
            "End_Date": df.iloc[breakout]["Date"],
            "Confidence": round(confidence, 3),
            "Confirmed": True
        })

    # ==================================
    # DOUBLE BOTTOM
    # ==================================

    for i in range(len(lows) - 1):

        first = lows.iloc[i]
        second = lows.iloc[i + 1]

        first_idx = int(first["Index"])
        second_idx = int(second["Index"])

        separation = second_idx - first_idx

        if not min_separation <= separation <= max_separation:
            continue

        similarity = price_similarity(
            first["Price"],
            second["Price"]
        )

        if similarity > tolerance:
            continue

        middle_highs = highs[
            (highs["Index"] > first_idx)
            & (highs["Index"] < second_idx)
        ]

        if middle_highs.empty:
            continue

        neckline_row = middle_highs.loc[
            middle_highs["Price"].idxmax()
        ]

        neckline = float(neckline_row["Price"])

        # Search for neckline breakout
        search_end = min(
            second_idx + breakout_window + 1,
            len(df)
        )

        breakout = None

        for j in range(second_idx + 1, search_end):

            if df.iloc[j]["Close"] > neckline:
                breakout = j
                break

        if breakout is None:
            continue

        confidence = max(
            0.0,
            min(
                1.0,
                0.85 - (similarity / tolerance) * 0.15
            )
        )

        results.append({
            "Pattern": "Double Bottom",
            "Direction": "BULLISH",
            "Start_Index": first_idx,
            "End_Index": breakout,
            "Second_Index": second_idx,
            "Second_Date": second["Date"],
            "Trough_1": float(first["Price"]),
            "Trough_2": float(second["Price"]),
            "Neckline": neckline,
            "Start_Date": first["Date"],
            "End_Date": df.iloc[breakout]["Date"],
            "Confidence": round(confidence, 3),
            "Confirmed": True
        })

    return results
