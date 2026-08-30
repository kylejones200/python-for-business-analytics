"""Visualize amenity features and price relationships.

This module demonstrates creating multi-panel visualizations to explore
relationships between amenities and prices. Readers learn how to create
comprehensive visualization dashboards for feature analysis.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 27
"""

import logging
import random

logger = logging.getLogger(__name__)

def main() -> None:
    """Create visualizations for amenity-price relationships."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import matplotlib.pyplot as plt
    import pandas as pd
    from pathlib import Path

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
    df_listings["pet"] = (
        (df_listings["pet"] | df_listings["cat"] | df_listings["dog"]).astype(int)
    )

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Price by WiFi
    wifi_prices = df_listings.groupby("wifi")["price"].mean()
    axes[0, 0].bar(
        ["No WiFi", "WiFi"], wifi_prices.values, color=["coral", "steelblue"]
    )
    axes[0, 0].set_ylabel("Average Price ($)", fontsize=12)
    axes[0, 0].set_title("Average Price by WiFi Availability", fontsize=14)

    # Plot 2: Price by Pet Policy
    pet_prices = df_listings.groupby("pet")["price"].mean()
    axes[0, 1].bar(
        ["No Pets", "Pet Friendly"],
        pet_prices.values,
        color=["lightcoral", "lightgreen"],
    )
    axes[0, 1].set_ylabel("Average Price ($)", fontsize=12)
    axes[0, 1].set_title("Average Price by Pet Policy", fontsize=14)

    # Plot 3: Amenity Frequency
    amenity_freq = df_listings[watch_words].sum()
    axes[1, 0].barh(watch_words, amenity_freq.values, color="plum")
    axes[1, 0].set_xlabel("Number of Listings", fontsize=12)
    axes[1, 0].set_title("Amenity Frequency Across Listings", fontsize=14)

    # Plot 4: Price Distribution by Pet and WiFi
    for has_pet in [0, 1]:
        for has_wifi in [0, 1]:
            subset = df_listings[
                (df_listings["pet"] == has_pet) & (df_listings["wifi"] == has_wifi)
            ]
            label = (
                f"{'Pet' if has_pet else 'No Pet'}, {'WiFi' if has_wifi else 'No WiFi'}"
            )
            if len(subset) > 0:
                axes[1, 1].scatter(
                    [label] * len(subset), subset["price"], alpha=0.6, s=50
                )

    axes[1, 1].set_ylabel("Price ($)", fontsize=12)
    axes[1, 1].set_title("Price Distribution by Amenity Combination", fontsize=14)
    axes[1, 1].tick_params(axis="x", rotation=45)

    plt.tight_layout()

    # Save plot before showing
    output_path = Path("img/nlp_amenity_price_analysis.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()
