"""Generate reproducible synthetic datasets for the book.

What you'll learn:
  - How to generate coherent synthetic business datasets with stable random seeds
  - How to cache datasets locally to `data/` for fast, repeatable examples
  - How to structure builder scripts that other examples can call via subprocess
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


DEFAULT_SEED = 20260202

N_CUSTOMERS = 2000
N_OPS = 10000
N_TICKETS = 5000
N_ZIPS = 1000


def _project_root() -> Path:
    import os

    env_root = os.environ.get("BOOK_PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return Path(__file__).resolve().parents[1]


def _write_parquet(df: pd.DataFrame, path: Path, *, force: bool) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        logger.info("Using cached dataset: %s", path)
        return False
    df.to_parquet(path, index=False)
    logger.info("Wrote %s rows to %s", f"{len(df):,}", path)
    return True


def make_zip_income(rng: np.random.Generator, n: int = N_ZIPS) -> pd.DataFrame:
    # Generate a Texas-flavored set of ZIPs so it pairs naturally with the default
    # Texas ZIP geometry download in fetch_zip_geometry.py.
    zips = rng.choice(np.arange(75001, 79999), size=n, replace=False)
    # Income distribution: lognormal around ~$65k with some spread.
    income = rng.lognormal(mean=np.log(65000), sigma=0.35, size=n)
    df = pd.DataFrame(
        {"zip": [f"{int(z):05d}" for z in zips], "median_income_usd": income.round(0).astype(int)}
    ).sort_values("zip")
    return df.reset_index(drop=True)


def make_business_customers(
    rng: np.random.Generator, zip_income: pd.DataFrame, n: int = N_CUSTOMERS
) -> pd.DataFrame:
    segments = np.array(["SMB", "Mid-Market", "Enterprise"])
    industries = np.array(
        ["SaaS", "Retail", "Healthcare", "Manufacturing", "Education", "Finance"]
    )
    regions = np.array(["Northeast", "Southeast", "Midwest", "Southwest", "West"])

    customer_id = [f"C{idx:06d}" for idx in range(1, n + 1)]

    signup_end = date.today()
    signup_start = signup_end - timedelta(days=4 * 365)
    signup_days = rng.integers(0, (signup_end - signup_start).days + 1, size=n)
    signup_date = [signup_start + timedelta(days=int(d)) for d in signup_days]

    segment = rng.choice(segments, size=n, p=[0.55, 0.30, 0.15])
    industry = rng.choice(industries, size=n, replace=True)
    region = rng.choice(regions, size=n, replace=True)
    customer_zip = rng.choice(zip_income["zip"].to_numpy(), size=n, replace=True)

    # Monthly recurring revenue with segment effect.
    base = rng.lognormal(mean=np.log(120), sigma=0.65, size=n)
    seg_mult = np.where(segment == "Enterprise", 9.0, np.where(segment == "Mid-Market", 3.0, 1.0))
    mrr_usd = (base * seg_mult).round(2)

    # Adoption and NPS correlate.
    adoption = np.clip(rng.normal(loc=0.62, scale=0.20, size=n), 0, 1)
    onboarding_complete = rng.random(n) < (0.75 + 0.20 * adoption)
    nps = np.clip((rng.normal(loc=25, scale=35, size=n) + (adoption - 0.5) * 60), -100, 100).round(0).astype(int)

    # Churn probability: higher when adoption is low and NPS is low.
    z = (
        -1.2
        + (0.9 * (0.5 - adoption))
        + (0.015 * (0 - nps))
        + (0.10 * (segment == "SMB"))
    )
    churn_prob = 1 / (1 + np.exp(-z))
    churned = rng.random(n) < churn_prob

    churn_date = []
    for s_date, c in zip(signup_date, churned):
        if not c:
            churn_date.append(pd.NaT)
            continue
        start = pd.to_datetime(s_date)
        end = pd.to_datetime(date.today())
        if end <= start:
            churn_date.append(end)
            continue
        days = int(rng.integers(30, max(31, (end - start).days)))
        churn_date.append(start + pd.Timedelta(days=days))

    df = pd.DataFrame(
        {
            "customer_id": customer_id,
            "signup_date": pd.to_datetime(signup_date),
            "segment": segment,
            "industry": industry,
            "region": region,
            "zip": customer_zip,
            "mrr_usd": mrr_usd,
            "nps": nps,
            "adoption": adoption.round(3),
            "onboarding_complete": onboarding_complete.astype(bool),
            "churn_prob": churn_prob.round(4),
            "churned": churned.astype(bool),
            "churn_date": pd.to_datetime(churn_date),
        }
    )
    return df


def make_business_ops(
    rng: np.random.Generator, customers: pd.DataFrame, n: int = N_OPS
) -> pd.DataFrame:
    products = np.array(
        ["Widget Pro", "Widget Mini", "Gizmo Plus", "Doodad Max", "Starter Kit", "Refill Pack"]
    )
    customer_ids = customers["customer_id"].to_numpy()

    order_id = [f"O{idx:07d}" for idx in range(1, n + 1)]
    order_end = datetime.now()
    order_start = order_end - timedelta(days=3 * 365)
    order_ts = order_start + pd.to_timedelta(
        rng.integers(0, int((order_end - order_start).total_seconds()), size=n), unit="s"
    )

    customer_id = rng.choice(customer_ids, size=n, replace=True)
    product = rng.choice(products, size=n, replace=True)
    quantity = rng.integers(1, 6, size=n)

    unit_price_usd = rng.lognormal(mean=np.log(35), sigma=0.75, size=n)
    unit_price_usd = np.clip(unit_price_usd, 5, 450).round(2)
    discount_rate = np.clip(rng.beta(a=2.2, b=9.5, size=n), 0, 0.40).round(3)

    gross_value_usd = (quantity * unit_price_usd).round(2)
    net_value_usd = (gross_value_usd * (1 - discount_rate)).round(2)

    promised_ship_days = rng.integers(1, 8, size=n)
    # Mostly on-time; some delays.
    delay = rng.choice([0, 0, 0, 1, 2, 3, 5], size=n, replace=True)
    actual_ship_days = np.maximum(1, promised_ship_days + delay)

    # Satisfaction drops with delays and larger discounts (proxying promos).
    satisfaction = 4.6 - 0.35 * (actual_ship_days - promised_ship_days) - 0.8 * discount_rate
    satisfaction = np.clip(satisfaction + rng.normal(0, 0.35, size=n), 1.0, 5.0).round(2)

    df = pd.DataFrame(
        {
            "order_id": order_id,
            "order_date": pd.to_datetime(order_ts),
            "customer_id": customer_id,
            "product": product,
            "quantity": quantity.astype(int),
            "unit_price_usd": unit_price_usd,
            "discount_rate": discount_rate,
            "gross_value_usd": gross_value_usd,
            "net_value_usd": net_value_usd,
            "promised_ship_days": promised_ship_days.astype(int),
            "actual_ship_days": actual_ship_days.astype(int),
            "satisfaction": satisfaction,
        }
    )
    return df


def make_business_tickets(
    rng: np.random.Generator, customers: pd.DataFrame, n: int = N_TICKETS
) -> pd.DataFrame:
    categories = np.array(["Shipping", "Billing", "Product", "Account", "Returns", "Other"])
    channels = np.array(["email", "chat", "phone", "web"])
    priorities = np.array(["low", "medium", "high"])
    statuses = np.array(["open", "closed"])

    customer_ids = customers["customer_id"].to_numpy()
    ticket_id = [f"T{idx:07d}" for idx in range(1, n + 1)]

    end = datetime.now()
    start = end - timedelta(days=365 * 2)
    created_at = start + pd.to_timedelta(
        rng.integers(0, int((end - start).total_seconds()), size=n), unit="s"
    )

    customer_id = rng.choice(customer_ids, size=n, replace=True)
    category = rng.choice(categories, size=n, replace=True)
    channel = rng.choice(channels, size=n, replace=True)
    priority = rng.choice(priorities, size=n, p=[0.55, 0.33, 0.12])
    status = rng.choice(statuses, size=n, p=[0.08, 0.92])

    # Response and resolution times vary by channel and priority.
    base_response = np.where(channel == "chat", 0.8, np.where(channel == "phone", 0.6, 3.5))
    priority_mult = np.where(priority == "high", 0.6, np.where(priority == "medium", 1.0, 1.4))
    first_response_hours = np.clip(
        rng.lognormal(mean=np.log(base_response), sigma=0.55) * priority_mult, 0.05, 72
    ).round(2)
    resolution_hours = np.clip(
        first_response_hours + rng.lognormal(mean=np.log(6.0), sigma=0.75, size=n), 0.25, 720
    ).round(2)

    # Simple CSAT proxy: lower for long resolution and high priority.
    csat = 4.8 - 0.0035 * resolution_hours - 0.3 * (priority == "high")
    csat = np.clip(csat + rng.normal(0, 0.45, size=n), 1.0, 5.0).round(2)
    reopened = rng.random(n) < (0.03 + 0.02 * (csat < 3.0))

    df = pd.DataFrame(
        {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "created_at": pd.to_datetime(created_at),
            "category": category,
            "channel": channel,
            "priority": priority,
            "status": status,
            "first_response_hours": first_response_hours,
            "resolution_hours": resolution_hours,
            "csat": csat,
            "reopened": reopened.astype(bool),
        }
    )
    return df


def _run_other_builder(script: Path, *, only: str, force: bool) -> None:
    cmd = [sys.executable, str(script), "--only", only]
    if force:
        cmd.append("--force")
    proc = subprocess.run(cmd, cwd=str(_project_root()))
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def main(argv: list[str] | None = None) -> None:
    """Generate the book's canonical datasets under `data/`.

    Args:
        argv: Optional CLI args (primarily for testing).
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Create canonical book datasets under data/ (synthetic, reproducible)."
    )
    parser.add_argument(
        "--only",
        default="all",
        help=(
            "Create only one dataset name (business_ops, business_customers, business_tickets, zip_income) "
            "or 'all' to create everything."
        ),
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--force", action="store_true", help="Overwrite cached outputs.")
    parser.add_argument(
        "--with-network",
        action="store_true",
        default=False,
        help="Also fetch network-backed datasets (fred_series, zip_geometry).",
    )
    args = parser.parse_args(argv)

    root = _project_root()
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)

    # zip_income is a small table used for spatial joins (doesn't require network).
    zip_income = make_zip_income(rng, n=N_ZIPS)

    if args.only in {"zip_income", "all"}:
        _write_parquet(zip_income, data_dir / "zip_income.parquet", force=args.force)

    # Customers depend on zip_income.
    customers = make_business_customers(rng, zip_income, n=N_CUSTOMERS)
    if args.only in {"business_customers", "all"}:
        _write_parquet(customers, data_dir / "business_customers.parquet", force=args.force)

    # Ops + tickets depend on customers.
    ops = make_business_ops(rng, customers, n=N_OPS)
    if args.only in {"business_ops", "all"}:
        _write_parquet(ops, data_dir / "business_ops.parquet", force=args.force)

    tickets = make_business_tickets(rng, customers, n=N_TICKETS)
    if args.only in {"business_tickets", "all"}:
        _write_parquet(tickets, data_dir / "business_tickets.parquet", force=args.force)

    # For convenience: generate reviews in the same "one step" command.
    if args.only == "all":
        reviews_script = root / "scripts" / "make_reviews.py"
        if reviews_script.exists():
            _run_other_builder(reviews_script, only="reviews", force=args.force)

        if args.with_network:
            fetch_fred = root / "scripts" / "fetch_fred.py"
            fetch_zip = root / "scripts" / "fetch_zip_geometry.py"
            if fetch_fred.exists():
                _run_other_builder(fetch_fred, only="fred_series", force=args.force)
            if fetch_zip.exists():
                _run_other_builder(fetch_zip, only="zip_geometry", force=args.force)

    return None


if __name__ == "__main__":
    main()

