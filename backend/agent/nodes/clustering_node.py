
from backend.agent.state import AgentState

from backend.patterns.similarity.normalization import (
    extract_price_sequences
)

from backend.patterns.similarity.clustering import (
    cluster_sequences
)


def clustering_node(state: AgentState) -> dict:

    print("\n--- CLUSTERING NODE ---")

    try:
        market_data = state["market_data"]

        if market_data is None or market_data.empty:
            raise ValueError("No market data available.")

        sequences = extract_price_sequences(
            market_data,
            window_size=20,
            step_size=2
        )

        # Skip clustering if insufficient sequences
        if len(sequences) < 4:

            print("Skipping clustering: insufficient data.")

            processing_report = state.get("processing_report", [])
            processing_report.append(
                "Clustering skipped: at least 4 price sequences are required."
            )

            return {
                "clustered_sequences": [],
                "processing_report": processing_report,
                "error": None
            }

        clustered_sequences = cluster_sequences(
            sequences,
            n_clusters=4,
            random_state=42
        )

        print(f"Total sequences: {len(clustered_sequences)}")

        return {
            "clustered_sequences": clustered_sequences,
            "error": None
        }

    except Exception as e:

        return {
            "error": str(e)
        }
