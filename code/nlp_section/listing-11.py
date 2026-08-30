"""Add sentiment scores to review data.

This module demonstrates adding VADER sentiment scores to a DataFrame of reviews
using list comprehension for efficient processing. Readers learn how to classify
sentiment into categories (Positive, Negative, Neutral) based on compound scores.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 11
"""

import logging
import random

logger = logging.getLogger(__name__)

def classify_sentiment(compound):
    """Classify sentiment based on compound score.

    Args:
        compound: VADER compound sentiment score.

    Returns:
        str: Sentiment category ('Positive', 'Negative', or 'Neutral').
    """
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def add_sentiment_scores(df, text_column, sid):
    """Add sentiment scores to a DataFrame.

    Args:
        df: DataFrame with reviews.
        text_column: Name of column containing text.
        sid: SentimentIntensityAnalyzer instance.

    Returns:
        pandas.DataFrame: DataFrame with added sentiment columns.
    """
    import pandas as pd

    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame")

    # Method 1: Using list comprehension (faster and more "Pythonic")
    logger.info(f"Analyzing {len(df)} reviews...")

    # Calculate sentiment scores for each review
    sentiment_scores = [sid.polarity_scores(str(text)) for text in df[text_column]]

    # Extract individual scores into separate columns
    df = df.copy()
    df["sentiment_neg"] = [score["neg"] for score in sentiment_scores]
    df["sentiment_neu"] = [score["neu"] for score in sentiment_scores]
    df["sentiment_pos"] = [score["pos"] for score in sentiment_scores]
    df["sentiment_compound"] = [score["compound"] for score in sentiment_scores]

    # Classify sentiment based on compound score
    df["sentiment_category"] = df["sentiment_compound"].apply(classify_sentiment)

    logger.info("Sentiment analysis complete!")
    return df

def main() -> None:
    """Apply sentiment analysis to sample review data."""
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

    # Apply sentiment analysis
    df = add_sentiment_scores(df, "review_text", sid)

    # Display results
    logger.info("\nReviews with Sentiment Scores:")
    logger.info(
        f"\n{df[['review_text', 'rating', 'sentiment_compound', 'sentiment_category']].head(10)}"
    )

if __name__ == "__main__":
    main()
