
import numpy as np

from backend.patterns.similarity.sequence_matcher import (
    calculate_dtw_distance,
    calculate_similarity
)

# Similar movements at different price levels
sequence_a = np.array([0.0, 0.05, 0.10, 0.05, 0.02])
sequence_b = np.array([0.0, 0.05, 0.10, 0.05, 0.02])

# Different movement
sequence_c = np.array([0.0, -0.05, -0.10, -0.15, -0.20])

distance = calculate_dtw_distance(
    sequence_a,
    sequence_b
)

similarity = calculate_similarity(
    sequence_a,
    sequence_b
)

different_similarity = calculate_similarity(
    sequence_a,
    sequence_c
)

print("Similar sequence distance:", distance)
print("Similar sequence score:", similarity)
print("Different sequence score:", different_similarity)

assert distance == 0
assert similarity > different_similarity

print("\nAll similarity tests passed!")
