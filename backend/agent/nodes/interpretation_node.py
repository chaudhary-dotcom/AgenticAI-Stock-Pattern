
from backend.agent.state import AgentState

from backend.patterns.similarity.cluster_interpreter import (
    interpret_clusters
)


def cluster_interpretation_node(state: AgentState) -> dict:

    print("\n--- CLUSTER INTERPRETATION NODE ---")

    try:
        clustered_sequences = state["clustered_sequences"]

        # Skip interpretation if clustering was skipped
        if not clustered_sequences:

            print("Skipping interpretation: no clusters available.")

            processing_report = list(
                state.get("processing_report", [])
            )

            processing_report.append(
                "Cluster interpretation skipped: no clusters available."
            )

            return {
                "cluster_interpretations": {},
                "processing_report": processing_report,
                "error": None
            }

        interpretations = interpret_clusters(
            clustered_sequences
        )

        print(f"Interpreted {len(interpretations)} clusters.")

        return {
            "cluster_interpretations": interpretations,
            "error": None
        }

    except Exception as e:

        return {
            "error": str(e)
        }
