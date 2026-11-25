
from pathlib import Path
import pandas as pd
import html


def create_analysis_report(
    analysis_result: dict,
    output_path: str
):

    df = analysis_result["data"]
    patterns = analysis_result["patterns"]
    swing_points = analysis_result["swing_points"]
    chart = analysis_result["chart"]
    processing_report = analysis_result["processing_report"]

    # Calculate pattern statistics
    total_patterns = len(patterns)

    bullish_patterns = sum(
        1 for pattern in patterns
        if pattern["Direction"] == "BULLISH"
    )

    bearish_patterns = sum(
        1 for pattern in patterns
        if pattern["Direction"] == "BEARISH"
    )

    # Calculate swing point statistics
    swing_highs = (
        (swing_points["Type"] == "HIGH").sum()
        if not swing_points.empty else 0
    )

    swing_lows = (
        (swing_points["Type"] == "LOW").sum()
        if not swing_points.empty else 0
    )

    # Convert patterns into an HTML table
    if patterns:
        pattern_df = pd.DataFrame(patterns)

        display_columns = [
            column for column in [
                "Pattern",
                "Direction",
                "Start_Date",
                "End_Date",
                "Confidence",
                "Confirmed"
            ]
            if column in pattern_df.columns
        ]

        pattern_table = pattern_df[
            display_columns
        ].to_html(index=False, border=0)

    else:
        pattern_table = "<p>No technical patterns detected.</p>"

    # Convert processing report into HTML
    processing_html = "".join(
        f"<li>{html.escape(str(issue))}</li>"
        for issue in processing_report
    )

    # Generate interactive chart HTML
    chart_html = chart.to_html(
        full_html=False,
        include_plotlyjs=True
    )

    # Build complete HTML report
    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stock Pattern Analysis Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 35px;
                background: #f5f7fa;
                color: #222;
            }}

            h1, h2 {{
                color: #1e293b;
            }}

            .summary {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
            }}

            .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }}

            .card h2 {{
                font-size: 28px;
                margin: 5px;
            }}

            .section {{
                background: white;
                padding: 20px;
                margin-top: 25px;
                border-radius: 10px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}

            th {{
                background: #e2e8f0;
            }}

            @media (max-width: 700px) {{
                .summary {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>

    <body>

        <h1>Stock Pattern Analysis Report</h1>

        <p>Total market data rows: {len(df)}</p>

        <div class="summary">

            <div class="card">
                <h2>{total_patterns}</h2>
                <p>Total Patterns</p>
            </div>

            <div class="card">
                <h2>{bullish_patterns}</h2>
                <p>Bullish Patterns</p>
            </div>

            <div class="card">
                <h2>{bearish_patterns}</h2>
                <p>Bearish Patterns</p>
            </div>

            <div class="card">
                <h2>{swing_highs}</h2>
                <p>Swing Highs</p>
            </div>

            <div class="card">
                <h2>{swing_lows}</h2>
                <p>Swing Lows</p>
            </div>

            <div class="card">
                <h2>{len(df)}</h2>
                <p>Trading Records</p>
            </div>

        </div>

        <div class="section">
            <h2>Detected Technical Patterns</h2>
            {pattern_table}
        </div>

        <div class="section">
            <h2>Interactive Stock Chart</h2>
            {chart_html}
        </div>

        <div class="section">
            <h2>Data Processing Report</h2>
            <ul>
                {processing_html}
            </ul>
        </div>

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
