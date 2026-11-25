
from pathlib import Path

from backend.data.loaders.file_loader import (
    load_stock_file
)

from backend.patterns.technical.pattern_detector import (
    detect_all_patterns
)

from app.components.charts import (
    create_pattern_chart
)


def main():

    # Load stock data
    df = load_stock_file(
        file_path="data/sample/sample_stock.csv",
        symbol="TEST",
        market="US"
    )

    print("\nStock data loaded successfully.")
    print("Total records:", len(df))

    # Detect patterns
    results = detect_all_patterns(df)

    patterns = results["patterns"]
    swing_points = results["swing_points"]

    print("\nSWING POINTS")
    print(swing_points)

    print("\nDETECTED PATTERNS")
    print("=" * 50)

    if patterns:

        for pattern in patterns:

            print(
                f"{pattern['Pattern']} | "
                f"{pattern['Direction']} | "
                f"{pattern['Start_Date']} | "
                f"{pattern['End_Date']} | "
                f"Confidence: {pattern['Confidence']}"
            )

    else:

        print("No confirmed patterns detected.")

    # Generate chart
    fig = create_pattern_chart(
        df=df,
        patterns=patterns,
        swing_points=swing_points
    )

    # Save interactive chart
    output_dir = Path("data/processed")
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        output_dir / "pattern_analysis.html"
    )

    fig.write_html(
        str(output_path),
        auto_open=True
    )

    print("\nChart generated successfully!")
    print("Saved at:", output_path.resolve())


if __name__ == "__main__":
    main()
