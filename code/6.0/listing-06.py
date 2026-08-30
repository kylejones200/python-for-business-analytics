"""Recommend items from a fixed user-item matrix."""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

item_names = ["Core", "Plus", "Pro", "Services"]
user_item_matrix = np.array(
    [
        [5, 3, 0, 1],
        [4, 0, 0, 1],
        [1, 1, 0, 5],
        [1, 0, 0, 4],
        [0, 1, 5, 4],
    ],
    dtype=float,
)

item_similarity = cosine_similarity(user_item_matrix.T)


def get_item_recommendations(item_id, n_similar=3):
    """Return the most similar items, excluding the query item."""
    ranked = item_similarity[item_id].argsort()[::-1]
    similar = [idx for idx in ranked if idx != item_id][:n_similar]
    return similar


query_id = 0
recommended = get_item_recommendations(query_id)
print("Item similarity matrix:")
print(np.round(item_similarity, 3))
print(f"Items similar to {item_names[query_id]}:")
for idx in recommended:
    print(
        f"  {item_names[idx]} (cosine={item_similarity[query_id, idx]:.3f})"
    )
