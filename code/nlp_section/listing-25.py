"""Create cross-tabulations for categorical features.

This module demonstrates using pandas crosstab to analyze relationships between
categorical variables. Readers learn how to create contingency tables and
calculate percentages for categorical data analysis.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 25
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Create cross-tabulations for pet policies."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import pandas as pd

    # Seed randomness for reproducibility
    random.seed(42)

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

    # How many listings have both cats and dogs?
    logger.info("\nCross-tabulation: Cat vs Dog Policies")
    ct = pd.crosstab(df_listings["cat"], df_listings["dog"], margins=True)
    ct.index = ["No Cats", "Cats OK", "Total"]
    ct.columns = ["No Dogs", "Dogs OK", "Total"]
    logger.info(f"\n{ct}")

    # As percentages
    logger.info("\nAs percentages of total:")
    ct_pct = pd.crosstab(df_listings["cat"], df_listings["dog"], normalize=True) * 100
    ct_pct.index = ["No Cats", "Cats OK"]
    ct_pct.columns = ["No Dogs", "Dogs OK"]
    logger.info(f"\n{ct_pct.round(1)}")

if __name__ == "__main__":
    main()
