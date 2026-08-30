"""Fit regression model with amenities and sentiment features.

This module demonstrates fitting regression models using both extracted keyword
features and sentiment scores as predictors. Readers learn how to combine
structured and unstructured features in predictive models.

Note: This is exploratory analysis on the full dataset, not a predictive model
with train/test splits, so no leakage checks are needed.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 26
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Fit regression model with amenities and sentiment."""
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

    # Create sample listing data
    listings_extended = {
        "listing_id": range(1, 21),
        "description": [
            "Beautiful home with WiFi and cable TV. Pet friendly!",
            "Modern apartment with high-speed WiFi. No pets allowed.",
            "Cozy space with cable TV. Cat friendly, no dogs.",
            "Luxurious villa with WiFi, cable TV, and pet-friendly policy.",
            "Basic room with WiFi. Pets welcome!",
            "Premium suite with all amenities. No pets.",
            "Charming cottage with WiFi and cable. Dogs and cats welcome.",
            "Downtown loft with WiFi. Pet-free environment.",
            "Family home with cable TV. Cat friendly.",
            "Modern condo with WiFi and cable TV. No pets.",
            "Rustic cabin with WiFi. Pet friendly!",
            "Urban apartment with cable TV. No pets allowed.",
            "Beach house with WiFi. Dogs welcome!",
            "Mountain retreat with cable TV. Pet friendly.",
            "City center flat with WiFi. No pets.",
            "Suburban home with cable TV and WiFi. Cat friendly.",
            "Lake house with WiFi. Pet-free property.",
            "Country estate with cable TV. Dogs and cats allowed.",
            "Studio with WiFi. No pets permitted.",
            "Penthouse with WiFi and cable. Pet friendly!",
        ],
        "price": [
            150, 200, 175, 300, 100, 250, 180, 220, 160, 210,
            130, 190, 170, 140, 230, 165, 240, 155, 205, 280,
        ],
    }

    df_listings = pd.DataFrame(listings_extended)

    # Create keyword features
    watch_words = ["wifi", "cable tv", "pet", "cat", "dog"]
    for keyword in watch_words:
        df_listings[keyword] = (
            df_listings["description"].str.lower().str.contains(keyword).astype(int)
        )
    df_listings["pet"] = (
        (df_listings["pet"] | df_listings["cat"] | df_listings["dog"]).astype(int)
    )

    # Add sentiment to our listings
    sentiment_scores = [
        sid.polarity_scores(str(text)) for text in df_listings["description"]
    ]
    df_listings = pd.concat([df_listings, pd.DataFrame(sentiment_scores)], axis=1)

    # Regression: price predicted by amenities and sentiment
    model = ols("price ~ wifi + pet + compound", data=df_listings).fit()

    logger.info(f"\n{model.summary()}")

    # Extract and interpret coefficients
    logger.info("COEFFICIENT INTERPRETATION")

    for var in ["wifi", "pet", "compound"]:
        coef = model.params[var]
        pval = model.pvalues[var]
        sig = "Significant" if pval < 0.05 else "Not significant"
        logger.info(f"\n{var.capitalize()}:")
        logger.info(f"  Coefficient: ${coef:.2f}")
        logger.info(f"  P-value: {pval:.4f} {sig}")

        if var in ["wifi", "pet"]:
            logger.info(f"  Interpretation: Listings with {var} are associated with")
            logger.info(f"                 a ${coef:.2f} price difference")
        else:
            logger.info(f"  Interpretation: 0.1 increase in sentiment -> ${coef*0.1:.2f}")

if __name__ == "__main__":
    main()
