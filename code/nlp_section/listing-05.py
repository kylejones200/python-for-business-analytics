"""Remove stopwords from tokenized text.

This module demonstrates filtering common stopwords from tokenized text using
NLTK's stopword corpus. Readers learn how to remove noise words that don't
carry semantic meaning to focus on meaningful content.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 05
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def remove_stopwords(tokens):
    """Filter out common words that don't carry much meaning.

    Args:
        tokens: List of token strings to filter.

    Returns:
        list: Filtered list of tokens with stopwords removed.
    """
    from nltk.corpus import stopwords

    if not tokens:
        raise ValueError("Input tokens list cannot be empty")

    # Get English stop words
    stop_words = set(stopwords.words("english"))

    # Keep only words NOT in the stop words list
    filtered_tokens = [word for word in tokens if word not in stop_words]

    logger.info(f"Removed {len(tokens) - len(filtered_tokens)} stop words")
    logger.info(f"Kept {len(filtered_tokens)} meaningful tokens")

    return filtered_tokens

def main() -> None:
    """Remove stopwords from tokenized text.

    Loads ``alice_wonderland.txt`` (created by listing-03), tokenizes it, and
    removes common English stopwords using NLTK.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    from nltk.tokenize import RegexpTokenizer

    project_root = Path(__file__).resolve().parents[2]
    text_file = project_root / "alice_wonderland.txt"
    if not text_file.exists():
        logger.error("Text file not found: %s", text_file)
        logger.error(
            "Run `python code/nlp_section/listing-03.py` first to fetch the text."
        )
        raise SystemExit(1)

    text = text_file.read_text(encoding="utf-8")
    if not text.strip():
        logger.error("Text file is empty: %s", text_file)
        raise SystemExit(1)

    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text.lower())
    logger.info("Found %d tokens", len(tokens))

    meaningful_tokens = remove_stopwords(tokens)

    logger.info("Original first 20: %s", tokens[:20])
    logger.info("Filtered first 20: %s", meaningful_tokens[:20])

if __name__ == "__main__":
    main()
