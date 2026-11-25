
import numpy as np
from sklearn.cluster import KMeans


def cluster_sequences(
    sequences: list[dict],
    n_clusters: int = 4,
    random_state: int = 42
) -> list[dict]:
    """
    Group normalized historical price sequences
    using K-Means clustering.
    """

    if not sequences:
        raise ValueError("No sequences provided.")

    if n_clusters < 1:
        raise ValueError("n_clusters must be at least 1.")

    if n_clusters > len(sequences):
        raise ValueError(
            "Number of clusters cannot exceed number of sequences."
        )

    # Extract normalized price movements
    X = np.array([
        sequence["Normalized_Prices"]
        for sequence in sequences
    ], dtype=float)

    if X.ndim != 2:
        raise ValueError("All sequences must have the same length.")

    if not np.all(np.isfinite(X)):
        raise ValueError("Sequences must contain finite values.")

    # Apply K-Means clustering
    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )

    labels = model.fit_predict(X)

    # Attach cluster IDs to original sequence information
    clustered_sequences = []

    for sequence, label in zip(sequences, labels):

        result = sequence.copy()
        result["Cluster"] = int(label)

        clustered_sequences.append(result)

    return clustered_sequences


def get_cluster_summary(
    clustered_sequences: list[dict]
) -> dict:
    """
    Summarize the number of sequences in each cluster.
    """

    if not clustered_sequences:
        return {}

    summary = {}

    for sequence in clustered_sequences:

        cluster_id = sequence["Cluster"]

        if cluster_id not in summary:
            summary[cluster_id] = 0

        summary[cluster_id] += 1

    return summary


def get_cluster_centers(
    clustered_sequences: list[dict]
) -> dict:
    """
    Calculate the average normalized movement
    for each discovered cluster.
    """

    if not clustered_sequences:
        return {}

    centers = {}

    cluster_ids = sorted({
        sequence["Cluster"]
        for sequence in clustered_sequences
    })

    for cluster_id in cluster_ids:

        cluster_data = [
            sequence["Normalized_Prices"]
            for sequence in clustered_sequences
            if sequence["Cluster"] == cluster_id
        ]

        centers[cluster_id] = np.mean(
            np.array(cluster_data),
            axis=0
        )

    return centers
