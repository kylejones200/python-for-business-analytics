"""Shared helpers for the worked examples in *Business Analytics with Python*.

Each function here is printed in full in the chapter where it is introduced,
because reading the implementation is part of the lesson. Later listings that
need the same routine import it from this module instead of reprinting it.

Where a chapter first shows a helper:

    spherical_gamma, ordinary_krige, ordinary_krige_points  Chapter 8
    sse, cost, binary_segmentation                          Chapter 7
    kaplan_meier                                            Chapter 7
    load_safety_data                                        Chapter 7
    generate_kpi_data, calculate_control_limits             Chapter 7
    make_synthetic_turbofan, make_cox_units, make_weibull_units  Chapter 7
    apriori_itemsets, association_rules_simple              Chapter 6

Nothing here depends on anything outside numpy, pandas and scipy.
"""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
from scipy import stats

__all__ = [
    "spherical_gamma", "ordinary_krige", "ordinary_krige_points",
    "sse", "cost", "binary_segmentation", "kaplan_meier",
    "load_safety_data", "generate_kpi_data", "calculate_control_limits",
    "make_synthetic_turbofan", "unit_level", "make_cox_units", "make_weibull_units",
    "apriori_itemsets", "association_rules_simple",
]


# --------------------------------------------------------------------------
# Chapter 8: geostatistics
# --------------------------------------------------------------------------

def spherical_gamma(h, nugget, psill, rng):
    """Spherical variogram model evaluated at lag distances ``h``."""
    h = np.asarray(h, dtype=float)
    out = np.full_like(h, nugget + psill, dtype=float)
    mask = h < rng
    hr = h[mask] / rng
    out[mask] = nugget + psill * (1.5 * hr - 0.5 * hr**3)
    out[h == 0] = 0.0
    return out


def _krige_weights(x, y, x0, y0, nugget, psill, rng):
    """Solve the ordinary-kriging system at one target location."""
    from scipy.spatial import distance_matrix

    n = len(x)
    d_obs = distance_matrix(np.column_stack([x, y]), np.column_stack([x, y]))
    A = np.ones((n + 1, n + 1))
    A[:n, :n] = spherical_gamma(d_obs, nugget, psill, rng)
    A[-1, -1] = 0.0
    d0 = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
    b = np.ones(n + 1)
    b[:n] = spherical_gamma(d0, nugget, psill, rng)
    try:
        w = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        w = np.linalg.lstsq(A, b, rcond=None)[0]
    return w, b


def ordinary_krige(x, y, z, x0, y0, nugget, psill, rng,
                   return_variance=False, clip=None):
    """Predict ``z`` at one location under a fitted spherical variogram.

    Args:
        return_variance: also return the kriging variance.
        clip: optional ``(low, high)`` bound, used for indicator kriging.
    """
    w, b = _krige_weights(x, y, x0, y0, nugget, psill, rng)
    n = len(z)
    pred = float(np.dot(w[:n], z))
    if clip is not None:
        pred = float(np.clip(pred, clip[0], clip[1]))
    if return_variance:
        return pred, max(float(np.dot(w, b)), 0.0)
    return pred


def ordinary_krige_points(x_tr, y_tr, z_tr, x_te, y_te, nugget, psill, rng,
                          return_std=False):
    """Predict at many locations from a single training set."""
    preds, stds = [], []
    for x0, y0 in zip(x_te, y_te):
        w, b = _krige_weights(x_tr, y_tr, x0, y0, nugget, psill, rng)
        n = len(z_tr)
        preds.append(float(np.dot(w[:n], z_tr)))
        if return_std:
            stds.append(float(np.sqrt(max(float(np.dot(w, b)), 0.0))))
    if return_std:
        return np.asarray(preds), np.asarray(stds)
    return np.asarray(preds)


# --------------------------------------------------------------------------
# Chapter 7: change-point detection
# --------------------------------------------------------------------------

def sse(values):
    """Sum of squared deviations from the mean of ``values``."""
    values = np.asarray(values, dtype=float)
    return float(np.sum((values - values.mean()) ** 2)) if len(values) else 0.0


