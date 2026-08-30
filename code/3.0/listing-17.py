"""Create an interactive revenue chart with Plotly."""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

np.random.seed(123)
dates = pd.date_range("2023-01-01", periods=100, freq="D")
values = (
    100
    + 2 * np.arange(100)
    + 10 * np.sin(np.linspace(0, 10, 100))
    + np.random.normal(0, 5, 100)
)

fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=values, mode="lines", name="Revenue"))
fig.update_layout(
    title="Interactive Revenue Trend",
    xaxis_title="Date",
    yaxis_title="Revenue ($1000s)",
    hovermode="x unified",
)

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
out = img_dir / "ch3_interactive_revenue.html"
fig.write_html(str(out))
print(f"Saved {out}")
