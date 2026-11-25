
import numpy as np
from fastdtw import fastdtw


def calculate_dtw_distance(
    sequence_a: np.ndarray,
    sequence_b: np.ndarray
) -> float:
    """
    Calculate Dynamic Time Warping distance
    between two normalized price sequences.
    """

    sequence_a = np.asarray(sequence_a, dtype=float)
    sequence_b = np.asarray(sequence_b, dtype=float)

    if sequence_a.ndim != 1 or sequence_b.ndim != 1:
        raise ValueError("Both sequences must be one-dimensional.")

    if len(sequence_a) == 0 or len(sequence_b) == 0:
        raise ValueError("Sequences cannot be empty.")

    if not np.all(np.isfinite(sequence_a)):
        raise ValueError("Sequence A must contain finite values.")

    if not np.all(np.isfinite(sequence_b)):
        raise ValueError("Sequence B must contain finite values.")

    # Absolute distance works with individual scalar values
    distance, _ = fastdtw(
        sequence_a,
        sequence_b,
        dist=lambda x, y: abs(x - y)
    )

    return float(distance)


def calculate_similarity(
    sequence_a: np.ndarray,
    sequence_b: np.ndarray
) -> float:
    """
    Convert DTW distance into a similarity score from 0 to 1.
    This is a relative score, not a probability.
    """

    distance = calculate_dtw_distance(
        sequence_a,
        sequence_b
    )

    similarity = 1 / (1 + distance)

    return float(similarity)




def find_similar_sequences(
    target_sequence: np.ndarray,
    historical_sequences: list[dict],
    top_n: int = 5,
    min_similarity: float = 0.0,
    target_start_index: int = None,
    target_end_index: int = None
) -> list[dict]:
    """
    Find the most similar non-overlapping historical sequences.
    """

    target_sequence = np.asarray(target_sequence, dtype=float)

    if target_sequence.ndim != 1 or len(target_sequence) == 0:
        raise ValueError("Target sequence must be a non-empty 1D array.")

    if not np.all(np.isfinite(target_sequence)):
        raise ValueError("Target sequence must contain finite values.")

    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if not 0 <= min_similarity <= 1:
        raise ValueError("min_similarity must be between 0 and 1.")

    results = []

    # Find all candidate matches
    for historical in historical_sequences:

        historical_sequence = np.asarray(
            historical["Normalized_Prices"],
            dtype=float
        )

        if historical_sequence.ndim != 1 or len(historical_sequence) == 0:
            continue

        if not np.all(np.isfinite(historical_sequence)):
            continue

        start_idx = historical["Start_Index"]
        end_idx = historical["End_Index"]

        # Exclude windows overlapping the target period
        if (
            target_start_index is not None
            and target_end_index is not None
        ):
            overlaps_target = (
                start_idx <= target_end_index
                and end_idx >= target_start_index
            )

            if overlaps_target:
                continue

        distance = calculate_dtw_distance(
            target_sequence,
            historical_sequence
        )

        similarity = 1 / (1 + distance)

        if similarity < min_similarity:
            continue

        results.append({
            "Start_Index": start_idx,
            "End_Index": end_idx,
            "Start_Date": historical["Start_Date"],
            "End_Date": historical["End_Date"],
            "DTW_Distance": distance,
            "Similarity": similarity,
            "Original_Prices": historical["Original_Prices"],
            "Normalized_Prices": historical_sequence
        })

    # Best matches first
    results.sort(key=lambda item: item["DTW_Distance"])

    # Remove overlapping matches
    selected_matches = []

    for candidate in results:

        overlaps_existing = any(
            candidate["Start_Index"] <= match["End_Index"]
            and candidate["End_Index"] >= match["Start_Index"]
            for match in selected_matches
        )

        if not overlaps_existing:
            selected_matches.append(candidate)

        if len(selected_matches) >= top_n:
            break

    return selected_matches