def cost(values, kind="l2"):
    """Segment cost. ``l2`` penalises squared error, ``l1`` absolute error."""
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return 0.0
    if kind == "l2":
        return float(np.sum((values - values.mean()) ** 2))
    return float(np.sum(np.abs(values - np.median(values))))


def binary_segmentation(signal, n_bkps=3, min_size=3, kind="l2",
                        include_bounds=False):
    """Retrospective binary segmentation of a one-dimensional signal.

    Args:
        include_bounds: return ``[0, ..., n]`` rather than the interior
            breakpoints alone.
    """
    signal = np.asarray(signal, dtype=float)
    n = len(signal)
    breakpoints = [0, n]
    for _ in range(n_bkps):
        best_gain, best_idx = 0.0, None
        for i in range(len(breakpoints) - 1):
            start, end = breakpoints[i], breakpoints[i + 1]
            if end - start < 2 * min_size:
                continue
            parent = cost(signal[start:end], kind)
            for tau in range(start + min_size, end - min_size + 1):
                gain = parent - cost(signal[start:tau], kind) - cost(signal[tau:end], kind)
                if gain > best_gain:
                    best_gain, best_idx = gain, tau
        if best_idx is None:
            break
        breakpoints.append(best_idx)
        breakpoints = sorted(breakpoints)
    return breakpoints if include_bounds else breakpoints[1:-1]


def load_safety_data():
    """Yearly recordable-incident frequency rate, 1986-2020."""
    years = list(range(1986, 2021))
    rifr = [
        4.22, 8.32, 4.68, 8.77, 2.09, 0.74, 0.00, 0.00, 0.00, 2.76,
        7.60, 2.05, 3.45, 2.42, 2.03, 1.90, 1.61, 2.29, 0.87, 1.20,
        1.32, 1.31, 1.70, 1.62, 0.86, 1.06, 1.08, 0.67, 0.64, 0.88,
        0.98, 0.76, 0.34, 0.54, 0.35,
    ]
    return pd.DataFrame({"Year": years, "RIFR_per_200k": rifr})


# --------------------------------------------------------------------------
# Chapter 7: statistical process control
# --------------------------------------------------------------------------

def generate_kpi_data(n_points=30, base_value=100, noise_level=3,
                      start="2024-01-01", seed=42, with_period=False):
    """A KPI series with common-cause variation only."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start=start, periods=n_points, freq="D")
    values = base_value + rng.normal(0, noise_level, n_points)
    out = {"Date": dates, "KPI_Value": values}
    if with_period:
        out["Period"] = np.arange(1, n_points + 1)
    return pd.DataFrame(out)


def calculate_control_limits(data, column="KPI_Value", sigma_level=3):
    """Centre line and symmetric control limits for a stable baseline."""
    values = data[column]
    center_line = float(values.mean())
    std_dev = float(values.std(ddof=1))
    return {
        "center_line": center_line,
        "ucl": center_line + sigma_level * std_dev,
        "lcl": center_line - sigma_level * std_dev,
        "std_dev": std_dev,
    }


# --------------------------------------------------------------------------
# Chapter 7: survival analysis
# --------------------------------------------------------------------------

def kaplan_meier(durations, event_observed):
    """Kaplan-Meier survival estimate for right-censored durations."""
    durations = np.asarray(durations, dtype=float)
    event_observed = np.asarray(event_observed, dtype=int)
    order = np.argsort(durations)
    t, e = durations[order], event_observed[order]
    times, surv, s = [0.0], [1.0], 1.0
    for ti in np.unique(t[e == 1]):
        n_at_risk = float(np.sum(t >= ti))
        d_events = float(np.sum((t == ti) & (e == 1)))
        if n_at_risk > 0:
            s *= 1.0 - d_events / n_at_risk
        times.append(float(ti))
        surv.append(float(s))
    return np.array(times), np.array(surv)


def make_synthetic_turbofan(n_units=40, seed=7):
    """A CMAPSS-shaped synthetic run-to-failure table.

    One row per unit-cycle, with one operating setting and two sensors that
    drift with wear. Every fifth unit is right-censored at 70% of its life.
    The official NASA CMAPSS files are not bundled with this book; this table
    reproduces their unit-cycle-sensor layout so the examples run offline.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for unit in range(1, n_units + 1):
        life = int(rng.integers(90, 220))
        censored = unit % 5 == 0
        observed_end = life if not censored else max(30, int(life * 0.70))
        for t in range(1, observed_end + 1):
            wear = t / float(life)
            rows.append({
                "unit": unit,
                "cycle": t,
                "setting_1": rng.normal(0.0, 0.01),
                "sensor_4": 1400.0 + 40.0 * wear + rng.normal(0, 3.0),
                "sensor_11": 47.0 + 8.0 * wear + rng.normal(0, 0.4),
                "true_life": life,
                "failed": 0 if censored else 1,
            })
    df = pd.DataFrame(rows)
    df["RUL"] = df["true_life"] - df["cycle"]
    return df


