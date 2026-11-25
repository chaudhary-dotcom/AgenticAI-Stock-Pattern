
from pathlib import Path

from backend.market_analyzer import analyze_market_file
from backend.analysis_report import create_analysis_report


def main():

    # Use the synthetic market data created by the previous test
    input_file = Path("data/processed/analyzer_test.csv")

    if not input_file.exists():
        raise FileNotFoundError(
            "Run tests.test_market_analyzer first."
        )

    # Analyze stock market data
    result = analyze_market_file(str(input_file))

    # Generate complete analysis report
    report_path = create_analysis_report(
        analysis_result=result,
        output_path="data/processed/stock_analysis_report.html"
    )

    print("\nANALYSIS REPORT GENERATED")
    print("=" * 50)

    print("Total market rows:", len(result["data"]))
    print("Total patterns:", len(result["patterns"]))
    print("Total swing points:", len(result["swing_points"]))

    print("\nReport location:")
    print(report_path.resolve())


if __name__ == "__main__":
    main()
