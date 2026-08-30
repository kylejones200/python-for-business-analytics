"""Create vacation rental listings dataset with sentiment scores.

This module demonstrates creating a realistic dataset of vacation rental listings
and adding sentiment scores to descriptions. Readers learn how to combine
sentiment analysis with structured data for business analytics.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 17
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Create listings dataset and add sentiment scores."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import numpy as np
    import pandas as pd
    import nltk

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

    # Create a realistic dataset: vacation rental listings
    listings_data = {
        "listing_id": range(1, 101),
        "description": [
            # Sample descriptions with varying sentiment
            "Absolutely stunning beachfront property! Luxurious amenities, breathtaking views.",
            "Nice apartment in decent location. Some wear and tear but functional.",
            "Beautiful home with modern updates. Perfect for families! Amazing pool.",
            "Small unit, needs some work. Location is okay, nothing special.",
            "Gorgeous historic home with incredible charm and character!",
            # ... (in practice, you'd have 100+ real descriptions)
        ]
        * 20,  # Repeat to get 100 listings
        "price": np.random.randint(50, 500, 100),  # Prices from $50 to $500
    }

    listings_df = pd.DataFrame(listings_data)

    # Add sentiment scores
    sentiment_scores = [
        sid.polarity_scores(str(text)) for text in listings_df["description"]
    ]
    listings_df = pd.concat([listings_df, pd.DataFrame(sentiment_scores)], axis=1)

    logger.info("Listing Data with Sentiment:")
    logger.info(f"\n{listings_df[['description', 'price', 'compound']].head()}")

if __name__ == "__main__":
    main()
