"""Demonstrates selecting specific columns for analysis from a dataset.

This script shows how to load customer data and select relevant columns for
churn analysis. Readers learn column selection, data subsetting, and preparing
data for specific analytical tasks.

"""
import logging
import sys
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating column selection for analysis."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    from bookdata import load_frame

    df = load_frame("business_customers")

    # Focus on churn-relevant columns for this chapter
    churn_view = [
        "customer_id",
        "segment",
        "industry",
        "region",
        "mrr_usd",
        "nps",
        "adoption",
        "onboarding_complete",
        "churn_prob",
        "churned",
        "churn_date",
    ]
    logger.info(df[churn_view].head())

if __name__ == "__main__":
    main()
