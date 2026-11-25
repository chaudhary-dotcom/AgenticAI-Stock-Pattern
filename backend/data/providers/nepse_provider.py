
from backend.data.loaders.file_loader import load_stock_file


def load_nepse_data(file_path: str, symbol: str):
    """
    Load NEPSE historical data from CSV or Excel.
    The provider can later be extended to use
    a verified NEPSE data API.
    """

    return load_stock_file(
        file_path=file_path,
        symbol=symbol,
        market="NEPSE"
    )
