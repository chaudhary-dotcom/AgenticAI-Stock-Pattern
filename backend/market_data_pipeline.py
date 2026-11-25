import pandas as pd

from backend.data_loader import load_market_data
from backend.data_cleaner import standardize_market_data
from backend.data_validator import validate_market_data


def prepare_market_data(
    file_path: str
) -> tuple[pd.DataFrame, list[str]]:

    # Step 1: Load CSV or Excel data
    df = load_market_data(file_path)

    # Step 2: Standardize column names and dates
    standardized_df, cleaning_issues = standardize_market_data(df)

    # Step 3: Validate OHLCV data
    validated_df, validation_issues = validate_market_data(
        standardized_df
    )

    # Combine all processing messages
    all_issues = cleaning_issues + validation_issues

    return validated_df, all_issues