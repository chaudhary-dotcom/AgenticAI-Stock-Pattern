
from typing import TypedDict, Optional, Any
import pandas as pd


class AgentState(TypedDict):

    # User's request
    user_query: str

    # Input market data
    file_path: str

    # Processed market data
    market_data: Optional[pd.DataFrame]

    # Data preparation issues
    processing_report: list[str]

    # Technical analysis results
    technical_patterns: list[dict]

    # Swing high and low points
    swing_points: Optional[pd.DataFrame]

    # Similar historical patterns
    historical_matches: list[dict]

    # Clustering results
    clustered_sequences: list[dict]

    cluster_interpretations: list[int, dict]

    # Final analysis
    final_report: str

    report_path: str

    # Error information
    error: Optional[str]