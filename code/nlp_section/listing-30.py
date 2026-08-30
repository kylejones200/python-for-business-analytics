"""Extract entities from DataFrame of texts.

This module demonstrates batch processing of multiple texts to extract entities
using spaCy. Readers learn how to process large datasets efficiently and
structure entity extraction results for analysis.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 30
"""

import logging

logger = logging.getLogger(__name__)

def _entity_candidates_regex(text: str) -> list[str]:
    """Fallback entity extraction using capitalization heuristics."""
    import re

    return re.findall(r"\b[A-Z][a-zA-Z\.]+(?:\s+[A-Z][a-zA-Z\.]+)*\b", text)


def extract_entities_from_dataframe(df, text_column, nlp):
    """Extract entities from all texts in a DataFrame.

    Args:
        df: DataFrame with text data.
        text_column: Name of column containing text.
        nlp: spaCy language model instance.

    Returns:
        pandas.DataFrame: DataFrame with entity information.
    """
    import pandas as pd

    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame")

    all_entities = []

    logger.info(f"Processing {len(df)} documents...")

    for idx, text in enumerate(df[text_column]):
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
            # Process text with spaCy
            doc = nlp(raw)
            for ent in doc.ents:
                all_entities.append(
                    {
                        "document_id": idx,
                        "entity_text": ent.text,
                        "entity_type": ent.label_,
                        "original_text": raw[:100] + "...",  # First 100 chars
                    }
                )

    entities_df = pd.DataFrame(all_entities)
    logger.info(f"Extracted {len(entities_df)} entities")

    return entities_df

def main() -> None:
    """Extract entities from sample customer feedback data."""
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
    entities_df = extract_entities_from_dataframe(df, "text", nlp)

    logger.info("Extracted Entities (first 15 rows):\n%s", entities_df.head(15))

if __name__ == "__main__":
    main()
