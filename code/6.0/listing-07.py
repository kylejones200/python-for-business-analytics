"""Draw association rules whose lift is at least one."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import apriori_itemsets, association_rules_simple

import itertools

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
products = [
    "Bread",
    "Milk",
    "Eggs",
    "Butter",
    "Cheese",
    "Apples",
    "Bananas",
    "Diapers",
    "Beer",
]
rows = []
for tid in range(1, 301):
    basket = set(rng.choice(products, size=int(rng.integers(1, 5)), replace=False))
    if rng.random() < 0.20:
        basket.update({"Diapers", "Beer"})
    if rng.random() < 0.25:
        basket.update({"Bread", "Butter"})
    rows.extend({"TransactionID": tid, "Product": p} for p in sorted(basket))

df_encoded = (
    pd.crosstab(pd.DataFrame(rows)["TransactionID"], pd.DataFrame(rows)["Product"]) > 0
).astype(int)
rules = association_rules_simple(
    apriori_itemsets(df_encoded, min_support=0.05), min_confidence=0.7
)

G = nx.Graph()
for _, rule in rules[rules["lift"] >= 1].iterrows():
    G.add_edge(
        ",".join(sorted(rule["antecedents"])),
        ",".join(sorted(rule["consequents"])),
        weight=round(float(rule["lift"]), 2),
    )

pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="0.85",
    node_size=900,
    font_size=8,
    edge_color="0.4",
)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"))
plt.axis("off")

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch6_association_rules.png", dpi=300, bbox_inches="tight")
plt.close()

print("Saved img/ch6_association_rules.png")
print(f"Rules plotted (lift >= 1): {G.number_of_edges()}")
print(f"Nodes: {G.number_of_nodes()}")
