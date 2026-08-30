"""Extract keyword features from text descriptions.

This module demonstrates creating dummy variables from text by searching for
specific keywords. Readers learn how to convert unstructured text into binary
features for machine learning models.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 22
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Extract keyword features from listing descriptions."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import pandas as pd

    # Seed randomness for reproducibility
    random.seed(42)

    # Create sample listing data with amenity descriptions
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

    # Define keywords we want to track
    watch_words = ["wifi", "cable tv", "pet", "cat", "dog"]

    # Create dummy variables for each keyword
    # Convert to lowercase to catch all variations (WiFi, wifi, WIFI)
    for keyword in watch_words:
        df_listings[keyword] = (
            df_listings["description"].str.lower().str.contains(keyword).astype(int)
        )

    # Create pet-friendly indicator (if pet, cat, or dog mentioned)
    df_listings["pet"] = (
        (df_listings["pet"] | df_listings["cat"] | df_listings["dog"]).astype(int)
    )

    # Display the results
    logger.info("Listings with Extracted Features:")
    logger.info(f"\n{df_listings[['listing_id', 'description', 'price'] + watch_words + ['pet']].head(10)}")

if __name__ == "__main__":
    main()
