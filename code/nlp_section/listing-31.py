"""Analyze entity patterns and frequencies.

This module demonstrates analyzing extracted entities to identify patterns,
frequencies, and common mentions. Readers learn how to summarize and interpret
entity extraction results for business insights.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 31
"""

import logging

logger = logging.getLogger(__name__)

def _entity_candidates_regex(text: str) -> list[str]:
    """Fallback entity extraction using capitalization heuristics."""
    import re

    return re.findall(r"\b[A-Z][a-zA-Z\.]+(?:\s+[A-Z][a-zA-Z\.]+)*\b", text)


def analyze_entity_patterns(entities_df):
    """Analyze and visualize entity patterns.

    Args:
        entities_df: DataFrame with extracted entities.

    Returns:
        pandas.Series: Entity type counts.
    """
    if entities_df.empty:
        logger.warning("No entities found to analyze")
        return None

    logger.info("ENTITY ANALYSIS")

    # Count entities by type
    logger.info("\nEntities by Type:")
    entity_type_counts = entities_df["entity_type"].value_counts()
    logger.info(f"\n{entity_type_counts}")

    # Most frequently mentioned entities by type
    for entity_type in ["ORG", "PRODUCT", "GPE", "MONEY"]:
        if entity_type in entities_df["entity_type"].values:
            logger.info(f"\nTop {entity_type} mentions:")
            type_entities = entities_df[entities_df["entity_type"] == entity_type]
            top_entities = type_entities["entity_text"].value_counts().head(5)
            logger.info(f"\n{top_entities}")

    return entity_type_counts

def main() -> None:
    """Analyze entity patterns from sample data."""
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

    all_entities = []
    for idx, text in enumerate(df["text"]):
        raw = str(text)
        if nlp is None:
            for cand in _entity_candidates_regex(raw):
                all_entities.append(
                    {
                        "document_id": idx,
                        "entity_text": cand,
                        "entity_type": "CANDIDATE",
                        "original_text": raw[:100] + "...",
                    }
                )
        else:
            doc = nlp(raw)
            for ent in doc.ents:
                all_entities.append(
                    {
                        "document_id": idx,
                        "entity_text": ent.text,
                        "entity_type": ent.label_,
                        "original_text": raw[:100] + "...",
                    }
                )

    entities_df = pd.DataFrame(all_entities)
    analyze_entity_patterns(entities_df)

if __name__ == "__main__":
    main()
