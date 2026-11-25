
from backend.agent.nodes.data_node import data_preparation_node
from backend.agent.nodes.clustering_node import clustering_node
from backend.agent.nodes.interpretation_node import (
    cluster_interpretation_node
)


state = {
    "user_query": "Interpret discovered stock clusters",
    "file_path": "data/processed/analyzer_test.csv",
    "market_data": None,
    "processing_report": [],
    "technical_patterns": [],
    "swing_points": None,
    "historical_matches": [],
    "clustered_sequences": [],
    "cluster_interpretations": [],
    "final_report": "",
    "error": None
}


# Step 1: Prepare data
result = data_preparation_node(state)
state.update(result)

if state["error"]:
    raise RuntimeError(state["error"])


# Step 2: Cluster sequences
result = clustering_node(state)
state.update(result)

if state["error"]:
    raise RuntimeError(state["error"])


# Step 3: Interpret clusters
result = cluster_interpretation_node(state)
state.update(result)

if state["error"]:
    raise RuntimeError(state["error"])


# Display interpretations

print("\nCLUSTER INTERPRETATIONS")
print("=" * 50)

for cluster_id, item in state["cluster_interpretations"].items():

    print(f"\nCluster: {cluster_id}")
    print(f"Direction: {item['Direction']}")
    print(f"Total Sequences: {item['Total_Sequences']}")
    print(f"Average Return: {item['Average_Return']:.2%}")
    print(f"Average Volatility: {item['Average_Volatility']:.2%}")
    print(f"Average Drawdown: {item['Average_Max_Drawdown']:.2%}")
