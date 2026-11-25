
from pathlib import Path
import pandas as pd


def load_market_data(file_path: str) -> pd.DataFrame:
    """
    Load historical stock market data from CSV or Excel.
    """

    path = Path(file_path)

    # Check whether file exists
    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    # Check file extension
    extension = path.suffix.lower()

    if extension == ".csv":
        df = pd.read_csv(path)

    elif extension in [".xlsx", ".xls"]:
        df = pd.read_excel(path)

    else:
        raise ValueError(
            "Unsupported file format. Use CSV or Excel."
        )

    # Check whether file contains data
    if df.empty:
        raise ValueError(
            "The uploaded file contains no data."
        )

    # Standardize column names
    df.columns = [
        str(column).strip().capitalize()
        for column in df.columns
    ]

    return df
