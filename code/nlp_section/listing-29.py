"""Extract named entities from text using spaCy.

This module demonstrates using spaCy to extract named entities (people, places,
organizations, etc.) from text. Readers learn how to identify and categorize
entities in unstructured text data.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 29
"""

import logging

logger = logging.getLogger(__name__)

def extract_entities_regex(text: str) -> list[str]:
    """Fallback entity extraction using capitalization heuristics.

    Args:
        text: Input text.

    Returns:
        List of extracted candidate entity phrases.
    """
    import re

    # Simple heuristic: sequences of capitalized tokens (e.g., "Sarah Johnson", "Apple Store").
    return re.findall(r"\b[A-Z][a-zA-Z\.]+(?:\s+[A-Z][a-zA-Z\.]+)*\b", text)


def extract_entities(text, nlp):
    """Extract and display named entities from text.

    Args:
        text: Input text string to analyze.
        nlp: spaCy language model instance.

    Returns:
        spacy.tokens.Doc: Processed spaCy document object.
    """
    import spacy

    # Process the text with spaCy
    doc = nlp(text)

    # Extract entities
    logger.info(f"Text: {text}")
    logger.info("\nEntities found:")

    for ent in doc.ents:
        logger.info(f"{ent.text:25s} | {ent.label_:15s} | {spacy.explain(ent.label_)}")

    return doc

def main() -> None:
    """Extract entities from an example customer service transcript."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        import spacy
    except ModuleNotFoundError:
        logger.warning("SKIPPED: spaCy is not installed. Install with: pip install spacy")
        logger.warning("Fallback: using a simple regex-based entity heuristic.")
        spacy = None

    try:
        nlp = spacy.load("en_core_web_sm") if spacy is not None else None
    except OSError:
        logger.warning("spaCy model 'en_core_web_sm' not installed.")
        logger.warning("Install with: python -m spacy download en_core_web_sm")
        logger.warning("Fallback: using a simple regex-based entity heuristic.")
        nlp = None

    text = (
        "I purchased an iPhone 15 from the Apple Store in Seattle on January 15th, "
        "2024 for $999. The customer service representative, Sarah Johnson, was very "
        "helpful. However, when I compared it to Samsung's latest model, I noticed "
        "some issues. I called Amazon customer support last Tuesday and they suggested "
        "returning it to the store on 5th Avenue."
    )

    if nlp is None:
        candidates = extract_entities_regex(text)
        logger.info("Text: %s", text)
        logger.info("\nEntity candidates (regex heuristic):")
        for c in candidates[:20]:
            logger.info("%s", c)
        return

    extract_entities(text, nlp)

if __name__ == "__main__":
    main()
