
from pathlib import Path

import numpy as np
import pandas as pd

from backend.patterns.similarity.normalization import extract_price_sequences
from backend.patterns.similarity.clustering import (
    cluster_sequences,
    get_cluster_centers
)
from app.components.clustering_charts import create_cluster_chart


# Generate sample stock data
np.random.seed(42)

dates = pd.date_range(
    start="2025-01-01",
    periods=100
)

close_prices = (
    100
    + np.cumsum(np.random.randn(100) * 2)
)

df = pd.DataFrame({
    "Date": dates,
    "Close": close_prices
})


# Extract historical sequences
sequences = extract_price_sequences(
    df,
    window_size=10,
    step_size=2
)

print("Total sequences:", len(sequences))


# Cluster sequences
clustered_sequences = cluster_sequences(
    sequences,
    n_clusters=4
)

print("Clustering completed!")


# Calculate cluster centers
cluster_centers = get_cluster_centers(
    clustered_sequences
)


# Generate chart
fig = create_cluster_chart(
    clustered_sequences,
    cluster_centers
)


# Save HTML chart
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "cluster_analysis.html"

fig.write_html(str(output_path))

print("Cluster chart saved:", output_path.resolve())
