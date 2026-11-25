
import numpy as np
import pandas as pd

from backend.patterns.similarity.normalization import (
    extract_price_sequences
)

from backend.patterns.similarity.clustering import (
    cluster_sequences,
    get_cluster_centers
)

from backend.patterns.similarity.cluster_interpreter import (
    interpret_clusters
)

from app.components.cluster_report import create_cluster_report


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


# Step 1: Extract sequences
sequences = extract_price_sequences(
    df,
    window_size=10,
    step_size=2
)

print("Total sequences:", len(sequences))


# Step 2: Cluster sequences
clustered_sequences = cluster_sequences(
    sequences,
    n_clusters=4
)

print("Clustering completed!")


# Step 3: Calculate cluster centers
cluster_centers = get_cluster_centers(
    clustered_sequences
)


# Step 4: Interpret clusters
interpretations = interpret_clusters(
    clustered_sequences
)

print("Cluster interpretation completed!")


# Step 5: Generate complete report
report_path = create_cluster_report(
    clustered_sequences=clustered_sequences,
    cluster_centers=cluster_centers,
    interpretations=interpretations,
    output_path="data/processed/stock_pattern_report.html"
)

print("\nReport generated successfully!")
print("Report location:", report_path.resolve())
