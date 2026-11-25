
from backend.patterns.similarity.normalization import (
    normalize_price_sequence,
    extract_price_sequences
)

import pandas as pd


# Test 1: Compare different price levels
stock_a = [100, 105, 110, 105]
stock_b = [500, 525, 550, 525]

normalized_a = normalize_price_sequence(stock_a)
normalized_b = normalize_price_sequence(stock_b)

print("Stock A:", normalized_a)
print("Stock B:", normalized_b)

print(
    "Are movements similar?",
    (normalized_a == normalized_b).all()
)


# Test 2: Extract historical sequences
df = pd.DataFrame({
    "Date": pd.date_range("2026-01-01", periods=30),
    "Close": range(100, 130)
})

sequences = extract_price_sequences(
    df,
    window_size=10,
    step_size=5
)

print("\nTotal sequences:", len(sequences))

for sequence in sequences[:2]:
    print(
        sequence["Start_Index"],
        sequence["End_Index"],
        sequence["Normalized_Prices"]
    )
