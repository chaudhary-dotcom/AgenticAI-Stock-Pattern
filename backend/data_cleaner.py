
import pandas as pd


def standardize_market_data(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, list[str]]:

    if df.empty:
        raise ValueError("Market data is empty.")

    cleaned_df = df.copy()
    issues = []

    # Normalize column names
    column_aliases = {
        "date": "Date",
        "trading date": "Date",
        "timestamp": "Date",

        "open": "Open",
        "open price": "Open",

        "high": "High",
        "high price": "High",

        "low": "Low",
        "low price": "Low",

        "close": "Close",
        "closing price": "Close",
        "close price": "Close",

        "volume": "Volume",
        "trading volume": "Volume"
    }

    standardized_columns = {}

    for column in cleaned_df.columns:

        normalized_name = (
            str(column)
            .strip()
            .lower()
            .replace("_", " ")
        )

        normalized_name = " ".join(normalized_name.split())

        standardized_columns[column] = column_aliases.get(
            normalized_name,
            str(column).strip()
        )

    cleaned_df = cleaned_df.rename(
        columns=standardized_columns
    )

    # Check for duplicate column names after standardization
    if cleaned_df.columns.duplicated().any():
        raise ValueError(
            "Multiple columns map to the same standard name."
        )

    # Convert Date column
    if "Date" in cleaned_df.columns:

        cleaned_df["Date"] = pd.to_datetime(
            cleaned_df["Date"],
            errors="coerce"
        )

        invalid_dates = cleaned_df["Date"].isna()

        if invalid_dates.any():
            issues.append(
                f"Found {invalid_dates.sum()} invalid dates."
            )

        # Sort valid dates first, leaving invalid dates at the end
        cleaned_df = cleaned_df.sort_values(
            "Date",
            na_position="last"
        ).reset_index(drop=True)

    else:
        issues.append("Date column not found.")

    issues.append(
        "Column names standardized."
    )

    issues.append(
        "Market data sorted by date where available."
    )

    return cleaned_df, issues
