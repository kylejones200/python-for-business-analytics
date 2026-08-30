"""Demonstrates DataFrame column selection, filtering, and aggregation.

This script shows how to select columns, add new columns, filter rows, and
perform groupby aggregations. Readers learn DataFrame manipulation, boolean
indexing, and aggregation operations.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 07
"""
import logging

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating DataFrame operations."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Create example DataFrame
    import pandas as pd
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Age': [25, 30, 35, 28],
        'City': ['New York', 'London', 'New York', 'Tokyo']
    })
    
    # Selecting a column
    logger.info("Ages:\n%s", df["Age"])

    # Adding a new column
    df["Salary"] = [50000, 60000, 55000, 65000]
    logger.info("\nDataFrame with new column:\n%s", df)

    # Filtering data
    high_salary = df[df["Salary"] > 55000]
    logger.info("\nHigh salary employees:\n%s", high_salary)

    # Grouping and aggregation
    avg_salary_by_city = df.groupby("City")["Salary"].mean()
    logger.info("\nAverage salary by city:\n%s", avg_salary_by_city)

if __name__ == "__main__":
    main()