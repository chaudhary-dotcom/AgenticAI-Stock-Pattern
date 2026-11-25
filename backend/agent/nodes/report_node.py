from backend.agent.state import AgentState
from pathlib import Path

def final_report_node(state: AgentState) -> dict:

    print("\n--- FINAL REPORT NODE ---")

    try:
        report = []

        # 1. Report title
        report.append("=" * 60)
        report.append("STOCK PATTERN ANALYSIS REPORT")
        report.append("=" * 60)

        # 2. Data processing information
        report.append("\n1. DATA PROCESSING")

        report.append(
            f"Total Valid Rows: {len(state['market_data'])}"
        )

        if state["processing_report"]:
            report.append("\nProcessing Issues:")

            for issue in state["processing_report"]:
                report.append(f"- {issue}")
        else:
            report.append("No data processing issues found.")

        # 3. Technical patterns
        report.append("\n2. TECHNICAL PATTERNS")

        patterns = state["technical_patterns"]

        report.append(f"Total Patterns Detected: {len(patterns)}")

        for index, pattern in enumerate(patterns, start=1):

            report.append(f"\nPattern {index}")

            for key, value in pattern.items():
                report.append(f"{key}: {value}")

        # 4. Historical matches
        report.append("\n3. HISTORICAL PATTERN MATCHES")

        matches = state["historical_matches"]

        report.append(f"Total Matches: {len(matches)}")

        if matches:

            for index, match in enumerate(matches, start=1):

                report.append(f"\nMatch {index}")
                report.append(f"Start Date: {match['Start_Date']}")
                report.append(f"End Date: {match['End_Date']}")
                report.append(f"Similarity: {match['Similarity']:.4f}")
                report.append(f"DTW Distance: {match['DTW_Distance']:.4f}")

        else:
            report.append("No similar historical patterns found.")

        # 5. Cluster interpretations
        report.append("\n4. MARKET PATTERN CLUSTERS")

        interpretations = state["cluster_interpretations"]

        if interpretations:

            for cluster_id, item in interpretations.items():

                report.append(f"\nCluster {cluster_id}")
                report.append(f"Direction: {item['Direction']}")
                report.append(f"Sequences: {item['Total_Sequences']}")
                report.append(f"Average Return: {item['Average_Return']:.2%}")
                report.append(
                    f"Average Volatility: {item['Average_Volatility']:.2%}"
                )
                report.append(
                    f"Average Drawdown: {item['Average_Max_Drawdown']:.2%}"
                )

        else:
            report.append("No clusters available for interpretation.")

        # 6. Final note
        report.append("\n" + "=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)

        final_report = "\n".join(report)

        # Save report to project directory
        output_path = Path("data/processed/agent_report.txt")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(
        final_report,
        encoding="utf-8"
        )

        print(f"Report saved successfully: {output_path}")

        print("Final report generated successfully.")

        return {
            "final_report": final_report,
            "report_path": str(output_path),
            "error": None
        }

    except Exception as e:

        return {
            "error": str(e)
        }