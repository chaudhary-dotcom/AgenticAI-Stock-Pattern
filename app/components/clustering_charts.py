
import numpy as np
import plotly.graph_objects as go
from plotly.colors import qualitative


def create_cluster_chart(
    clustered_sequences: list[dict],
    cluster_centers: dict
):
    if not clustered_sequences:
        raise ValueError("No clustered sequences provided.")

    fig = go.Figure()

    colors = qualitative.Plotly

    cluster_ids = sorted(cluster_centers.keys())

    for index, cluster_id in enumerate(cluster_ids):

        color = colors[index % len(colors)]

        cluster_data = [
            sequence
            for sequence in clustered_sequences
            if sequence["Cluster"] == cluster_id
        ]

        # Plot individual historical sequences
        for sequence in cluster_data:

            prices = np.asarray(
                sequence["Normalized_Prices"],
                dtype=float
            )

            fig.add_trace(
                go.Scatter(
                    x=list(range(len(prices))),
                    y=prices,
                    mode="lines",
                    line=dict(
                        color=color,
                        width=1
                    ),
                    opacity=0.25,
                    showlegend=False,
                    hoverinfo="skip"
                )
            )

        # Plot the average pattern (cluster center)
        center = cluster_centers[cluster_id]

        fig.add_trace(
            go.Scatter(
                x=list(range(len(center))),
                y=center,
                mode="lines",
                name=f"Cluster {cluster_id} Average (n={len(cluster_data)})",
                line=dict(
                    color=color,
                    width=4
                )
            )
        )

    fig.update_layout(
        title="Historical Stock Pattern Clusters",
        xaxis_title="Time Steps",
        yaxis_title="Normalized Price Movement",
        template="plotly_white",
        hovermode="x unified",
        height=650,
        legend_title="Discovered Patterns"
    )

    return fig
