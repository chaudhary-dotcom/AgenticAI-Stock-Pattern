from langgraph.graph import StateGraph, START, END

from backend.agent.state import AgentState
from backend.agent.nodes.report_node import final_report_node
from backend.agent.nodes.data_node import data_preparation_node
from backend.agent.nodes.pattern_node import technical_pattern_node
from backend.agent.nodes.historical_node import historical_matching_node
from backend.agent.nodes.clustering_node import clustering_node
from backend.agent.nodes.interpretation_node import cluster_interpretation_node


# Check whether the previous node encountered an error
def check_error(state: AgentState):
    if state.get("error"):
        return "stop"

    return "continue"


def build_stock_agent():

    workflow = StateGraph(AgentState)

    # Register nodes
    workflow.add_node("data_preparation", data_preparation_node)
    workflow.add_node("technical_patterns", technical_pattern_node)
    workflow.add_node("historical_matching", historical_matching_node)
    workflow.add_node("clustering", clustering_node)
    workflow.add_node("cluster_interpretation", cluster_interpretation_node)
    workflow.add_node("final_report", final_report_node)

    # Starting point
    workflow.add_edge(START, "data_preparation")

    # Conditional routing
    workflow.add_conditional_edges(
        "data_preparation",
        check_error,
        {
            "continue": "technical_patterns",
            "stop": END
        }
    )

    workflow.add_conditional_edges(
        "technical_patterns",
        check_error,
        {
            "continue": "historical_matching",
            "stop": END
        }
    )

    workflow.add_conditional_edges(
        "historical_matching",
        check_error,
        {
            "continue": "clustering",
            "stop": END
        }
    )

    workflow.add_conditional_edges(
        "clustering",
        check_error,
        {
            "continue": "cluster_interpretation",
            "stop": END
        }
    )

    workflow.add_conditional_edges(
        "cluster_interpretation",
        check_error,
        {
            "continue": "final_report",
            "stop": END
        }
    )

    workflow.add_conditional_edges(
        "final_report",
        check_error,
        {
        "continue": END,
        "stop": END
        }
    )

    return workflow.compile()