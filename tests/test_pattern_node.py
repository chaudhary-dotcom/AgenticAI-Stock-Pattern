
from backend.agent.nodes.data_node import data_preparation_node
from backend.agent.nodes.pattern_node import technical_pattern_node


# Initial state
state = {
    "user_query": "Detect technical patterns",
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
data_result = data_preparation_node(state)
state.update(data_result)

if state["error"]:
    raise RuntimeError(state["error"])


# Step 2: Detect technical patterns
pattern_result = technical_pattern_node(state)
state.update(pattern_result)

if state["error"]:
    raise RuntimeError(state["error"])


# Display results
print("\nPATTERN NODE OUTPUT")
print("=" * 40)

print("Total patterns:", len(state["technical_patterns"]))
print("Total swing points:", len(state["swing_points"]))

for pattern in state["technical_patterns"]:
    print(
        pattern.get("Pattern"),
        "|",
        pattern.get("Direction")
    )
