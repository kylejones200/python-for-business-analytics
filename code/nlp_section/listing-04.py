"""Tokenize text into individual words.

This module demonstrates text tokenization using NLTK's RegexpTokenizer to split
text into words while removing punctuation. Readers learn how to preprocess text
for NLP analysis by breaking it into meaningful units.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 04
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def tokenize_text(text):
    """Convert text into individual words (tokens).

    Removes punctuation and converts to lowercase using regex tokenization.

    Args:
        text: Input text string to tokenize.

    Returns:
        list: List of token strings (words).
    """
    from nltk.tokenize import RegexpTokenizer

    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")

    # Create tokenizer that keeps only word characters
    tokenizer = RegexpTokenizer(r"\w+")

    # Split text into words
    tokens = tokenizer.tokenize(text.lower())

    logger.info(f"Found {len(tokens)} tokens")
    return tokens

def main() -> None:
    """Tokenize text from a local file.

    Reads ``alice_wonderland.txt`` (created by listing-03) and logs a preview of
    the first few tokens.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

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

    tokens = tokenize_text(text)
    logger.info("First 20 tokens: %s", tokens[:20])

if __name__ == "__main__":
    main()
