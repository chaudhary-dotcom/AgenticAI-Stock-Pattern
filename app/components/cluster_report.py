
from pathlib import Path
from html import escape

from app.components.clustering_charts import create_cluster_chart


def create_cluster_report(
    clustered_sequences: list[dict],
    cluster_centers: dict,
    interpretations: dict,
    output_path: str
):
    if not interpretations:
        raise ValueError("No cluster interpretations available.")

    # Generate the interactive chart
    fig = create_cluster_chart(
        clustered_sequences,
        cluster_centers
    )

    chart_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True
    )

    # Generate summary table
    table_rows = ""

    for cluster_id, result in sorted(interpretations.items()):

        table_rows += f"""
        <tr>
            <td>Cluster {cluster_id}</td>
            <td>{escape(result["Direction"])}</td>
            <td>{result["Total_Sequences"]}</td>
            <td>{result["Average_Return"] * 100:.2f}%</td>
            <td>{result["Average_Volatility"] * 100:.3f}%</td>
            <td>{result["Average_Max_Drawdown"] * 100:.2f}%</td>
        </tr>
        """

    # Complete HTML report
    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Stock Pattern Analysis Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background-color: #f5f7fa;
                color: #222;
            }}

            h1, h2 {{
                color: #183153;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin-bottom: 30px;
            }}

            th, td {{
                padding: 14px;
                text-align: center;
                border: 1px solid #ddd;
            }}

            th {{
                background-color: #183153;
                color: white;
            }}

            tr:nth-child(even) {{
                background-color: #f0f3f7;
            }}

            .chart-container {{
                background: white;
                padding: 15px;
                border-radius: 8px;
            }}

            .note {{
                color: #666;
                font-size: 13px;
            }}
        </style>
    </head>

    <body>

        <h1>Stock Pattern Analysis Report</h1>

        <p>
            This report summarizes historical price patterns
            discovered using K-Means clustering.
        </p>

        <h2>Cluster Summary</h2>

        <table>
            <tr>
                <th>Cluster</th>
                <th>Direction</th>
                <th>Total Sequences</th>
                <th>Average Return</th>
                <th>Average Volatility</th>
                <th>Average Max Drawdown</th>
            </tr>

            {table_rows}

        </table>

        <h2>Cluster Visualization</h2>

        <div class="chart-container">
            {chart_html}
        </div>

        <p class="note">
            Note: These results describe historical patterns.
            They are not guaranteed predictions of future
            stock prices or trading signals.
        </p>

    </body>
    </html>
    """

    # Save report
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        report_html,
        encoding="utf-8"
    )

    return output_file
