"""Display customer dataset summary for understanding statistical analysis.

This script shows the structure of business customer data before analysis.

Chapter: Reasoning with Data and Uncertainty
Source: 4.0.tex
"""
import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Display customer data summary."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    
    from bookdata import ensure_dataset
    
    customers_path = ensure_dataset("business_customers")
    if customers_path is None:
        logger.warning("SKIPPED: business_customers dataset unavailable.")
        return
    
    df = pd.read_parquet(customers_path)
    
    # Create figure showing key dataset info
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis("off")
    
    # Create summary text
    summary_lines = [
        "Business Customer Dataset Summary",
        "=" * 50,
        f"Total Customers: {len(df):,}",
        "",
        "Key Metrics:",
        f"  - MRR Range: ${df['mrr_usd'].min():,.0f} to ${df['mrr_usd'].max():,.0f}",
        f"  - Average MRR: ${df['mrr_usd'].mean():,.0f}",
        f"  - NPS Range: {df['nps'].min():.0f} to {df['nps'].max():.0f}",
        f"  - Average NPS: {df['nps'].mean():.1f}",
        "",
        "Customer Segments:",
    ]
    
    for seg in df['segment'].value_counts().sort_index().items():
        summary_lines.append(f"  - {seg[0]}: {seg[1]:,} customers ({seg[1]/len(df)*100:.1f}%)")
    
    summary_lines.extend([
        "",
        "Geographic Regions:",
    ])
    
    for reg in df['region'].value_counts().sort_index().items():
        summary_lines.append(f"  - {reg[0]}: {reg[1]:,} customers")
    
    summary_lines.extend([
        "",
        "Customer Status:",
        f"  - Churned: {df['churned'].sum():,} ({df['churned'].sum()/len(df)*100:.1f}%)",
        f"  - Active: {(~df['churned']).sum():,} ({(~df['churned']).sum()/len(df)*100:.1f}%)",
        f"  - Onboarding Complete: {df['onboarding_complete'].sum():,} ({df['onboarding_complete'].sum()/len(df)*100:.1f}%)",
    ])
    
    text = "\n".join(summary_lines)
    
    ax.text(0.1, 0.95, text,
            transform=ax.transAxes,
            fontfamily="monospace",
            fontsize=11,
            verticalalignment="top")
    
    # Save figure
    img_dir = ROOT / "img"
    output_path = img_dir / "ch4_customer_summary.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
