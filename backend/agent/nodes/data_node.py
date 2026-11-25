
from backend.agent.state import AgentState
from backend.market_data_pipeline import prepare_market_data


def data_preparation_node(state: AgentState) -> dict:

    print("\n--- DATA PREPARATION NODE ---")

    try:
        # 1. Get the uploaded file path
        file_path = state["file_path"]

        # 2. Prepare and validate market data
        market_data, processing_report = prepare_market_data(file_path)

        print(f"Successfully processed {len(market_data)} rows.")

        # 3. Return updated state fields
        return {
            "market_data": market_data,
            "processing_report": processing_report,
            "error": None
        }

    except Exception as e:

        return {
            "error": str(e)
        }
