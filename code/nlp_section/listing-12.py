"""Compare performance of .apply() vs list comprehension for sentiment analysis.

This module demonstrates performance differences between pandas .apply() and list
comprehension when processing large datasets. Readers learn that list comprehension
is typically faster for sentiment analysis tasks.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 12
"""

import logging
import random
import time

logger = logging.getLogger(__name__)

def main() -> None:
    """Compare performance of different methods for sentiment analysis."""
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

    # Create a dataset with 10,000 reviews
    large_review_data = {
        "review_id": range(1, 10001),
        "review_text": [
            (
                "This product is amazing!"
                if i % 2 == 0
                else "Terrible quality, very disappointed."
            )
            for i in range(10000)
        ],
    }

    df_large = pd.DataFrame(large_review_data)

    logger.info(f"Testing with {len(df_large)} reviews\n")

    # Method 1: Using .apply() with lambda
    logger.info("Method 1: Using .apply() with lambda")
    start_time = time.time()
    df_large["scores_apply"] = df_large["review_text"].apply(
        lambda text: sid.polarity_scores(str(text))
    )
    apply_time = time.time() - start_time
    logger.info(f"Time: {apply_time:.2f} seconds\n")

    # Method 2: Using list comprehension
    logger.info("Method 2: Using list comprehension")
    start_time = time.time()
    df_large["scores_list_comp"] = [
        sid.polarity_scores(str(text)) for text in df_large["review_text"]
    ]
    list_comp_time = time.time() - start_time
    logger.info(f"Time: {list_comp_time:.2f} seconds\n")

    # Calculate speedup
    speedup = (apply_time / list_comp_time - 1) * 100
    logger.info(f"List comprehension is {speedup:.1f}% faster!")

if __name__ == "__main__":
    main()