def unit_level(df):
    """Collapse a unit-cycle table to one row per unit.

    ``duration`` is the last observed cycle and ``event`` is 1 for a unit that
    failed and 0 for one that was still running when observation stopped.
    """
    last = df.sort_values(["unit", "cycle"]).groupby("unit").tail(1).copy()
    last["duration"] = last["cycle"]
    last["event"] = last["failed"]
    return last.reset_index(drop=True)


def make_cox_units(n_units=80, seed=7):
    """Unit-level durations whose hazard depends on two covariates."""
    rng = np.random.default_rng(seed)
    rows = []
    for unit in range(1, n_units + 1):
        sensor = rng.normal(50.0, 4.0)
        setting = rng.normal(0.0, 1.0)
        life = int(np.clip(220 - 2.2 * (sensor - 50.0) + 4.0 * setting
                           + rng.normal(0, 18), 60, 260))
        censored = unit % 5 == 0
        duration = life if not censored else max(30, int(life * 0.70))
        rows.append({
            "duration": duration,
            "event": 0 if censored else 1,
            "sensor_11": sensor,
            "setting_1": setting,
        })
    return pd.DataFrame(rows)


def make_weibull_units(n_units=80, seed=7):
    """Unit-level durations drawn from a Weibull life and an exponential censor."""
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(1, n_units + 1):
        life = float(stats.weibull_min(c=1.6, scale=160).rvs(random_state=rng))
        censor = float(rng.exponential(220))
        rows.append({
            "duration": min(life, censor),
            "event": 1 if life <= censor else 0,
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Chapter 6: association rules
# --------------------------------------------------------------------------

def apriori_itemsets(df_encoded, min_support):
    """Frequent itemsets from a one-hot basket matrix."""
    if not 0 <= min_support <= 1:
        raise ValueError("min_support must be in [0, 1].")
    supports = {}
    items = list(df_encoded.columns)
    for item in items:
        sup = float(df_encoded[item].mean())
        if sup >= min_support:
            supports[frozenset([item])] = sup
    for k in range(2, min(4, len(items)) + 1):
        for combo in itertools.combinations(items, k):
            sup = float(df_encoded.loc[:, combo].all(axis=1).mean())
            if sup >= min_support:
                supports[frozenset(combo)] = sup
    return pd.DataFrame(
        [{"support": sup, "itemsets": itemset} for itemset, sup in supports.items()]
    ).sort_values(["support"], ascending=False, ignore_index=True)


def association_rules_simple(frequent_itemsets, min_confidence):
    """Rules with consequent support and lift = confidence / support(consequent)."""
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
                    rules.append({
                        "antecedents": antecedent,
                        "consequents": consequent,
                        "support": sup,
                        "confidence": confidence,
                        "consequent_support": sup_c,
                        "lift": confidence / sup_c,
                    })
    columns = ["antecedents", "consequents", "support", "confidence",
               "consequent_support", "lift"]
    if not rules:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rules).sort_values(
        ["lift", "confidence"], ascending=False, ignore_index=True
    )
