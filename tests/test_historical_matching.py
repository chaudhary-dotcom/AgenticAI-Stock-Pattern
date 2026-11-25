
import numpy as np

from backend.patterns.similarity.normalization import (
    normalize_price_sequence,
    extract_price_sequences
)

from backend.patterns.similarity.sequence_matcher import (
    find_similar_sequences
)

import pandas as pd


# Create sample historical stock data
df = pd.DataFrame({
    "Date": pd.date_range("2025-01-01", periods=60),
    "Close": [
        100, 102, 105, 108, 110, 108, 105, 103, 106, 110,
        112, 115, 118, 116, 113, 110, 108, 111, 115, 119,
        120, 117, 114, 110, 108, 105, 107, 110, 115, 118,
        120, 122, 125, 123, 120, 117, 115, 118, 122, 126,
        128, 125, 122, 119, 115, 112, 110, 113, 117, 121,
        123, 126, 130, 128, 125, 122, 120, 123, 127, 131
    ]
})


# Extract historical sequences
historical_sequences = extract_price_sequences(
    df,
    window_size=10,
    step_size=2
)


# Select the latest sequence as target
target = historical_sequences[-1]
target_sequence = target["Normalized_Prices"]


# Find similar historical movements
matches = find_similar_sequences(
    target_sequence=target_sequence,
    historical_sequences=historical_sequences,
    top_n=5,
    min_similarity=0.50,
    target_start_index=target["Start_Index"],
    target_end_index=target["End_Index"]
)


# Display results
print("\nTOP 5 SIMILAR HISTORICAL PATTERNS")
print("=" * 50)

for index, match in enumerate(matches, start=1):

    print(f"\nMatch {index}")
    print("Start Date:", match["Start_Date"])
    print("End Date:", match["End_Date"])
    print("DTW Distance:", round(match["DTW_Distance"], 4))
    print("Similarity:", round(match["Similarity"], 4))
