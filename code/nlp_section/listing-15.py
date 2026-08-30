"""Display extreme positive and negative reviews.

This module demonstrates identifying and displaying the most positive and negative
reviews based on sentiment scores. Readers learn how to extract and present
extreme cases for analysis.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 15
"""

import logging
import random

logger = logging.getLogger(__name__)

def show_extreme_reviews(df, n=3):
    """Display the most positive and negative reviews.

    Args:
        df: DataFrame with sentiment scores and review text.
        n: Number of extreme reviews to display for each category.
    """
    if "sentiment_compound" not in df.columns:
        raise ValueError("DataFrame must contain 'sentiment_compound' column")
    if "review_text" not in df.columns:
        raise ValueError("DataFrame must contain 'review_text' column")

    logger.info(f"\nTOP {n} MOST POSITIVE REVIEWS")

    top_positive = df.nlargest(n, "sentiment_compound")
    for idx, row in top_positive.iterrows():
        rating_str = f" | Rating: {row['rating']} stars" if "rating" in df.columns else ""
        logger.info(
            f"\nScore: {row['sentiment_compound']:.3f}{rating_str}"
        )
        logger.info(f"Review: {row['review_text']}")

    logger.info(f"\nTOP {n} MOST NEGATIVE REVIEWS")

    top_negative = df.nsmallest(n, "sentiment_compound")
    for idx, row in top_negative.iterrows():
        rating_str = f" | Rating: {row['rating']} stars" if "rating" in df.columns else ""
        logger.info(
            f"\nScore: {row['sentiment_compound']:.3f}{rating_str}"
        )
        logger.info(f"Review: {row['review_text']}")

def main() -> None:
    """Show extreme reviews from sample data."""
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

    # Add sentiment scores
    sentiment_scores = [sid.polarity_scores(str(text)) for text in df["review_text"]]
    df = pd.concat([df, pd.DataFrame(sentiment_scores)], axis=1)
    df.rename(
        columns={
            "neg": "sentiment_neg",
            "neu": "sentiment_neu",
            "pos": "sentiment_pos",
            "compound": "sentiment_compound",
        },
        inplace=True,
    )

    # Show extreme reviews
    show_extreme_reviews(df, n=3)

if __name__ == "__main__":
    main()
