"""Find frequent itemsets and association rules with lift."""

import itertools

import numpy as np
import pandas as pd

def apriori_itemsets(df_encoded, min_support):
    """Return frequent itemsets from a one-hot basket matrix."""
    if not 0 <= min_support <= 1:
        raise ValueError("min_support must be in [0, 1].")

    supports = {}
    items = list(df_encoded.columns)
    for item in items:
        sup = float(df_encoded[item].mean())
        if sup >= min_support:
            supports[frozenset([item])] = sup

    max_k = min(4, len(items))
    for k in range(2, max_k + 1):
        for combo in itertools.combinations(items, k):
            sup = float(df_encoded.loc[:, combo].all(axis=1).mean())
            if sup >= min_support:
                supports[frozenset(combo)] = sup

    return pd.DataFrame(
        [{"support": sup, "itemsets": itemset} for itemset, sup in supports.items()]
    ).sort_values(["support"], ascending=False, ignore_index=True)

def association_rules_simple(frequent_itemsets, min_confidence):
    """Build rules with consequent support and lift = confidence / support(Z)."""
    if not 0 <= min_confidence <= 1:
        raise ValueError("min_confidence must be in [0, 1].")

    support_map = {
        frozenset(row["itemsets"]): float(row["support"])
        for _, row in frequent_itemsets.iterrows()
    }

    rules = []
    for itemset, sup in support_map.items():
        if len(itemset) < 2:
            continue
        items = list(itemset)
        for r in range(1, len(items)):
            for antecedent in itertools.combinations(items, r):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                sup_a = support_map.get(antecedent)
                sup_c = support_map.get(consequent)
                if not sup_a or not sup_c:
                    continue
                confidence = sup / sup_a
                if confidence >= min_confidence:
                    rules.append(
                        {
                            "antecedents": antecedent,
                            "consequents": consequent,
                            "support": sup,
                            "confidence": confidence,
                            "consequent_support": sup_c,
                            "lift": confidence / sup_c,
                        }
                    )

    columns = [
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "consequent_support",
        "lift",
    ]
    if not rules:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rules).sort_values(
        ["lift", "confidence"], ascending=False, ignore_index=True
    )

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

n_tx = 300
rows = []
for tid in range(1, n_tx + 1):
    basket_size = int(rng.integers(1, 5))
    basket = set(rng.choice(products, size=basket_size, replace=False))
    if rng.random() < 0.20:
        basket.update({"Diapers", "Beer"})
    if rng.random() < 0.25:
        basket.update({"Bread", "Butter"})
    rows.extend({"TransactionID": tid, "Product": p} for p in sorted(basket))

df = pd.DataFrame(rows)
df_encoded = (pd.crosstab(df["TransactionID"], df["Product"]) > 0).astype(int)

frequent_itemsets = apriori_itemsets(df_encoded, min_support=0.05)
rules = association_rules_simple(frequent_itemsets, min_confidence=0.7)

print("Frequent itemsets (top 8):")
print(frequent_itemsets.head(8).to_string(index=False))
print("Association rules (top 8):")
print(rules.head(8).to_string(index=False))
print(f"Rules with lift: {len(rules)}")
