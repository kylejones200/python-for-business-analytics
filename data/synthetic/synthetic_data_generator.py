"""Generate a small, coherent family of synthetic business datasets.

What you'll learn:
  - How to generate reproducible synthetic tabular data with NumPy + pandas
  - How to write deterministic data generators without external dependencies
  - How to persist datasets (Parquet) for reuse in downstream scripts

Outputs (written under `data/` at the project root):
  - `data/business_customers.parquet`
  - `data/business_ops.parquet`
  - `data/business_tickets.parquet`
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Sizes:
    customers: int = 2_000
    ops: int = 10_000
    tickets: int = 5_000


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _categorical(r: np.random.Generator, values: list[str], p: list[float] | None, n: int) -> np.ndarray:
    return r.choice(values, size=n, replace=True, p=p)


def _clip(a: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return np.clip(a, lo, hi)


@dataclass
class SimpleFaker:
    """Lightweight, deterministic replacements for a few Faker helpers.

    This keeps dependencies small while still producing realistic-looking strings.

    Args:
        r: NumPy random generator used for deterministic sampling.
    """

    r: np.random.Generator

    _company_adjectives = (
        "Blue",
        "Red",
        "Green",
        "North",
        "South",
        "Silver",
        "Golden",
        "Rapid",
        "Bright",
        "Modern",
    )
    _company_nouns = (
        "River",
        "Pine",
        "Summit",
        "Harbor",
        "Canyon",
        "Oak",
        "Horizon",
        "Atlas",
        "Vertex",
        "Beacon",
    )
    _company_suffixes = ("LLC", "Inc.", "Co.", "Group", "Partners")
    _first_names = ("Alex", "Jordan", "Taylor", "Casey", "Riley", "Morgan", "Sam", "Jamie")
    _last_names = ("Smith", "Johnson", "Lee", "Patel", "Garcia", "Nguyen", "Brown", "Davis")
    _cities = ("Seattle", "Austin", "Denver", "Chicago", "Boston", "Phoenix", "Atlanta", "Miami")
    _states = ("WA", "TX", "CO", "IL", "MA", "AZ", "GA", "FL")

    def company(self) -> str:
        adj = self.r.choice(self._company_adjectives)
        noun = self.r.choice(self._company_nouns)
        suf = self.r.choice(self._company_suffixes)
        return f"{adj} {noun} {suf}"

    def name(self) -> str:
        first = self.r.choice(self._first_names)
        last = self.r.choice(self._last_names)
        return f"{first} {last}"

    def company_email(self) -> str:
        first = str(self.r.choice(self._first_names)).lower()
        last = str(self.r.choice(self._last_names)).lower()
        domain = str(self.r.choice(self._company_nouns)).lower() + ".example"
        return f"{first}.{last}@{domain}"

    def city(self) -> str:
        return str(self.r.choice(self._cities))

    def state_abbr(self) -> str:
        return str(self.r.choice(self._states))

    def postcode(self) -> str:
        return f"{int(self.r.integers(10000, 99999)):05d}"


def build_customers(fake: SimpleFaker, r: np.random.Generator, n: int) -> pd.DataFrame:
    """Build a synthetic customer master table.

    Args:
        fake: Deterministic string generator for names/emails/locations.
        r: Random generator for numeric sampling.
        n: Number of customers to generate.

    Returns:
        Customer DataFrame.
    """
    segments = ["SMB", "Mid", "Enterprise"]
    segment_p = [0.62, 0.28, 0.10]

    industries = ["Retail", "Manufacturing", "Energy", "Healthcare", "Finance", "SaaS"]
    industry_p = [0.20, 0.18, 0.12, 0.16, 0.14, 0.20]

    regions = ["West", "Mountain", "Midwest", "South", "Northeast"]
    region_p = [0.18, 0.14, 0.20, 0.28, 0.20]

    customer_id = np.arange(1, n + 1, dtype=np.int64)
    segment = _categorical(r, segments, segment_p, n)
    industry = _categorical(r, industries, industry_p, n)
    region = _categorical(r, regions, region_p, n)

    signup_days_ago = r.integers(10, 365 * 6, size=n)
    signup_date = (pd.Timestamp.today().normalize() - pd.to_timedelta(signup_days_ago, unit="D")).astype("datetime64[ns]")

    employees = (r.lognormal(mean=4.3, sigma=0.7, size=n)).astype(int)
    employees = _clip(employees, 5, 50_000).astype(int)

    annual_revenue_usd = employees * r.normal(loc=180_000, scale=35_000, size=n)
    annual_revenue_usd = _clip(annual_revenue_usd, 200_000, 25_000_000_000)

    base_mrr = np.where(
        segment == "SMB",
        r.normal(850, 350, size=n),
        np.where(segment == "Mid", r.normal(7_500, 2_800, size=n), r.normal(65_000, 24_000, size=n)),
    )
    mrr_usd = _clip(base_mrr, 100, 500_000)

    # Customer health signals (bounded)
    nps = _clip(r.normal(loc=24, scale=18, size=n), -100, 100)
    onboarding_complete = r.random(size=n) < np.where(segment == "Enterprise", 0.78, np.where(segment == "Mid", 0.84, 0.88))

    # Churn propensity driver: lower NPS + incomplete onboarding + low product adoption
    adoption = _clip(r.beta(2.2, 3.0, size=n), 0, 1)
    churn_score = (
        0.45 * (1 - (nps + 100) / 200) +
        0.35 * (1 - adoption) +
        0.20 * (1 - onboarding_complete.astype(float))
    )
    churn_prob = _clip(0.03 + 0.55 * churn_score, 0.01, 0.70)

    churned = r.random(size=n) < churn_prob
    churn_days_after_signup = np.where(churned, r.integers(30, 365 * 3, size=n), np.nan)
    churn_date = pd.to_datetime(signup_date) + pd.to_timedelta(churn_days_after_signup, unit="D")
    churn_date = churn_date.where(churned, pd.NaT)

    df = pd.DataFrame(
        {
            "customer_id": customer_id,
            "customer_name": [fake.company() for _ in range(n)],
            "contact_name": [fake.name() for _ in range(n)],
            "contact_email": [fake.company_email() for _ in range(n)],
            "industry": industry,
            "segment": segment,
            "region": region,
            "city": [fake.city() for _ in range(n)],
            "state": [fake.state_abbr() for _ in range(n)],
            "postal_code": [fake.postcode() for _ in range(n)],
            "signup_date": signup_date,
            "employees": employees,
            "annual_revenue_usd": annual_revenue_usd.round(0),
            "mrr_usd": mrr_usd.round(2),
            "adoption": adoption.round(4),
            "nps": nps.round(0).astype(int),
            "onboarding_complete": onboarding_complete,
            "churn_prob": churn_prob.round(4),
            "churned": churned,
            "churn_date": churn_date,
        }
    )

    return df


def build_ops(r: np.random.Generator, customers: pd.DataFrame, n: int) -> pd.DataFrame:
    """Build a synthetic "orders / operations" fact table.

    Args:
        r: Random generator for sampling.
        customers: Customer table produced by `build_customers`.
        n: Number of operations/orders to generate.

    Returns:
        Operations DataFrame.
    """
    channels = ["web", "phone", "field", "partner"]
    channel_p = [0.42, 0.28, 0.18, 0.12]

    products = ["Core", "Plus", "Pro", "Enterprise"]
    product_p = [0.44, 0.30, 0.18, 0.08]

    order_id = np.arange(1, n + 1, dtype=np.int64)
    customer_id = r.choice(customers["customer_id"].to_numpy(), size=n, replace=True)
    channel = _categorical(r, channels, channel_p, n)
    product = _categorical(r, products, product_p, n)

    # Time index. Keep within last 30 months.
    days_ago = r.integers(0, 30 * 30, size=n)
    order_date = (pd.Timestamp.today().normalize() - pd.to_timedelta(days_ago, unit="D")).astype("datetime64[ns]")

    qty = _clip(r.poisson(lam=2.2, size=n) + 1, 1, 25).astype(int)

    base_unit = np.select(
        [product == "Core", product == "Plus", product == "Pro", product == "Enterprise"],
        [r.normal(45, 9, n), r.normal(85, 15, n), r.normal(145, 25, n), r.normal(260, 45, n)],
        default=r.normal(75, 20, n),
    )
    unit_price = _clip(base_unit, 10, 600)

    # Discounts depend on channel and segment size via customer join.
    seg = customers.set_index("customer_id").loc[customer_id, "segment"].to_numpy()
    base_disc = np.where(channel == "partner", r.uniform(0.08, 0.22, n), r.uniform(0.00, 0.12, n))
    seg_bump = np.where(seg == "Enterprise", 0.05, np.where(seg == "Mid", 0.02, 0.00))
    discount = _clip(base_disc + seg_bump + r.normal(0, 0.01, n), 0.0, 0.35)

    gross = qty * unit_price
    net = gross * (1 - discount)

    # Operational outcomes
    promised_days = np.where(channel == "field", r.integers(5, 14, n), r.integers(2, 10, n))
    delay = r.normal(loc=0.6, scale=2.2, size=n)
    # Enterprise orders have more coordination overhead
    delay += np.where(seg == "Enterprise", r.normal(0.9, 1.2, n), 0.0)
    ship_days = _clip(promised_days + delay, 1, 35).round(0).astype(int)

    on_time = ship_days <= promised_days

    # Returns: higher for web, slightly higher for Core/Plus
    return_prob = 0.03
    return_prob += np.where(channel == "web", 0.03, 0.00)
    return_prob += np.where(product == "Core", 0.02, np.where(product == "Plus", 0.01, 0.00))
    return_prob += np.where(~on_time, 0.02, 0.00)
    returned = r.random(size=n) < _clip(return_prob, 0.01, 0.20)

    # Satisfaction score: down with delays and returns
    sat = 4.4 - 0.07 * (ship_days - promised_days) - 0.8 * returned.astype(float) + r.normal(0, 0.35, n)
    satisfaction = _clip(sat, 1.0, 5.0).round(2)

    df = pd.DataFrame(
        {
            "order_id": order_id,
            "customer_id": customer_id.astype(np.int64),
            "order_date": order_date,
            "channel": channel,
            "product": product,
            "quantity": qty,
            "unit_price_usd": unit_price.round(2),
            "discount_rate": discount.round(4),
            "gross_value_usd": gross.round(2),
            "net_value_usd": net.round(2),
            "promised_ship_days": promised_days.astype(int),
            "actual_ship_days": ship_days.astype(int),
            "on_time": on_time,
            "returned": returned,
            "satisfaction": satisfaction,
        }
    )

    return df


def build_tickets(
    fake: SimpleFaker,
    r: np.random.Generator,
    customers: pd.DataFrame,
    ops: pd.DataFrame,
    n: int,
) -> pd.DataFrame:
    """Build a synthetic support tickets table (with short text for NLP).

    Args:
        fake: Deterministic string generator for agent names.
        r: Random generator for sampling.
        customers: Customer table produced by `build_customers`.
        ops: Operations table produced by `build_ops`.
        n: Number of tickets to generate.

    Returns:
        Tickets DataFrame.
    """
    topics = ["billing", "bug", "how_to", "performance", "access", "integration", "feature_request"]
    topic_p = [0.16, 0.18, 0.20, 0.12, 0.14, 0.12, 0.08]

    priority = ["low", "medium", "high", "urgent"]
    priority_p = [0.34, 0.43, 0.18, 0.05]

    channels = ["email", "chat", "phone", "web_form"]
    channel_p = [0.42, 0.30, 0.18, 0.10]

    ticket_id = np.arange(1, n + 1, dtype=np.int64)
    customer_id = r.choice(customers["customer_id"].to_numpy(), size=n, replace=True)
    topic = _categorical(r, topics, topic_p, n)
    prio = _categorical(r, priority, priority_p, n)
    channel = _categorical(r, channels, channel_p, n)

    # Link some tickets to orders (support tied to fulfillment issues).
    order_link = r.random(size=n) < 0.35
    order_id = np.where(order_link, r.choice(ops["order_id"].to_numpy(), size=n, replace=True), np.nan)

    # Ticket times within last 18 months
    days_ago = r.integers(0, 18 * 30, size=n)
    created_at = (pd.Timestamp.today().normalize() - pd.to_timedelta(days_ago, unit="D")).astype("datetime64[ns]")
    created_at = pd.to_datetime(created_at) + pd.to_timedelta(r.integers(0, 24 * 60, size=n), unit="m")

    # Resolution time driven by priority + topic
    base_hours = r.lognormal(mean=2.2, sigma=0.7, size=n)  # ~ 9 hours median-ish
    prio_mult = np.select(
        [prio == "low", prio == "medium", prio == "high", prio == "urgent"],
        [0.9, 1.0, 1.4, 2.2],
        default=1.0,
    )
    topic_mult = np.select(
        [topic == "billing", topic == "bug", topic == "how_to", topic == "performance", topic == "integration", topic == "access", topic == "feature_request"],
        [0.9, 1.4, 0.8, 1.5, 1.6, 1.1, 1.3],
        default=1.0,
    )
    resolve_hours = _clip(base_hours * prio_mult * topic_mult, 0.25, 240).round(2)
    resolved_at = created_at + pd.to_timedelta(resolve_hours, unit="h")

    # SLA breach probability
    sla_target_hours = np.select(
        [prio == "low", prio == "medium", prio == "high", prio == "urgent"],
        [72, 48, 24, 6],
        default=48,
    ).astype(float)
    sla_breached = resolve_hours > sla_target_hours

    # Short, usable text for NLP. Keep it simple and consistent.
    text_templates = {
        "billing": [
            "Invoice shows an unexpected charge for {product}. Please explain the line items.",
            "Need a copy of last month invoice and the usage breakdown for {product}.",
            "Discount did not apply on renewal. Please confirm contract terms for {product}.",
        ],
        "bug": [
            "App crashes after login when I open the dashboard for {product}.",
            "Export fails with an error code. Steps to reproduce included below for {product}.",
            "Report totals look wrong after the latest update in {product}.",
        ],
        "how_to": [
            "How do I add a new user and set permissions in {product}?",
            "Need help configuring alerts and scheduled reports in {product}.",
            "How do I connect {product} to our data source and verify the sync?",
        ],
        "performance": [
            "Queries run slow during peak hours in {product}. Any tuning tips?",
            "Dashboard loads take over 30 seconds in {product}.",
            "Latency spikes appear after we add filters in {product}.",
        ],
        "access": [
            "User cannot access the project workspace in {product}. Please reset access.",
            "SSO login fails with an authentication error in {product}.",
            "Need to rotate API keys and confirm permissions for {product}.",
        ],
        "integration": [
            "Integration with our CRM fails during sync from {product}.",
            "Webhook does not trigger when records update in {product}.",
            "Need guidance to map fields across systems for {product}.",
        ],
        "feature_request": [
            "Request: add a summary view with filters in {product}.",
            "Please add support for a new export format in {product}.",
            "Request: allow custom roles and audit logs in {product}.",
        ],
    }

    products = ["Core", "Plus", "Pro", "Enterprise"]
    product = r.choice(products, size=n, replace=True)
    text = []
    for t, p in zip(topic, product):
        template = r.choice(text_templates[t])
        text.append(template.format(product=p))

    df = pd.DataFrame(
        {
            "ticket_id": ticket_id,
            "customer_id": customer_id.astype(np.int64),
            "order_id": pd.Series(order_id).astype("Int64"),
            "created_at": pd.to_datetime(created_at),
            "resolved_at": pd.to_datetime(resolved_at),
            "topic": topic,
            "priority": prio,
            "channel": channel,
            "resolve_hours": resolve_hours,
            "sla_target_hours": sla_target_hours,
            "sla_breached": sla_breached,
            "text": text,
            "agent_name": [fake.name() for _ in range(n)],
        }
    )

    return df


def main() -> None:
    """Generate datasets and write them to the project `data/` directory."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    project_root = Path(__file__).resolve().parents[2]
    out_dir = project_root / "data"
    _ensure_dir(out_dir)

    seed = 7
    r = _rng(seed)
    fake = SimpleFaker(r)

    sizes = Sizes()

    customers = build_customers(fake, r, sizes.customers)
    ops = build_ops(r, customers, sizes.ops)
    tickets = build_tickets(fake, r, customers, ops, sizes.tickets)

    customers_path = out_dir / "business_customers.parquet"
    ops_path = out_dir / "business_ops.parquet"
    tickets_path = out_dir / "business_tickets.parquet"

    customers.to_parquet(customers_path, index=False)
    ops.to_parquet(ops_path, index=False)
    tickets.to_parquet(tickets_path, index=False)

    logger.info(
        "Wrote %s (rows=%s cols=%s)",
        customers_path,
        f"{len(customers):,}",
        customers.shape[1],
    )
    logger.info(
        "Wrote %s (rows=%s cols=%s)",
        ops_path,
        f"{len(ops):,}",
        ops.shape[1],
    )
    logger.info(
        "Wrote %s (rows=%s cols=%s)",
        tickets_path,
        f"{len(tickets):,}",
        tickets.shape[1],
    )
    logger.info("Done.")


if __name__ == "__main__":
    main()
