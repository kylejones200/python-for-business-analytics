"""Fetch a small set of FRED series to a local cache.

What you'll learn:
  - How to download public economic time series data from FRED
  - How to build a small, reproducible local dataset cache in `data/`
  - How to write scripts that fail gracefully when the network is unavailable

This script intentionally does **not** require an API key.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import logging
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


DEFAULT_SERIES = ("UNRATE", "CPIAUCSL", "DGS10")


def _project_root() -> Path:
    import os

    env_root = os.environ.get("BOOK_PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return Path(__file__).resolve().parents[1]


def _fetch_with_pandas_datareader(
    series: Iterable[str], start: _dt.date, end: _dt.date
) -> pd.DataFrame:
    # User requested pandas-datareader; it does not require an API key for FRED.
    import pandas_datareader.data as web  # type: ignore

    df = web.DataReader(list(series), "fred", start, end)
    df = df.reset_index()
    # pandas-datareader may name the date column differently depending on version.
    if "DATE" in df.columns:
        df = df.rename(columns={"DATE": "date"})
    elif "index" in df.columns:
        df = df.rename(columns={"index": "date"})
    else:
        df = df.rename(columns={df.columns[0]: "date"})
    return df


def _fetch_with_fred_csv(series: Iterable[str], start: _dt.date, end: _dt.date) -> pd.DataFrame:
    # Fallback when pandas-datareader isn't installed. Still no API key.
    # Uses FRED's CSV endpoint per series and merges on date.
    out: pd.DataFrame | None = None
    for sid in series:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
        s = pd.read_csv(url)
        # Common FRED column names across endpoints/versions.
        date_col = None
        if "DATE" in s.columns:
            date_col = "DATE"
        elif "observation_date" in s.columns:
            date_col = "observation_date"
        if date_col is None:
            raise ValueError(f"Unexpected FRED CSV columns for {sid}: {list(s.columns)[:8]}")

        s = s.rename(columns={date_col: "date"})
        s["date"] = pd.to_datetime(s["date"])
        # Filter dates
        s = s[(s["date"] >= pd.to_datetime(start)) & (s["date"] <= pd.to_datetime(end))]
        out = s if out is None else out.merge(s, on="date", how="outer")
    assert out is not None
    out = out.sort_values("date").reset_index(drop=True)
    return out


def fetch_fred_series(
    *,
    series: Iterable[str] = DEFAULT_SERIES,
    start: _dt.date = _dt.date(2010, 1, 1),
    end: _dt.date | None = None,
) -> pd.DataFrame:
    end = end or _dt.date.today()
    try:
        return _fetch_with_pandas_datareader(series, start, end)
    except ModuleNotFoundError:
        # pandas-datareader not installed; fall back to direct CSV download.
        return _fetch_with_fred_csv(series, start, end)


def _synthetic_fred_series(
    series: Iterable[str], start: _dt.date, end: _dt.date, *, seed: int = 42
) -> pd.DataFrame:
    """Generate a small synthetic stand-in for FRED series (offline-friendly)."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start, end, freq="MS")
    df = pd.DataFrame({"date": dates})
    for sid in series:
        sid_u = sid.upper()
        if sid_u == "UNRATE":
            base = 4.5 + 1.2 * np.sin(np.linspace(0, 3 * np.pi, len(dates)))
            noise = rng.normal(0, 0.25, len(dates))
            df[sid] = np.clip(base + noise, 2.5, 12.0)
        elif sid_u == "CPIAUCSL":
            trend = np.linspace(230, 310, len(dates))
            noise = rng.normal(0, 1.5, len(dates))
            df[sid] = trend + noise
        elif sid_u == "DGS10":
            base = 3.0 + 1.0 * np.sin(np.linspace(0, 2.5 * np.pi, len(dates)))
            noise = rng.normal(0, 0.15, len(dates))
            df[sid] = np.clip(base + noise, 0.5, 8.0)
        else:
            df[sid] = rng.normal(0, 1.0, len(dates))
    return df


def main(argv: list[str] | None = None) -> None:
    """Fetch FRED series and write them to `data/fred_series.parquet`.

    Args:
        argv: Optional CLI args (primarily for testing).
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Fetch a small set of FRED series and cache to data/fred_series.parquet."
    )
    parser.add_argument("--only", default="fred_series", help="Dataset name (for compatibility).")
    parser.add_argument("--force", action="store_true", help="Overwrite cached output.")
    parser.add_argument(
        "--start", default="2010-01-01", help="Start date (YYYY-MM-DD)."
    )
    parser.add_argument("--end", default=None, help="End date (YYYY-MM-DD), default today.")
    args = parser.parse_args(argv)

    if args.only not in {"fred_series", "all"}:
        logger.info(
            "SKIPPED: fetch_fred.py only supports --only fred_series (got %r).",
            args.only,
        )
        return None

    root = _project_root()
    out_path = root / "data" / "fred_series.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists() and not args.force:
        logger.info("Using cached FRED dataset: %s", out_path)
        return None

    try:
        start = _dt.date.fromisoformat(args.start)
        end = _dt.date.fromisoformat(args.end) if args.end else None
    except ValueError as e:
        logger.error("Invalid date format: %s", e)
        logger.error("Expected ISO format YYYY-MM-DD for --start/--end.")
        raise SystemExit(2)

    try:
        df = fetch_fred_series(series=DEFAULT_SERIES, start=start, end=end)
    except Exception as e:
        if out_path.exists():
            logger.warning(
                "Failed to fetch FRED data from the network; using existing cache.\nReason: %s",
                e,
            )
            return None
        logger.warning("Failed to fetch FRED data; generating a small synthetic fallback dataset.")
        logger.warning("Reason: %s", e)
        df = _synthetic_fred_series(DEFAULT_SERIES, start, end or _dt.date.today(), seed=42)

    df.to_parquet(out_path, index=False)
    logger.info(
        "Wrote FRED series %s to %s (%s rows)",
        list(DEFAULT_SERIES),
        out_path,
        f"{len(df):,}",
    )
    return None


if __name__ == "__main__":
    main()

