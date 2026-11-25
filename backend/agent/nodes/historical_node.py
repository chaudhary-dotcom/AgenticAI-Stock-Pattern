
from backend.agent.state import AgentState

from backend.patterns.similarity.normalization import (
    extract_price_sequences
)

from backend.patterns.similarity.sequence_matcher import (
    find_similar_sequences
)


def historical_matching_node(state: AgentState) -> dict:

    print("\n--- HISTORICAL MATCHING NODE ---")

    try:
        market_data = state["market_data"]

        if market_data is None or market_data.empty:
            raise ValueError("No market data available.")

        sequences = extract_price_sequences(
            market_data,
            window_size=20,
            step_size=1
        )

        # Skip matching if insufficient historical data
        if len(market_data) < 40:

            print("Skipping historical matching: insufficient data.")

            processing_report = state.get("processing_report", [])
            processing_report.append(
                "Historical matching skipped: at least 40 valid rows are required."
            )

            return {
                "historical_matches": [],
                "processing_report": processing_report,
                "error": None
            }

        target = sequences[-1]
        target_sequence = target["Normalized_Prices"]

        print("Target start:", target["Start_Date"])
        print("Target end:", target["End_Date"])

        matches = find_similar_sequences(
            target_sequence=target_sequence,
            historical_sequences=sequences[:-1],
            top_n=5,
            min_similarity=0.0,
            target_start_index=target["Start_Index"],
            target_end_index=target["End_Index"]
        )

        print(f"Found {len(matches)} historical matches.")

        return {
            "historical_matches": matches,
            "error": None
        }

    except Exception as e:

        return {
            "error": str(e)
        }
