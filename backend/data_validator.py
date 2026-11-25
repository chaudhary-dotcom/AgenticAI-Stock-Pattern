
import pandas as pd


def validate_market_data(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, list[str]]:
    """
    Validate and clean historical OHLCV market data.

    Returns:
        cleaned_df: Valid market data.
        issues: List of problems found and handled.
    """

    if df.empty:
        raise ValueError("Market data is empty.")

    # Work on a copy to preserve original data
    cleaned_df = df.copy()
    issues = []

    # Required columns
    required_columns = [
        "Date", "Open", "High", "Low", "Close", "Volume"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in cleaned_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    original_count = len(cleaned_df)

    # Convert Date column
    cleaned_df["Date"] = pd.to_datetime(
        cleaned_df["Date"],
        errors="coerce"
    )

    invalid_dates = cleaned_df["Date"].isna()

    if invalid_dates.any():
        issues.append(
            f"Removed {invalid_dates.sum()} rows with invalid dates."
        )
        cleaned_df = cleaned_df.loc[~invalid_dates].copy()

    # Convert numeric columns
    numeric_columns = [
        "Open", "High", "Low", "Close", "Volume"
    ]

    for column in numeric_columns:
        cleaned_df[column] = pd.to_numeric(
            cleaned_df[column],
            errors="coerce"
        )

    # Remove missing or non-numeric values
    missing_values = cleaned_df[
        required_columns
    ].isna().any(axis=1)

    if missing_values.any():
        issues.append(
            f"Removed {missing_values.sum()} rows with missing or invalid values."
        )
        cleaned_df = cleaned_df.loc[~missing_values].copy()

    # Remove duplicate dates
    duplicate_dates = cleaned_df["Date"].duplicated()

    if duplicate_dates.any():
        issues.append(
            f"Removed {duplicate_dates.sum()} rows with duplicate dates."
        )
        cleaned_df = cleaned_df.loc[~duplicate_dates].copy()

    # Remove zero or negative prices
    invalid_prices = (
        (cleaned_df[["Open", "High", "Low", "Close"]] <= 0)
        .any(axis=1)
    )

    if invalid_prices.any():
        issues.append(
            f"Removed {invalid_prices.sum()} rows with zero or negative prices."
        )
        cleaned_df = cleaned_df.loc[~invalid_prices].copy()

    # Remove negative volume
    invalid_volume = cleaned_df["Volume"] < 0

    if invalid_volume.any():
        issues.append(
            f"Removed {invalid_volume.sum()} rows with negative volume."
        )
        cleaned_df = cleaned_df.loc[~invalid_volume].copy()

    # Validate OHLC relationships
    invalid_ohlc = (
        (cleaned_df["High"] < cleaned_df["Open"])
        | (cleaned_df["High"] < cleaned_df["Close"])
        | (cleaned_df["High"] < cleaned_df["Low"])
        | (cleaned_df["Low"] > cleaned_df["Open"])
        | (cleaned_df["Low"] > cleaned_df["Close"])
    )

    if invalid_ohlc.any():
        issues.append(
            f"Removed {invalid_ohlc.sum()} rows with invalid OHLC relationships."
        )
        cleaned_df = cleaned_df.loc[~invalid_ohlc].copy()

    # Sort by date
    cleaned_df = cleaned_df.sort_values(
        by="Date"
    ).reset_index(drop=True)

    removed_count = original_count - len(cleaned_df)

    issues.append(
        f"Original rows: {original_count}"
    )

    issues.append(
        f"Valid rows remaining: {len(cleaned_df)}"
    )

    issues.append(
        f"Total rows removed: {removed_count}"
    )

    if cleaned_df.empty:
        raise ValueError(
            "No valid market data remains after validation."
        )

    return cleaned_df, issues
