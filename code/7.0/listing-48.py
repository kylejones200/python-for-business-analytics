"""Load a short yearly safety series for retrospective change-point analysis."""

import pandas as pd

def load_safety_data():
    years = list(range(1986, 2021))
    rifr = [
        4.22, 8.32, 4.68, 8.77, 2.09, 0.74, 0.00, 0.00, 0.00, 2.76,
        7.60, 2.05, 3.45, 2.42, 2.03, 1.90, 1.61, 2.29, 0.87, 1.20,
        1.32, 1.31, 1.70, 1.62, 0.86, 1.06, 1.08, 0.67, 0.64, 0.88,
        0.98, 0.76, 0.34, 0.54, 0.35,
    ]
    return pd.DataFrame({"Year": years, "RIFR_per_200k": rifr})

df = load_safety_data()
print("Years: {} to {} (n={})".format(int(df["Year"].min()), int(df["Year"].max()), len(df)))
print("RIFR range: {:.2f} to {:.2f}".format(float(df["RIFR_per_200k"].min()), float(df["RIFR_per_200k"].max())))
print("This series is used for retrospective segmentation, not online monitoring.")
