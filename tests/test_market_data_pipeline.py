from pathlib import Path
import pandas as pd

from backend.market_data_pipeline import prepare_market_data


def main():

    # Create sample market data
    data = {
        "trading_date": pd.date_range(
            start="2025-01-01",
            periods=10
        ),
        "open_price": [100, 102, 101, 105, 107, 106, 110, 112, 111, 115],
        "HIGH": [105, 104, 106, 108, 110, 112, 113, 115, 116, 118],
        "low_price": [98, 100, 99, 103, 105, 104, 108, 110, 109, 113],
        "closing_price": [103, 101, 105, 107, 109, 110, 112, 114, 115, 117],
        "trading_volume": [1000, 1200, 1100, 1500, 1300, 1600, 1700, 1800, 1900, 2000]
    }

    df = pd.DataFrame(data)

    # Create test files
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "pipeline_test.csv"
    excel_path = output_dir / "pipeline_test.xlsx"

    df.to_csv(csv_path, index=False)
    df.to_excel(excel_path, index=False)

    # Test CSV pipeline
    for file_path in [csv_path, excel_path]:

        print("\n" + "=" * 50)
        print(f"Testing: {file_path.name}")
        print("=" * 50)

        cleaned_df, issues = prepare_market_data(str(file_path))

        print("\nProcessed Data:")
        print(cleaned_df)

        print("\nProcessing Report:")

        for issue in issues:
            print("-", issue)

        print("\nFinal rows:", len(cleaned_df))


if __name__ == "__main__":
    main()