"""Build an interactive Plotly graph of the unemployment forecast."""

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("fred_series")
df["date"] = pd.to_datetime(df["date"])
series = (
    df.loc[df["UNRATE"].notna(), ["date", "UNRATE"]]
    .set_index("date")["UNRATE"]
    .sort_index()
    .resample("MS")
    .mean()
    .interpolate(limit=2)
    .dropna()
)

fit = ExponentialSmoothing(series, trend="add", seasonal=None).fit()
forecast = fit.forecast(12)
resid_sd = float((series - fit.fittedvalues).dropna().std())
lower = forecast - 1.28 * resid_sd
upper = forecast + 1.28 * resid_sd

fig = go.Figure()
fig.add_trace(
    go.Scatter(x=series.index, y=series.values, mode="lines", name="Observed UNRATE")
)
fig.add_trace(
    go.Scatter(
        x=list(forecast.index) + list(forecast.index[::-1]),
        y=list(upper) + list(lower[::-1]),
        fill="toself",
        fillcolor="rgba(214, 39, 40, 0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Approx. 80% band",
        hoverinfo="skip",
    )
)
fig.add_trace(
    go.Scatter(x=forecast.index, y=forecast.values, mode="lines", name="12-month forecast")
)
fig.update_layout(
    title="Interactive unemployment forecast (Plotly)",
    xaxis_title="Date",
    yaxis_title="Unemployment rate (%)",
    hovermode="x unified",
)

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
html_path = img_dir / "ch7_plotly_forecast.html"
fig.write_html(html_path, include_plotlyjs="cdn")
print("Saved", html_path.relative_to(ROOT))
print("Last observed UNRATE:", round(float(series.iloc[-1]), 2))
print("Forecast horizon:", forecast.index.min().date(), "to", forecast.index.max().date())
print(forecast.round(2).to_string())
