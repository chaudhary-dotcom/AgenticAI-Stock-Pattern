
from backend.agent.nodes.data_node import data_preparation_node
from backend.agent.nodes.historical_node import historical_matching_node


state = {
    "user_query": "Find similar historical stock patterns",
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


# Step 2: Find historical matches
result = historical_matching_node(state)
state.update(result)

if state["error"]:
    raise RuntimeError(state["error"])


# Display results
print("\nHISTORICAL MATCHING RESULTS")
print("=" * 50)

print("Total matches:", len(state["historical_matches"]))

for index, match in enumerate(state["historical_matches"], start=1):

    print(f"\nMatch {index}")
    print("Start Date:", match["Start_Date"])
    print("End Date:", match["End_Date"])
    print("DTW Distance:", round(match["DTW_Distance"], 4))
    print("Similarity:", round(match["Similarity"], 4))
