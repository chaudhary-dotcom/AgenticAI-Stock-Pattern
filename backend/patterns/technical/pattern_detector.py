
import pandas as pd

from backend.patterns.technical.swing_points import (
    detect_swing_points
)

from backend.patterns.technical.candlestick import (
    detect_candlestick_patterns
)

from backend.patterns.technical.double_top_bottom import (
    detect_double_patterns
)


def detect_all_patterns(
    df: pd.DataFrame
) -> dict:

    if df.empty:
        return {
            "swing_points": pd.DataFrame(),
            "patterns": []
        }

    swing_points = detect_swing_points(
        df,
        distance=5
    )

    candlestick_patterns = detect_candlestick_patterns(
        df
    )

    double_patterns = detect_double_patterns(
        df
    )

    all_patterns = (
        candlestick_patterns + double_patterns
    )

    all_patterns.sort(
        key=lambda x: x["Start_Index"]
    )

    return {
        "swing_points": swing_points,
        "patterns": all_patterns
    }
