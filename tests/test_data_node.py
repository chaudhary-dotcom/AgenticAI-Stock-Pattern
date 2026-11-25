
from backend.agent.nodes.data_node import data_preparation_node

initial_state = {
    "user_query": "Analyze this stock data",
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

result = data_preparation_node(initial_state)

print("\nNODE OUTPUT")
print("=" * 40)

if result["error"]:
    print("Error:", result["error"])
else:
    print("Rows processed:", len(result["market_data"]))
    print("Processing report:")

    for issue in result["processing_report"]:
        print("-", issue)
