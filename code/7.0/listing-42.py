"""Generate a stable KPI series for a control-chart example."""

import numpy as np
import pandas as pd

def generate_kpi_data(n_points=30, base_value=100, noise_level=3, seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start="2024-01-01", periods=n_points, freq="D")
    values = base_value + rng.normal(0, noise_level, n_points)
    return pd.DataFrame({"Date": dates, "KPI_Value": values, "Period": np.arange(1, n_points + 1)})

stable_data = generate_kpi_data()
print(stable_data.head().round(2).to_string(index=False))
print("Mean:", round(float(stable_data["KPI_Value"].mean()), 2))
print("These control-chart data are simulated common-cause variation only.")
