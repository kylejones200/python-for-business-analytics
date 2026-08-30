"""Combine entity extraction with sentiment analysis.

This module demonstrates combining named entity recognition with sentiment
analysis to understand sentiment associated with specific entities. Readers
learn how to integrate multiple NLP techniques for deeper insights.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 33
"""

import logging

logger = logging.getLogger(__name__)

def _entity_candidates_regex(text: str) -> list[str]:
    """Fallback entity extraction using capitalization heuristics."""
    import re

    return re.findall(r"\b[A-Z][a-zA-Z\.]+(?:\s+[A-Z][a-zA-Z\.]+)*\b", text)


def analyze_entities_with_sentiment(df, text_column, nlp):
    """Extract entities and analyze sentiment for each mention.

    Args:
        df: DataFrame with text data.
        text_column: Name of column containing text.
        nlp: spaCy language model instance.

    Returns:
        pandas.DataFrame: DataFrame with entities and associated sentiment.
    """
    import pandas as pd
    import nltk

    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame")

    # Download VADER lexicon if needed (network may be unavailable).
    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception:
        pass

    sid = None
    try:
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        sid = SentimentIntensityAnalyzer()
    except LookupError:
        logger.warning("NLTK vader_lexicon not available; using a naive sentiment fallback.")
        sid = None

    results = []

    for idx, text in enumerate(df[text_column]):
        # Get overall sentiment
        raw = str(text)
        if sid is not None:
            sentiment = sid.polarity_scores(raw)
        else:
            # Naive fallback: simple keyword scoring (teaching-only).
            pos = sum(w in raw.lower() for w in ["great", "helpful", "satisfied", "free"])
            neg = sum(w in raw.lower() for w in ["broken", "died", "issues", "problem"])
            compound = (pos - neg) / max(pos + neg, 1)
            sentiment = {"compound": float(compound)}

        # Extract entities
        if nlp is None:
            candidates = _entity_candidates_regex(raw)
            ents = [(c, "CANDIDATE") for c in candidates]
        else:
            doc = nlp(raw)
            ents = [(ent.text, ent.label_) for ent in doc.ents]

        for ent_text, ent_type in ents:
            results.append(
                {
                    "document_id": idx,
                    "entity": ent_text,
                    "entity_type": ent_type,
                    "sentiment_compound": sentiment["compound"],
                    "sentiment_category": (
                        "Positive"
                        if sentiment["compound"] >= 0.05
                        else ("Negative" if sentiment["compound"] <= -0.05 else "Neutral")
                    ),
                    "text_excerpt": raw[:100],
                }
            )

    return pd.DataFrame(results)

def main() -> None:
    """Analyze entities with sentiment from sample data."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import pandas as pd

    try:
        import spacy
    except ModuleNotFoundError:
        logger.warning("spaCy is not installed. Install with: pip install spacy")
        logger.warning("Falling back to a simple regex-based entity heuristic.")
        spacy = None

    try:
        nlp = spacy.load("en_core_web_sm") if spacy is not None else None
    except OSError:
        logger.warning("spaCy model 'en_core_web_sm' not installed.")
        logger.warning("Install with: python -m spacy download en_core_web_sm")
        logger.warning("Falling back to a simple regex-based entity heuristic.")
        nlp = None

    feedback_data = {
        "feedback_id": range(1, 6),
        "text": [
            "I bought a MacBook Pro from Best Buy in New York last month for $2,500. Great service!",
            "The Samsung Galaxy phone I ordered from Amazon arrived broken. Called support on Monday.",
            "Microsoft Surface tablet purchased at Target in Chicago. Price was $899. Very satisfied.",
            "iPhone battery died after 6 months. Apple Store in Boston replaced it for free on Dec 1st.",
            "Got a Dell laptop from Walmart in Texas for $650. The manager, John Smith, was helpful.",
        ],
    }

    df = pd.DataFrame(feedback_data)

    entity_sentiment_df = analyze_entities_with_sentiment(df, "text", nlp)

    # Find products with negative sentiment
    logger.info("PRODUCTS MENTIONED IN NEGATIVE REVIEWS")

    negative_products = entity_sentiment_df[
        (entity_sentiment_df["entity_type"] == "PRODUCT")
        & (entity_sentiment_df["sentiment_category"] == "Negative")
    ]

    logger.info(f"\n{negative_products[['entity', 'sentiment_compound', 'text_excerpt']]}")

    # Calculate average sentiment by organization
    logger.info("AVERAGE SENTIMENT BY ORGANIZATION")

    org_sentiment = (
        entity_sentiment_df[entity_sentiment_df["entity_type"] == "ORG"]
        .groupby("entity")["sentiment_compound"]
        .agg(["mean", "count"])
    )

    logger.info(f"\n{org_sentiment.sort_values('mean', ascending=False)}")

if __name__ == "__main__":
    main()
