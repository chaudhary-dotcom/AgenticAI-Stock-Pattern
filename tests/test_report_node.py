from backend.agent.nodes.report_node import final_report_node
from backend.agent.nodes.data_node import data_preparation_node
from backend.agent.nodes.pattern_node import technical_pattern_node
from backend.agent.nodes.historical_node import historical_matching_node
from backend.agent.nodes.clustering_node import clustering_node
from backend.agent.nodes.interpretation_node import cluster_interpretation_node


# Initial state
state = {
    "user_query": "Analyze stock market data.",
    "file_path": "data/processed/analyzer_test.csv",
    "market_data": None,
    "processing_report": [],
    "technical_patterns": [],
    "swing_points": None,
    "historical_matches": [],
    "clustered_sequences": [],
    "cluster_interpretations": {},
    "final_report": "",
    "report_path": "",
    "error": None
}

# Execute nodes
for node in [
    data_preparation_node,
    technical_pattern_node,
    historical_matching_node,
    clustering_node,
    interpretation_node if False else cluster_interpretation_node
]:
    state.update(node(state))

    if state.get("error"):
        raise RuntimeError(state["error"])

# Generate final report
state.update(final_report_node(state))

if state.get("error"):
    raise RuntimeError(state["error"])

# Display report
print("\n")
print(state["final_report"])