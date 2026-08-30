"""Compare simple vs multiple regression models.

This module demonstrates fitting multiple regression models with different
predictors and comparing model performance using R-squared. Readers learn how
to evaluate whether adding more predictors improves model fit.

Note: This is exploratory analysis on the full dataset, not a predictive model
with train/test splits, so no leakage checks are needed.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 20
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Compare simple and multiple regression models."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import numpy as np
    import pandas as pd
    import nltk
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

    # Fit simple model
    model = ols("price ~ compound", data=listings_df).fit()

    # Multiple regression with all sentiment scores
    model_multi = ols("price ~ compound + neg + neu + pos", data=listings_df).fit()

    logger.info(f"\n{model_multi.summary()}")

    # Compare models
    logger.info("MODEL COMPARISON")
    logger.info(f"Simple model R^2: {model.rsquared:.4f}")
    logger.info(f"Multiple model R^2: {model_multi.rsquared:.4f}")
    logger.info(f"Improvement: {(model_multi.rsquared - model.rsquared)*100:.2f}%")

if __name__ == "__main__":
    main()
