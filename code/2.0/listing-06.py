"""Demonstrates saving DataFrames to CSV files.

This script shows how to export pandas DataFrames to CSV format using to_csv().
Readers learn data export, CSV file creation, and index handling options.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 06
"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating CSV export."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Create example DataFrame
    import pandas as pd
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'London', 'Tokyo']
    })
    
    output_path = Path("data/output.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"DataFrame saved to {output_path}")

if __name__ == "__main__":
    main()