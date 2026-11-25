
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd

from backend.agent.graph import build_stock_agent


def create_sample_data(file_path):

    total_days = 120
    x = np.arange(total_days)

    closing_prices = (
        100
        + 0.08 * x
        + 8 * np.sin(x * 2 * np.pi / 20)
    )

    opening_prices = (
        closing_prices
        - 1.2 * np.cos(x * 0.7)
    )

    high_prices = (
        np.maximum(opening_prices, closing_prices) + 1.5
    )

    low_prices = (
        np.minimum(opening_prices, closing_prices) - 1.5
    )

    df = pd.DataFrame({
        "Date": pd.date_range(
            start="2025-01-01",
            periods=total_days
        ),
        "Open": opening_prices,
        "High": high_prices,
        "Low": low_prices,
        "Close": closing_prices,
        "Volume": 1000 + (x * 15)
    })

    df.to_csv(file_path, index=False)


def run_agent(file_path):

    agent = build_stock_agent()

    initial_state = {
        "user_query": "Analyze this stock market data.",
        "file_path": str(file_path),
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

    result = agent.invoke(initial_state)

    # Verify agent execution
    assert result["error"] is None, (
        f"Agent failed: {result['error']}"
    )

    # Verify final report
    assert result["final_report"], "Final report is empty"

    # Verify report file
    assert result["report_path"], "Report path is missing"
    assert Path(result["report_path"]).exists(), (
        "Report file was not created"
    )

    # Verify output structures
    assert isinstance(result["technical_patterns"], list)
    assert isinstance(result["historical_matches"], list)
    assert isinstance(result["clustered_sequences"], list)
    assert isinstance(result["cluster_interpretations"], dict)

    print("\nAll agent graph assertions passed!")

    print("\n========== FINAL AGENT RESULTS ==========")
    print("Technical Patterns:", len(result["technical_patterns"]))
    print("Swing Points:", len(result["swing_points"])
          if result["swing_points"] is not None else 0)
    print("Historical Matches:", len(result["historical_matches"]))
    print("Clustered Sequences:", len(result["clustered_sequences"]))
    print("Cluster Interpretations:", len(result["cluster_interpretations"]))
    print("Report Path:", result["report_path"])

    return result


def test_agent_graph(tmp_path):

    # Create independent test data
    file_path = tmp_path / "sample_stock.csv"
    create_sample_data(file_path)

    result = run_agent(file_path)

    assert result["error"] is None


def main():

    # Allow running this test directly as a Python module
    with tempfile.TemporaryDirectory() as temp_dir:

        file_path = Path(temp_dir) / "sample_stock.csv"

        create_sample_data(file_path)
        run_agent(file_path)


if __name__ == "__main__":
    main()
