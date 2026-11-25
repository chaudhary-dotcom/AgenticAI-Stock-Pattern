
from backend.data.loaders.file_loader import load_stock_file

from backend.data.providers.us_provider import (
    fetch_us_stock_data
)

from backend.data.providers.nepse_provider import (
    load_nepse_data
)


def main():

    print("\nSTOCK PATTERN DETECTION AGENT")
    print("=" * 40)

    print("1. Fetch US stock data")
    print("2. Load US CSV/Excel")
    print("3. Load NEPSE CSV/Excel")

    choice = input("\nSelect option: ")

    if choice == "1":

        symbol = input("Enter ticker (e.g. AAPL): ")

        df = fetch_us_stock_data(symbol)

    elif choice == "2":

        path = input("Enter file path: ")
        symbol = input("Enter ticker: ")

        df = load_stock_file(
            path,
            symbol,
            "US"
        )

    elif choice == "3":

        path = input("Enter file path: ")
        symbol = input("Enter NEPSE symbol: ")

        df = load_nepse_data(
            path,
            symbol
        )

    else:

        print("Invalid option.")
        return

    print("\nDATA SUCCESSFULLY LOADED")
    print("=" * 40)

    print(df.head())

    print("\nDATA INFORMATION")
    print(df.info())

    print("\nDATA SUMMARY")
    print(df.describe())

    print("\nTotal records:", len(df))


if __name__ == "__main__":
    main()
