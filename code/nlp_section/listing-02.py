"""Download NLTK data resources.

This module demonstrates downloading NLTK datasets required for text processing,
including stopwords and tokenizers. Readers learn how to set up NLTK resources
for NLP tasks.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 02
"""

import logging

logger = logging.getLogger(__name__)

def main() -> None:
    """Download required NLTK data resources.

    Downloads the NLTK ``stopwords`` corpus and the ``punkt`` tokenizer so other
    listings can tokenize text and remove common words.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import nltk

    logger.info("Downloading NLTK stopwords...")
    nltk.download("stopwords", quiet=True)
    logger.info("Downloading NLTK punkt tokenizer...")
    nltk.download("punkt", quiet=True)
    logger.info("NLTK data download complete.")

if __name__ == "__main__":
    main()
