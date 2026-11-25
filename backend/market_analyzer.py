
from backend.market_data_pipeline import prepare_market_data
from backend.patterns.technical.pattern_detector import detect_all_patterns
from app.components.charts import create_pattern_chart


def analyze_market_file(file_path: str):

    # Step 1: Prepare market data
    df, processing_report = prepare_market_data(file_path)

    # Step 2: Detect all technical patterns
    detection_results = detect_all_patterns(df)

    swing_points = detection_results["swing_points"]
    patterns = detection_results["patterns"]

    # Step 3: Generate chart
    fig = create_pattern_chart(
        df=df,
        patterns=patterns,
        swing_points=swing_points
    )

    return {
        "data": df,
        "processing_report": processing_report,
        "patterns": patterns,
        "swing_points": swing_points,
        "chart": fig
    }
