
import numpy as np
import pandas as pd

from backend.patterns.similarity.normalization import (
    extract_price_sequences
)

from backend.patterns.similarity.clustering import (
    cluster_sequences
)

from backend.patterns.similarity.cluster_interpreter import (
    interpret_clusters
)


# Generate sample stock data
np.random.seed(42)

dates = pd.date_range(
    start="2025-01-01",
    periods=100
)

close_prices = (
    100 + np.cumsum(np.random.randn(100) * 2)
)

df = pd.DataFrame({
    "Date": dates,
    "Close": close_prices
})


# Extract sequences
sequences = extract_price_sequences(
    df,
    window_size=10,
    step_size=2
)


# Cluster sequences
clustered_sequences = cluster_sequences(
    sequences,
    n_clusters=4
)


# Interpret clusters
interpretations = interpret_clusters(
    clustered_sequences
)


# Display results
print("\nCLUSTER INTERPRETATION")
print("=" * 50)

for cluster_id, result in interpretations.items():

    print(f"\nCluster {cluster_id}")
    print("-" * 30)

    print("Total Sequences:", result["Total_Sequences"])
    print("Direction:", result["Direction"])

    print(
        "Average Return:",
        f'{result["Average_Return"] * 100:.2f}%'
    )

    print(
        "Average Volatility:",
        f'{result["Average_Volatility"] * 100:.3f}%'
    )

    print(
        "Average Maximum Drawdown:",
        f'{result["Average_Max_Drawdown"] * 100:.2f}%'
    )
