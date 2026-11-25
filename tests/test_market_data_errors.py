
import pandas as pd

from backend.data_validator import validate_market_data


def main():

    # Deliberately create corrupted market data
    data = {
        "Date": [
            "2025-01-01",
            "2025-01-02",
            "invalid-date",
            "2025-01-04",
            "2025-01-04",
            "2025-01-06",
            "2025-01-07",
            "2025-01-08"
        ],
        "Open": [100, 102, 103, 105, 107, -10, 110, 112],
        "High": [105, 104, 108, 108, 110, 112, 108, 115],
        "Low": [98, 100, 101, 103, 105, 104, 109, 110],
        "Close": [103, 101, 106, 107, 109, 110, 112, 114],
        "Volume": [1000, 1200, 1100, 1500, 1300, 1600, 1700, -500]
    }

    df = pd.DataFrame(data)

    print("\nORIGINAL CORRUPTED DATA")
    print(df)

    # Validate market data
    cleaned_df, issues = validate_market_data(df)

    print("\nVALIDATED DATA")
    print(cleaned_df)

    print("\nVALIDATION REPORT")

    for issue in issues:
        print("-", issue)

    print("\nFINAL ROW COUNT:", len(cleaned_df))


if __name__ == "__main__":
    main()
