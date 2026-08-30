"""Analyze relationship between sentiment and price using regression.

This module demonstrates exploratory data analysis and simple linear regression
to understand the relationship between description sentiment and listing prices.
Readers learn how to visualize relationships and fit regression models.

Note: This is exploratory analysis on the full dataset, not a predictive model
with train/test splits, so no leakage checks are needed.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 18
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Analyze sentiment-price relationship with regression."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import nltk
    from pathlib import Path
    from statsmodels.formula.api import ols

    # Seed randomness for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Download VADER lexicon if needed
    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception:
        pass

    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    # Initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Create sample listings data
    listings_data = {
        "listing_id": range(1, 101),
        "description": [
            "Absolutely stunning beachfront property! Luxurious amenities, breathtaking views.",
            "Nice apartment in decent location. Some wear and tear but functional.",
            "Beautiful home with modern updates. Perfect for families! Amazing pool.",
            "Small unit, needs some work. Location is okay, nothing special.",
            "Gorgeous historic home with incredible charm and character!",
        ]
        * 20,
        "price": np.random.randint(50, 500, 100),
    }

    listings_df = pd.DataFrame(listings_data)
    sentiment_scores = [
        sid.polarity_scores(str(text)) for text in listings_df["description"]
    ]
    listings_df = pd.concat([listings_df, pd.DataFrame(sentiment_scores)], axis=1)

    # First, let's look at the relationship visually
    plt.figure(figsize=(10, 6))
    plt.scatter(listings_df["compound"], listings_df["price"], alpha=0.6)
    plt.xlabel("Sentiment Score (Compound)", fontsize=12)
    plt.ylabel("Price ($)", fontsize=12)
    plt.title("Relationship Between Description Sentiment and Price", fontsize=14)
    plt.axvline(x=0, color="red", linestyle="--", alpha=0.3, label="Neutral")
    
    plt.legend()
    plt.tight_layout()

    # Save plot before showing
    output_path = Path("img/nlp_sentiment_price_scatter.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    plt.show()
    plt.close()

    # Run simple linear regression
    # Formula: price ~ compound (price is predicted by compound sentiment)
    model = ols("price ~ compound", data=listings_df).fit()

    # Display regression results
    logger.info(f"\n{model.summary()}")

if __name__ == "__main__":
    main()
