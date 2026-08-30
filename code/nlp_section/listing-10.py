"""Create sample review dataset for sentiment analysis.

This module demonstrates creating a sample dataset of product reviews with ratings
and text. Readers learn how to structure review data for sentiment analysis tasks.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 10
"""

import logging
import random

logger = logging.getLogger(__name__)

def main():
    """Create and display sample review dataset."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    import pandas as pd

    # Seed randomness for reproducibility
    random.seed(42)

    # Create sample review data (or load from CSV)
    sample_reviews = {
        "review_id": range(1, 11),
        "product": ["Widget A"] * 5 + ["Widget B"] * 5,
        "rating": [5, 4, 3, 2, 1, 5, 5, 4, 3, 1],
        "review_text": [
            "Absolutely love this product! Best purchase ever.",
            "Pretty good, works as expected.",
            "It's okay, nothing special.",
            "Not great, disappointed with quality.",
            "Terrible! Broke after one week. Very upset.",
            "Amazing quality! Highly recommend.",
            "Great product, exceeded expectations!",
            "Good value for the price.",
            "Average product, has some issues.",
            "Worst product ever. Complete waste of money.",
        ],
    }

    df = pd.DataFrame(sample_reviews)
    logger.info("Sample Review Data:")
    logger.info(f"\n{df.head()}")

if __name__ == "__main__":
    main()
