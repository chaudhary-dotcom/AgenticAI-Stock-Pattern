
from backend.llm.context_builder import build_analysis_context


def test_context_builder():

    print("\n--- TESTING ANALYSIS CONTEXT BUILDER ---")

    sample_result = {
        "market_data": None,
        "technical_patterns": [
            {
                "Pattern": "Double Bottom",
                "Direction": "BULLISH"
            }
        ],
        "swing_points": None,
        "historical_matches": [],
        "cluster_interpretations": {},
        "processing_report": []
    }

    context = build_analysis_context(sample_result)

    print("\nGENERATED CONTEXT:")
    print(context)

    assert isinstance(context, str)
    assert "Double Bottom" in context
    assert "BULLISH" in context

    print("\nContext builder test passed!")


if __name__ == "__main__":
    test_context_builder()
