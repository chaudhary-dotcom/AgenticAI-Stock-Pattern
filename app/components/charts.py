
import plotly.graph_objects as go
import pandas as pd


def create_pattern_chart(
    df: pd.DataFrame,
    patterns: list[dict],
    swing_points: pd.DataFrame = None
):

    # ==================================
    # Initialize chart FIRST
    # ==================================

    fig = go.Figure()

    # ==================================
    # Candlestick chart
    # ==================================

    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Stock Price"
        )
    )

    # ==================================
    # Highlight swing highs and lows
    # ==================================

    if swing_points is not None and not swing_points.empty:

        for point_type, color, symbol in [
            ("HIGH", "orange", "triangle-down"),
            ("LOW", "cyan", "triangle-up")
        ]:

            selected = swing_points[
                swing_points["Type"] == point_type
            ]

            fig.add_trace(
                go.Scatter(
                    x=selected["Date"],
                    y=selected["Price"],
                    mode="markers",
                    marker={
                        "size": 9,
                        "color": color,
                        "symbol": symbol
                    },
                    name=f"Swing {point_type}"
                )
            )

    # ==================================
    # Pattern highlighting
    # ==================================

    colors = {
        "Double Top": "red",
        "Double Bottom": "green",
        "Bullish Engulfing": "limegreen",
        "Bearish Engulfing": "crimson",
        "Hammer": "blue",
        "Shooting Star": "orange"
    }

    for pattern in patterns:

        name = pattern["Pattern"]
        start_idx = pattern["Start_Index"]
        end_idx = pattern["End_Index"]

        color = colors.get(name, "purple")

        # Candle patterns
        if name in [
            "Bullish Engulfing",
            "Bearish Engulfing",
            "Hammer",
            "Shooting Star"
        ]:

            fig.add_trace(
                go.Scatter(
                    x=[df.iloc[end_idx]["Date"]],
                    y=[pattern["Price"]],
                    mode="markers+text",
                    marker={
                        "size": 13,
                        "color": color,
                        "symbol": "diamond"
                    },
                    text=[name],
                    textposition="top center",
                    name=name,
                    hovertemplate=(
                        f"{name}<br>"
                        "Date: %{x}<br>"
                        "Price: %{y}<extra></extra>"
                    )
                )
            )

        # Double Top / Bottom
        else:

            second_idx = pattern["Second_Index"]

            first_date = df.iloc[start_idx]["Date"]
            second_date = df.iloc[second_idx]["Date"]
            end_date = df.iloc[end_idx]["Date"]

            if name == "Double Top":
                first_price = pattern["Peak_1"]
                second_price = pattern["Peak_2"]
            else:
                first_price = pattern["Trough_1"]
                second_price = pattern["Trough_2"]

            # Connect the two peaks or troughs
            fig.add_trace(
                go.Scatter(
                    x=[first_date, second_date],
                    y=[first_price, second_price],
                    mode="lines+markers",
                    line={
                        "color": color,
                        "width": 3
                    },
                    marker={"size": 10},
                    name=name,
                    hovertemplate=(
                        f"{name}<br>"
                        "Date: %{x}<br>"
                        "Price: %{y}<extra></extra>"
                    )
                )
            )

            # Draw neckline
            fig.add_shape(
                type="line",
                x0=first_date,
                x1=end_date,
                y0=pattern["Neckline"],
                y1=pattern["Neckline"],
                line={
                    "color": color,
                    "width": 2,
                    "dash": "dash"
                }
            )

            # Mark breakout
            fig.add_trace(
                go.Scatter(
                    x=[end_date],
                    y=[df.iloc[end_idx]["Close"]],
                    mode="markers+text",
                    marker={
                        "size": 12,
                        "color": color,
                        "symbol": "star"
                    },
                    text=["Breakout"],
                    textposition="bottom center",
                    name=f"{name} confirmation"
                )
            )

    # ==================================
    # Layout
    # ==================================

    fig.update_layout(
        title="Stock Pattern Detection Analysis",
        xaxis_title="Date",
        yaxis_title="Stock Price",
        template="plotly_dark",
        height=700,
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        legend={
            "orientation": "h",
            "y": 1.05
        }
    )

    return fig
