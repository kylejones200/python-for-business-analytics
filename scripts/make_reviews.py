"""Create a small synthetic reviews dataset for NLP examples.

What you'll learn:
  - How to generate a text dataset with controlled randomness (seeded RNG)
  - How to cache generated data to `data/` so other scripts can reuse it
"""

from __future__ import annotations

import argparse
import logging
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


DEFAULT_SEED = 20260202
DEFAULT_N = 2000


def _project_root() -> Path:
    # Allow override for subprocess callers (bookdata.ensure_dataset).
    override = Path(str(Path.cwd()))
    env_root = None
    try:
        import os

        env_root = os.environ.get("BOOK_PROJECT_ROOT")
    except Exception:
        env_root = None
    if env_root:
        return Path(env_root).resolve()
    # scripts/ is at project root/scripts/
    return Path(__file__).resolve().parents[1]


def make_reviews(n: int = DEFAULT_N, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """Generate a synthetic reviews dataset.

    Args:
        n: Number of reviews to generate.
        seed: Random seed for reproducibility.

    Returns:
        Reviews DataFrame with columns: review_id, product, rating, text, date.
    """
    rng = np.random.default_rng(seed)

    products = [
        "Widget Pro",
        "Widget Mini",
        "Gizmo Plus",
        "Gizmo Air",
        "Doodad Max",
        "Doodad Lite",
        "Service Plan",
        "Starter Kit",
        "Premium Bundle",
        "Refill Pack",
    ]

    positive_bits = [
        "works exactly as described",
        "setup was quick",
        "the quality feels premium",
        "shipping was fast",
        "customer support was helpful",
        "great value for the price",
        "the packaging was excellent",
    ]
    neutral_bits = [
        "it does the job",
        "nothing special, but fine",
        "average quality",
        "shipping was okay",
        "instructions could be clearer",
        "it met my expectations",
    ]
    negative_bits = [
        "stopped working after a week",
        "arrived damaged",
        "missing a key part",
        "not worth the price",
        "support never followed up",
        "the fit was off",
        "quality control seems inconsistent",
    ]

    # Slightly positive skew, typical of public review platforms.
    ratings = rng.choice([1, 2, 3, 4, 5], size=n, p=[0.07, 0.10, 0.18, 0.32, 0.33])
    product = rng.choice(products, size=n, replace=True)

    def render_text(p: str, r: int) -> str:
        if r >= 4:
            bit = rng.choice(positive_bits)
            return f"Love the {p} — {bit}."
        if r == 3:
            bit = rng.choice(neutral_bits)
            return f"The {p} is okay — {bit}."
        bit = rng.choice(negative_bits)
        return f"Disappointed with the {p} — {bit}."

    texts = [render_text(p, int(r)) for p, r in zip(product, ratings)]

    # Random dates in the last ~2 years.
    end = date.today()
    start = end - timedelta(days=730)
    days = rng.integers(0, (end - start).days + 1, size=n)
    dates = [start + timedelta(days=int(d)) for d in days]

    df = pd.DataFrame(
        {
            "review_id": [f"R{idx:06d}" for idx in range(1, n + 1)],
            "product": product,
            "rating": ratings.astype(int),
            "text": texts,
            "date": pd.to_datetime(dates),
        }
    )
    return df


def main(argv: list[str] | None = None) -> None:
    """CLI entrypoint to generate `data/reviews.csv`.

    Args:
        argv: Optional CLI args (primarily for testing).
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Create a small synthetic reviews dataset.")
    parser.add_argument("--only", default="reviews", help="Dataset name (for compatibility).")
    parser.add_argument("--n", type=int, default=DEFAULT_N)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--force", action="store_true", help="Overwrite if output exists.")
    args = parser.parse_args(argv)

    if args.only not in {"reviews", "all"}:
        logger.info(
            "SKIPPED: make_reviews.py only supports --only reviews (got %r).", args.only
        )
        return None

    root = _project_root()
    out_path = root / "data" / "reviews.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists() and not args.force:
        logger.info("Using cached reviews dataset: %s", out_path)
        return None

    df = make_reviews(n=args.n, seed=args.seed)
    df.to_csv(out_path, index=False)
    logger.info("Wrote %s reviews to %s", f"{len(df):,}", out_path)
    return None


if __name__ == "__main__":
    main()

