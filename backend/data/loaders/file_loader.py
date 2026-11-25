
import pandas as pd

from pathlib import Path

from backend.data.preprocessing.cleaner import (
    standardize_stock_data
)


def load_stock_file(
    file_path: str,
    symbol: str,
    market: str
) -> pd.DataFrame:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    extension = path.suffix.lower()

    if extension == ".csv":
        df = pd.read_csv(path)

    elif extension in [".xlsx", ".xls"]:
        df = pd.read_excel(path)

    else:
        raise ValueError(
            "Only CSV and Excel files are supported."
        )

    return standardize_stock_data(
        df=df,
        symbol=symbol,
        market=market
    )
