
import pandas as pd


def detect_candlestick_patterns(
    df: pd.DataFrame
) -> list[dict]:

    patterns = []

    for i in range(1, len(df)):

        previous = df.iloc[i - 1]
        current = df.iloc[i]

        prev_open = previous["Open"]
        prev_close = previous["Close"]

        open_price = current["Open"]
        close_price = current["Close"]
        high_price = current["High"]
        low_price = current["Low"]

        body = abs(close_price - open_price)

        upper_wick = (
            high_price - max(open_price, close_price)
        )

        lower_wick = (
            min(open_price, close_price) - low_price
        )

        candle_range = high_price - low_price

        # Avoid division by zero
        if candle_range <= 0 or body <= 0:
            continue

        pattern = None
        direction = None
        start_idx = i

        # --------------------------------
        # Bullish Engulfing
        # --------------------------------

        if (
            prev_close < prev_open
            and close_price > open_price
            and open_price <= prev_close
            and close_price >= prev_open
        ):

            pattern = "Bullish Engulfing"
            direction = "BULLISH"
            start_idx = i - 1

        # --------------------------------
        # Bearish Engulfing
        # --------------------------------

        elif (
            prev_close > prev_open
            and close_price < open_price
            and open_price >= prev_close
            and close_price <= prev_open
        ):

            pattern = "Bearish Engulfing"
            direction = "BEARISH"
            start_idx = i - 1

        # --------------------------------
        # Hammer
        # --------------------------------

        elif (
            lower_wick >= 2 * body
            and upper_wick <= 0.5 * body
            and body / candle_range <= 0.4
        ):

            pattern = "Hammer"
            direction = "BULLISH"

        # --------------------------------
        # Shooting Star
        # --------------------------------

        elif (
            upper_wick >= 2 * body
            and lower_wick <= 0.5 * body
            and body / candle_range <= 0.4
        ):

            pattern = "Shooting Star"
            direction = "BEARISH"

        if pattern:

            patterns.append({
                "Pattern": pattern,
                "Direction": direction,
                "Start_Index": start_idx,
                "End_Index": i,
                "Start_Date": df.iloc[start_idx]["Date"],
                "End_Date": current["Date"],
                "Price": float(close_price),
                "Confidence": 0.70,
                "Confirmed": True
            })

    return patterns
