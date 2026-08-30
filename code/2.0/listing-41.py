"""Demonstrates pandas plotting with bar and line charts.

This script shows how to create bar and line plots directly from pandas
DataFrames. Readers learn pandas plotting methods, different plot types,
and basic data visualization with pandas.

"""
import logging
import os
from pathlib import Path

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating pandas plotting."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Create example DataFrame
    import pandas as pd
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Age': [25, 30, 35, 28],
        'Salary': [50000, 60000, 55000, 65000]
    })
    
    script_path = Path(__file__)
    img_dir = script_path.parents[2] / "img"
    img_dir.mkdir(exist_ok=True)

    # Bar plot
    df["Age"].plot(kind="bar")
    plt.title("Age Distribution")
    fig_filename1 = img_dir / f"{script_path.stem}_bar.png"
    plt.savefig(fig_filename1, dpi=150, bbox_inches="tight")
    logger.info(f"Bar plot saved to {fig_filename1}")
    # Line plot
    df.set_index("Name")["Salary"].plot(kind="line")
    plt.title("Salary by Employee")
    fig_filename2 = img_dir / f"{script_path.stem}_line.png"
    plt.savefig(fig_filename2, dpi=150, bbox_inches="tight")
    logger.info(f"Line plot saved to {fig_filename2}")
if __name__ == "__main__":
    main()
