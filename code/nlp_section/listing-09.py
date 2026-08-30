"""Demonstrate VADER sentiment analysis on example texts.

This module demonstrates using VADER sentiment analyzer to score text polarity
with examples of positive, negative, and neutral sentiment. Readers learn how to
interpret VADER's compound scores and component scores (negative, neutral, positive).

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 09
"""

import logging

logger = logging.getLogger(__name__)

def analyze_sentiment_example(text, sid):
    """Demonstrate VADER sentiment scoring.

    Args:
        text: Input text string to analyze.
        sid: SentimentIntensityAnalyzer instance.

    Returns:
        dict: Dictionary containing sentiment scores.
    """
    scores = sid.polarity_scores(text)

    logger.info(f"Text: '{text}'")
    logger.info(f"Scores: {scores}")
    logger.info(f"  - Negative: {scores['neg']:.3f}")
    logger.info(f"  - Neutral:  {scores['neu']:.3f}")
    logger.info(f"  - Positive: {scores['pos']:.3f}")
    logger.info(f"  - Compound: {scores['compound']:.3f}")

    return scores

def main() -> None:
    """Test VADER sentiment analysis with example texts."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import nltk

    # Download VADER lexicon if needed
    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception:
        pass

    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()

    examples = [
        "This product is amazing!",
        "This product is terrible.",
        "The product is okay.",
        "LOVE IT!!!",
        "Worst purchase ever. Do not buy.",
    ]

    for example in examples:
        analyze_sentiment_example(example, sid)

if __name__ == "__main__":
    main()
