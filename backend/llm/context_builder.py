
import json


def build_analysis_context(analysis_result: dict) -> str:
    """
    Prepare stock analysis results for the LLM.

    Only relevant summaries are passed to the model.
    """

    if not analysis_result:
        return "No stock analysis results are available."

    market_data = analysis_result.get("market_data")

    # Market data summary
    market_summary = {}

    if market_data is not None and not market_data.empty:

        market_summary = {
            "total_records": len(market_data),
            "columns": list(market_data.columns),
            "start_date": str(market_data["Date"].min()),
            "end_date": str(market_data["Date"].max()),
            "first_closing_price": float(
                market_data["Close"].iloc[0]
            ),
            "latest_closing_price": float(
                market_data["Close"].iloc[-1]
            )
        }

    # Technical patterns
    patterns = analysis_result.get("technical_patterns", [])

    # Historical matches
    historical_matches = analysis_result.get(
        "historical_matches", []
    )

    # Cluster interpretations
    cluster_interpretations = analysis_result.get(
        "cluster_interpretations", {}
    )

    # Swing points
    swing_points = analysis_result.get("swing_points")

    if swing_points is not None and not swing_points.empty:
        swing_points = swing_points.to_dict(orient="records")
    else:
        swing_points = []

    # Processing issues
    processing_report = analysis_result.get(
        "processing_report", []
    )

    context = {
        "market_summary": market_summary,
        "technical_patterns": patterns,
        "swing_points": swing_points,
        "historical_matches": historical_matches,
        "cluster_interpretations": cluster_interpretations,
        "processing_report": processing_report
    }

    return json.dumps(
        context,
        indent=2,
        default=str
    )[:12000]
