"""Initialize spaCy NLP model for named entity recognition.

This module demonstrates setting up spaCy for advanced NLP tasks including
named entity recognition. Readers learn how to install and load spaCy models
for extracting structured information from unstructured text.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 28
"""

import logging

logger = logging.getLogger(__name__)

def main() -> None:
    """Load a spaCy NLP model for named entity recognition.

    This listing checks that spaCy is installed and that the small English model
    (``en_core_web_sm``) is available, then loads it.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Install instructions:
    #   pip install spacy
    #   python -m spacy download en_core_web_sm
    try:
        import spacy
    except ModuleNotFoundError:
        logger.warning("SKIPPED: spaCy is not installed.")
        logger.warning("Install with: pip install spacy")
        return

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        logger.warning("spaCy model 'en_core_web_sm' is not installed.")
        logger.warning("Install with: python -m spacy download en_core_web_sm")
        logger.warning("Falling back to a blank English pipeline (no NER/tagger/parser).")
        nlp = spacy.blank("en")

    logger.info("spaCy model loaded successfully: %s", nlp.meta.get("name", "en_core_web_sm"))
    doc = nlp("Apple is looking at buying U.K. startup for $1 billion.")
    logger.info("Tokens: %s", [t.text for t in doc[:10]])
    logger.info("Named entities: %s", [(ent.text, ent.label_) for ent in doc.ents])

if __name__ == "__main__":
    main()
