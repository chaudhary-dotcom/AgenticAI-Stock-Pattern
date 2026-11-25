
from backend.agent.nodes.data_node import data_preparation_node
from backend.agent.nodes.clustering_node import clustering_node


state = {
    "user_query": "Discover recurring stock patterns",
    "file_path": "data/processed/analyzer_test.csv",
    "market_data": None,
    "processing_report": [],
    "technical_patterns": [],
    "swing_points": None,
    "historical_matches": [],
    "clustered_sequences": [],
    "final_report": "",
    "error": None
}


# Step 1: Prepare data
result = data_preparation_node(state)
state.update(result)

if state["error"]:
    raise RuntimeError(state["error"])


# Step 2: Perform clustering
result = clustering_node(state)
state.update(result)

if state["error"]:
    raise RuntimeError(state["error"])


# Display results
print("\nCLUSTERING RESULTS")
print("=" * 40)

print("Total sequences:", len(state["clustered_sequences"]))

for cluster_id in sorted(
    set(item["Cluster"] for item in state["clustered_sequences"])
):
    count = sum(
        item["Cluster"] == cluster_id
        for item in state["clustered_sequences"]
    )

    print(f"Cluster {cluster_id}: {count} sequences")
