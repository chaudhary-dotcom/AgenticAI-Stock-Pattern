
from pathlib import Path
import numpy as np
import pandas as pd

from backend.market_analyzer import analyze_market_file


def test_market_analyzer():

    # Generate realistic stock price movements
    total_days = 120
    x = np.arange(total_days)

    closing_prices = (
        100
        + 0.08 * x
        + 8 * np.sin(x * 2 * np.pi / 20)
    )

    opening_prices = (
        closing_prices
        - 1.2 * np.cos(x * 0.7)
    )

    high_prices = (
        np.maximum(opening_prices, closing_prices) + 1.5
    )

    low_prices = (
        np.minimum(opening_prices, closing_prices) - 1.5
    )

    data = {
        "trading_date": pd.date_range(
            start="2025-01-01",
            periods=total_days
        ),
        "open_price": opening_prices,
        "HIGH": high_prices,
        "low_price": low_prices,
        "closing_price": closing_prices,
        "trading_volume": 1000 + (x * 15)
    }

    df = pd.DataFrame(data)

    # Save sample data
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "analyzer_test.csv"
    df.to_csv(file_path, index=False)

    assert file_path.exists()

    # Analyze market data
    result = analyze_market_file(str(file_path))

    # Verify analysis result structure
    required_keys = [
        "data",
        "processing_report",
        "patterns",
        "swing_points",
        "chart"
    ]

    for key in required_keys:
        assert key in result, f"Missing result key: {key}"

    # Verify processed market data
    assert len(result["data"]) == total_days

    expected_columns = [
        "Date", "Open", "High", "Low", "Close", "Volume"
    ]

    assert list(result["data"].columns) == expected_columns

    # Verify price data
    assert result["data"]["Close"].notna().all()
    assert (result["data"]["Close"] > 0).all()

    # Verify patterns and swing points
    assert isinstance(result["patterns"], list)

    assert isinstance(result["swing_points"], pd.DataFrame)

    assert not result["swing_points"].empty

    expected_swing_columns = [
        "Index", "Date", "Type", "Price"
    ]

    assert list(result["swing_points"].columns) == expected_swing_columns

    assert result["swing_points"]["Type"].isin(
        ["HIGH", "LOW"]
    ).all()

    assert result["swing_points"]["Price"].notna().all()

    for pattern in result["patterns"]:
        assert isinstance(pattern, dict)
        assert "Pattern" in pattern
    # Verify chart
    chart = result["chart"]

    assert chart is not None
    assert len(chart.data) > 0

    # Save interactive chart
    chart_path = output_dir / "market_analyzer_test.html"
    chart.write_html(str(chart_path))

    assert chart_path.exists()
    assert chart_path.stat().st_size > 0

    print("\nMARKET ANALYZER TEST")
    print("=" * 50)
    print("Processed rows:", len(result["data"]))
    print("Detected patterns:", len(result["patterns"]))
    print("Swing points:", len(result["swing_points"]))
    print("Chart saved:", chart_path.resolve())
    print("\nAll market analyzer assertions passed!")


if __name__ == "__main__":
    test_market_analyzer()
