"""Initialize VADER sentiment analyzer.

This module demonstrates setting up NLTK's VADER (Valence Aware Dictionary and
sEntiment Reasoner) sentiment analyzer. Readers learn how to download and
initialize sentiment analysis tools for analyzing text polarity.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 08
"""

import logging

logger = logging.getLogger(__name__)

def main() -> None:
    """Download VADER lexicon and initialize the sentiment analyzer."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    logger.info("Downloading VADER lexicon (one-time setup)...")
    nltk.download("vader_lexicon", quiet=True)

    sid = SentimentIntensityAnalyzer()
    example = "This product is surprisingly good!"
    logger.info("Initialized VADER. Example score for %r: %s", example, sid.polarity_scores(example))

if __name__ == "__main__":
    main()
