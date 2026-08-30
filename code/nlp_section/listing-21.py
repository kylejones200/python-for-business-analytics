"""Compare simple vs multiple regression models with interaction terms.

This module demonstrates fitting regression models with interaction terms to
understand how sentiment effects vary by product category. Readers learn how
to model interactions and visualize category-specific effects.

Note: This is exploratory analysis on the full dataset, not a predictive model
with train/test splits, so no leakage checks are needed.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 21
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Compare regression models with interaction terms."""
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

    # Add product categories to our data
    categories = ["Electronics", "Home & Garden", "Clothing", "Sports"] * 25
    listings_df["category"] = categories

    # Regression with category interaction
    model_interaction = ols("price ~ compound * category", data=listings_df).fit()

    logger.info(f"\n{model_interaction.summary()}")

    # Visualize sentiment effect by category
    fig, ax = plt.subplots(figsize=(12, 6))

    for category in listings_df["category"].unique():
        cat_data = listings_df[listings_df["category"] == category]
        ax.scatter(
            cat_data["compound"], cat_data["price"], label=category, alpha=0.6, s=50
        )

    ax.set_xlabel("Sentiment Score (Compound)", fontsize=12)
    ax.set_ylabel("Price ($)", fontsize=12)
    ax.set_title("Sentiment vs Price by Product Category", fontsize=14)
    ax.legend()
    plt.tight_layout()

    # Save plot before showing
    output_path = Path("img/nlp_sentiment_price_by_category.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    plt.show()
    plt.close()

    # Calculate average sentiment by category
    logger.info("\nAverage Sentiment by Category:")
    sentiment_by_cat = (
        listings_df.groupby("category")
        .agg({"compound": "mean", "price": "mean", "listing_id": "count"})
        .rename(columns={"listing_id": "count"})
    )
    logger.info(f"\n{sentiment_by_cat}")

if __name__ == "__main__":
    main()
