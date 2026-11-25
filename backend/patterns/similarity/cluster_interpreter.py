
import numpy as np


def interpret_clusters(
    clustered_sequences: list[dict]
) -> dict:

    if not clustered_sequences:
        return {}

    interpretations = {}

    cluster_ids = sorted({
        sequence["Cluster"]
        for sequence in clustered_sequences
    })

    for cluster_id in cluster_ids:

        cluster_data = [
            sequence
            for sequence in clustered_sequences
            if sequence["Cluster"] == cluster_id
        ]

        final_returns = []
        volatilities = []
        drawdowns = []

        for sequence in cluster_data:

            prices = np.asarray(
                sequence["Normalized_Prices"],
                dtype=float
            )

            if prices.ndim != 1 or len(prices) < 2:
                continue

            if not np.all(np.isfinite(prices)):
                continue

            # Overall movement from starting price
            final_returns.append(prices[-1])

            # Volatility: standard deviation of price changes
            price_changes = np.diff(prices)
            volatilities.append(np.std(price_changes))

            # Maximum drawdown
            running_max = np.maximum.accumulate(prices)
            sequence_drawdown = prices - running_max

            drawdowns.append(np.min(sequence_drawdown))

        if not final_returns:
            continue

        average_return = float(np.mean(final_returns))
        average_volatility = float(np.mean(volatilities))
        average_drawdown = float(np.mean(drawdowns))

        # Interpret the average price movement
        if average_return > 0.02:
            direction = "UPWARD"
        elif average_return < -0.02:
            direction = "DOWNWARD"
        else:
            direction = "SIDEWAYS"

        interpretations[cluster_id] = {
            "Cluster": cluster_id,
            "Total_Sequences": len(final_returns),
            "Direction": direction,
            "Average_Return": average_return,
            "Average_Volatility": average_volatility,
            "Average_Max_Drawdown": average_drawdown
        }

    return interpretations
