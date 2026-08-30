"""Plot group distributions for the ANOVA example."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

np.random.seed(42)
df = pd.DataFrame(
    {
        "value": np.concatenate(
            [
                np.random.normal(0, 1, 50),
                np.random.normal(0.5, 1, 50),
                np.random.normal(1, 1, 50),
            ]
        ),
        "group": np.repeat(["A", "B", "C"], repeats=50),
    }
)

plt.figure(figsize=(8, 5))
sns.boxplot(x="group", y="value", data=df, color="0.75")
plt.xlabel("Group")
plt.ylabel("Value")
plt.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch5_boxplot_groups.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch5_boxplot_groups.png")
