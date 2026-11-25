
from backend.agent.state import AgentState
from backend.patterns.technical.pattern_detector import detect_all_patterns


def technical_pattern_node(state: AgentState) -> dict:

    print("\n--- TECHNICAL PATTERN NODE ---")

    try:
        # Get processed market data
        market_data = state["market_data"]

        if market_data is None or market_data.empty:
            raise ValueError("No market data available for pattern detection.")

        # Detect technical patterns
        results = detect_all_patterns(market_data)

        # Extract patterns and swing points
        patterns = results["patterns"]
        swing_points = results["swing_points"]

        print(f"Detected {len(patterns)} technical patterns.")
        print(f"Detected {len(swing_points)} swing points.")

        # Return updated state
        return {
            "technical_patterns": patterns,
            "swing_points": swing_points,
            "error": None
        }

    except Exception as e:

        return {
            "error": str(e)
        }
