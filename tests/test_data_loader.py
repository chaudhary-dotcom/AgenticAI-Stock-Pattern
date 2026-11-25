
import pandas as pd
from pathlib import Path

from backend.data_loader import load_market_data


# Create sample market data
sample_data = pd.DataFrame({
    "date": pd.date_range(
        start="2025-01-01",
        periods=10
    ),
    "open": [100, 102, 101, 104, 105, 106, 108, 107, 110, 112],
    "high": [105, 104, 106, 107, 108, 110, 111, 112, 114, 115],
    "low": [98, 100, 99, 102, 103, 104, 105, 104, 108, 109],
    "close": [103, 101, 105, 106, 107, 109, 110, 111, 113, 114],
    "volume": [1000, 1200, 1500, 1300, 1800, 2000, 1700, 1900, 2200, 2500]
})


# Create test directory
test_dir = Path("data/processed")
test_dir.mkdir(parents=True, exist_ok=True)


# Save sample CSV and Excel files
csv_path = test_dir / "sample_market.csv"
excel_path = test_dir / "sample_market.xlsx"

sample_data.to_csv(csv_path, index=False)
sample_data.to_excel(excel_path, index=False)


# Test CSV loading
print("\nTESTING CSV LOADER")
csv_df = load_market_data(str(csv_path))
print(csv_df.head())


# Test Excel loading
print("\nTESTING EXCEL LOADER")
excel_df = load_market_data(str(excel_path))
print(excel_df.head())


print("\nBoth file formats loaded successfully!")
