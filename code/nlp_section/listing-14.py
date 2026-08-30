"""Create sentiment analysis visualization dashboard.

This module demonstrates creating comprehensive visualizations of sentiment analysis
results including distributions, category breakdowns, and relationships with ratings.
Readers learn how to create multi-panel dashboards for exploring sentiment data.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 14
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Create a sentiment analysis visualization dashboard."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import matplotlib.pyplot as plt
    import pandas as pd
    import nltk
    from pathlib import Path

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

    # Classify sentiment
    def classify_sentiment(compound):
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    df["sentiment_category"] = df["sentiment_compound"].apply(classify_sentiment)

    # Create visualization dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Distribution of Compound Scores
    axes[0, 0].hist(
        df["sentiment_compound"], bins=20, color="skyblue", edgecolor="black"
    )
    axes[0, 0].axvline(x=0, color="red", linestyle="--", label="Neutral")
    axes[0, 0].set_xlabel("Compound Sentiment Score", fontsize=12)
    axes[0, 0].set_ylabel("Number of Reviews", fontsize=12)
    axes[0, 0].set_title("Distribution of Sentiment Scores", fontsize=14)
    axes[0, 0].legend()

    # Plot 2: Sentiment Categories
    sentiment_counts = df["sentiment_category"].value_counts()
    axes[0, 1].bar(
        sentiment_counts.index, sentiment_counts.values, color=["green", "gray", "red"]
    )
    axes[0, 1].set_xlabel("Sentiment Category", fontsize=12)
    axes[0, 1].set_ylabel("Number of Reviews", fontsize=12)
    axes[0, 1].set_title("Review Sentiment Breakdown", fontsize=14)

    # Plot 3: Sentiment vs Star Rating
    rating_sentiment = df.groupby("rating")["sentiment_compound"].mean()
    axes[1, 0].plot(
        rating_sentiment.index,
        rating_sentiment.values,
        marker="o",
        linewidth=2,
        markersize=8,
    )
    axes[1, 0].set_xlabel("Star Rating", fontsize=12)
    axes[1, 0].set_ylabel("Average Sentiment Score", fontsize=12)
    axes[1, 0].set_title("Star Rating vs Sentiment Score", fontsize=14)

    # Plot 4: Sentiment by Product
    if "product" in df.columns:
        product_sentiment = (
            df.groupby("product")["sentiment_compound"].mean().sort_values()
        )
        axes[1, 1].barh(product_sentiment.index, product_sentiment.values)
        axes[1, 1].axvline(x=0, color="red", linestyle="--")
        axes[1, 1].set_xlabel("Average Sentiment Score", fontsize=12)
        axes[1, 1].set_title("Sentiment by Product", fontsize=14)

    plt.tight_layout()

    # Save plot before showing
    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / "img" / "nlp_sentiment_dashboard.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info("Plot saved to %s", output_path)
    plt.show()
    plt.close()

    # Log summary statistics
    logger.info("SENTIMENT ANALYSIS SUMMARY")
    logger.info(f"Total reviews analyzed: {len(df)}")
    logger.info("\nSentiment breakdown:")
    logger.info(f"\n{df['sentiment_category'].value_counts()}")
    logger.info(f"\nAverage sentiment score: {df['sentiment_compound'].mean():.3f}")
    logger.info(f"Most positive review: {df['sentiment_compound'].max():.3f}")
    logger.info(f"Most negative review: {df['sentiment_compound'].min():.3f}")

if __name__ == "__main__":
    main()
