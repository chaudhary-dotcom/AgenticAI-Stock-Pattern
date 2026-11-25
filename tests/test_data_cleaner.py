
import pandas as pd

from backend.data_cleaner import standardize_market_data


def test_standardize_market_data():

    # Create sample data with different column names
    sample_data = pd.DataFrame({
        "trading_date": [
            "2025-01-03",
            "2025-01-01",
            "2025-01-02"
        ],
        "open_price": [101, 100, 102],
        "HIGH": [106, 105, 107],
        "low_price": [99, 98, 100],
        "closing_price": [105, 103, 104],
        "trading_volume": [1500, 1000, 1200]
    })

    # Standardize data
    cleaned_df, issues = standardize_market_data(sample_data)

    # Verify standardized column names
    expected_columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    assert list(cleaned_df.columns) == expected_columns

    # Verify rows are sorted by date
    assert cleaned_df["Date"].is_monotonic_increasing

    # Verify correct number of rows
    assert len(cleaned_df) == 3

    # Verify dates
    expected_dates = pd.to_datetime([
        "2025-01-01",
        "2025-01-02",
        "2025-01-03"
    ])

    assert list(cleaned_df["Date"]) == list(expected_dates)

    # Verify closing prices remain correctly associated with dates
    assert list(cleaned_df["Close"]) == [103, 104, 105]

    print("All data cleaner assertions passed!")


if __name__ == "__main__":
    test_standardize_market_data()
