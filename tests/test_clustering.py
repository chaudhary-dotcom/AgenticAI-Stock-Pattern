
import pandas as pd
import numpy as np

from backend.patterns.similarity.normalization import (
    extract_price_sequences
)

from backend.patterns.similarity.clustering import (
    cluster_sequences,
    get_cluster_summary,
    get_cluster_centers
)


def test_clustering():

    # Create sample historical stock data
    df = pd.DataFrame({
        "Date": pd.date_range("2025-01-01", periods=100),
        "Close": [
            100, 102, 105, 108, 110, 108, 105, 103, 106, 110,
            112, 115, 118, 116, 113, 110, 108, 111, 115, 119,
            120, 117, 114, 110, 108, 105, 107, 110, 115, 118,
            120, 122, 125, 123, 120, 117, 115, 118, 122, 126,
            128, 125, 122, 119, 115, 112, 110, 113, 117, 121,
            123, 126, 130, 128, 125, 122, 120, 123, 127, 131,
            135, 138, 140, 137, 134, 130, 128, 132, 136, 140,
            142, 139, 135, 132, 130, 127, 125, 128, 132, 136,
            138, 141, 145, 142, 139, 136, 134, 137, 141, 145,
            148, 145, 142, 139, 136, 133, 130, 134, 138, 142
        ]
    })

    # Extract historical sequences
    sequences = extract_price_sequences(
        df,
        window_size=10,
        step_size=2
    )

    assert len(sequences) > 0, "No sequences were extracted"

    # Discover recurring groups
    clustered = cluster_sequences(
        sequences,
        n_clusters=4
    )

    assert len(clustered) == len(sequences)
    assert all("Cluster" in item for item in clustered)

    cluster_ids = {
        item["Cluster"] for item in clustered
    }

    assert cluster_ids.issubset({0, 1, 2, 3})
    assert len(cluster_ids) == 4, "Expected four non-empty clusters"

    # Display cluster summary
    summary = get_cluster_summary(clustered)

    assert len(summary) == 4
    assert sum(summary.values()) == len(clustered)

    # Display representative movements
    centers = get_cluster_centers(clustered)

    assert len(centers) == 4

    for cluster_id, center in centers.items():
        assert len(center) == 10
        assert np.isfinite(center).all()

    print("Total sequences:", len(sequences))
    print("\nCluster summary:", summary)
    print("\nAll clustering assertions passed!")


if __name__ == "__main__":
    test_clustering()
