"""Complete sentiment analysis pipeline function.

This module provides a reusable function for complete sentiment analysis pipeline
including data loading, sentiment scoring, visualization, and result saving.
Readers learn how to create modular NLP analysis functions.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 16
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def classify_sentiment(compound):
    """Classify sentiment based on compound score."""
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def add_sentiment_scores(df, text_column, sid):
    """Add sentiment scores to a DataFrame."""
    import pandas as pd

    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame")

    logger.info(f"Analyzing {len(df)} reviews...")
    sentiment_scores = [sid.polarity_scores(str(text)) for text in df[text_column]]
    df = df.copy()
    df["sentiment_neg"] = [score["neg"] for score in sentiment_scores]
    df["sentiment_neu"] = [score["neu"] for score in sentiment_scores]
    df["sentiment_pos"] = [score["pos"] for score in sentiment_scores]
    df["sentiment_compound"] = [score["compound"] for score in sentiment_scores]
    df["sentiment_category"] = df["sentiment_compound"].apply(classify_sentiment)
    logger.info("Sentiment analysis complete!")
    return df

def show_extreme_reviews(df, n=5):
    """Display the most positive and negative reviews."""
    logger.info(f"TOP {n} MOST POSITIVE REVIEWS")
    top_positive = df.nlargest(n, "sentiment_compound")
    for idx, row in top_positive.iterrows():
        rating_str = f" | Rating: {row['rating']} stars" if "rating" in df.columns else ""
        logger.info(f"\nScore: {row['sentiment_compound']:.3f}{rating_str}")
        logger.info(f"Review: {row['review_text']}")
    logger.info(f"\nTOP {n} MOST NEGATIVE REVIEWS")
    top_negative = df.nsmallest(n, "sentiment_compound")
    for idx, row in top_negative.iterrows():
        rating_str = f" | Rating: {row['rating']} stars" if "rating" in df.columns else ""
        logger.info(f"\nScore: {row['sentiment_compound']:.3f}{rating_str}")
        logger.info(f"Review: {row['review_text']}")

def complete_sentiment_analysis(csv_file, text_column, rating_column=None, sid=None):
    """Complete sentiment analysis pipeline for customer reviews.

    Args:
        csv_file: Path to CSV file with reviews.
        text_column: Name of column containing review text.
        rating_column: Optional star rating column for comparison.
        sid: Optional SentimentIntensityAnalyzer instance. If None, creates one.

    Returns:
        pandas.DataFrame: DataFrame with sentiment scores and visualizations.
    """
    import pandas as pd
    import nltk

    if sid is None:
        try:
            nltk.download("vader_lexicon", quiet=True)
        except Exception:
            pass
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        sid = SentimentIntensityAnalyzer()

    csv_path = Path(csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    # Load data
    logger.info(f"Loading data from {csv_file}...")
    df = pd.read_csv(csv_file)
    logger.info(f"Loaded {len(df)} reviews")

    # Add sentiment scores
    df = add_sentiment_scores(df, text_column, sid)

    # Show extreme reviews
    show_extreme_reviews(df, n=5)

    # Save results
    output_file = csv_path.parent / (csv_path.stem + "_with_sentiment.csv")
    df.to_csv(output_file, index=False)
    logger.info(f"\nResults saved to: {output_file}")

    return df

def main() -> None:
    """Show how to call the reusable pipeline function.

    This listing primarily defines ``complete_sentiment_analysis`` for reuse in
    later scripts. When run directly, it prints a short usage example.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logger.info("This module provides the complete_sentiment_analysis() function.")
    logger.info("Usage example:")
    logger.info("  df_analyzed = complete_sentiment_analysis(")
    logger.info("      'data/reviews.csv',")
    logger.info("      text_column='text',")
    logger.info("      rating_column='rating'")
    logger.info("  )")

if __name__ == "__main__":
    main()
