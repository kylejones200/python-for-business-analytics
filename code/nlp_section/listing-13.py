"""Extract sentiment scores into separate DataFrame columns.

This module demonstrates an elegant approach to expanding sentiment score dictionaries
into separate columns using pandas DataFrame concatenation. Readers learn efficient
methods for structuring sentiment analysis results.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 13
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Extract sentiment scores into separate columns."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import pandas as pd
    import nltk

    # Seed randomness for reproducibility
    random.seed(42)

    # Download VADER lexicon if needed
    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception:
        pass

    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    # Initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Create sample review data
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

    # Extract dictionary values into separate columns
    # This elegant approach uses pandas' built-in Series expansion
    sentiment_scores = [sid.polarity_scores(str(text)) for text in df["review_text"]]

    # Convert list of dictionaries to DataFrame and concatenate
    df = pd.concat([df, pd.DataFrame(sentiment_scores)], axis=1)

    # Rename columns for clarity
    df.rename(
        columns={
            "neg": "sentiment_neg",
            "neu": "sentiment_neu",
            "pos": "sentiment_pos",
            "compound": "sentiment_compound",
        },
        inplace=True,
    )

    logger.info(
        f"\n{df[['review_text', 'sentiment_neg', 'sentiment_neu', 'sentiment_pos', 'sentiment_compound']].head()}"
    )

if __name__ == "__main__":
    main()
