"""Interpret regression model results and extract key insights.

This module demonstrates interpreting regression coefficients, p-values, and
R-squared values to understand model significance and effect sizes. Readers
learn how to extract and communicate statistical insights from regression models.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 19
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Interpret regression model results."""
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

    # Create sample listings data and fit model
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

    # Fit regression model
    model = ols("price ~ compound", data=listings_df).fit()

    # Extract key metrics
    logger.info("KEY REGRESSION INSIGHTS")

    # Coefficient interpretation
    coef = model.params["compound"]
    pvalue = model.pvalues["compound"]
    r_squared = model.rsquared

    logger.info(f"\nCoefficient (compound): ${coef:.2f}")
    logger.info(f"P-value: {pvalue:.4f}")
    logger.info(f"R-squared: {r_squared:.4f}")

    logger.info("\nInterpretation:")
    if pvalue < 0.05:
        logger.info("OK: Sentiment is statistically significant (p < 0.05)")
        logger.info("OK: A 0.1 increase in sentiment score is associated with")
        logger.info(f"  a ${coef * 0.1:.2f} change in price")
    else:
        logger.info("NOT SIGNIFICANT: Sentiment is NOT statistically significant (p >= 0.05)")
        logger.info("  The relationship may be due to chance")

    logger.info(f"\nModel fit: The sentiment score explains {r_squared*100:.1f}% of")
    logger.info(f"the variation in price (R^2 = {r_squared:.3f})")

if __name__ == "__main__":
    main()
