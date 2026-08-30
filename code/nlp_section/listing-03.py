"""Fetch and extract text from web pages.

This module demonstrates web scraping using BeautifulSoup to extract clean text
from HTML pages. Readers learn how to fetch web content, parse HTML, and extract
textual data for NLP analysis.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 03
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def fetch_text_from_url(url):
    """Fetch and clean text from a URL.

    Args:
        url: URL string to fetch text from.

    Returns:
        str: Cleaned text string in lowercase, or None if error occurs.
    """
    try:
        from bs4 import BeautifulSoup
        from urllib.request import urlopen

        # Fetch the webpage
        html = urlopen(url)

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Extract text and convert to lowercase
        text = soup.get_text().lower()

        logger.info(f"Successfully fetched {len(text)} characters")
        return text

    except Exception as e:
        logger.error(f"Error fetching text: {e}")
        return None

def main():
    """Fetch text from URL and save to file."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Fetch Alice in Wonderland
    url = "https://www.gutenberg.org/cache/epub/11/pg11-images.html"
    text = fetch_text_from_url(url)

    if text is None:
        logger.error("Failed to fetch text. Exiting.")
        raise SystemExit(1)

    # Save for later use
    output_file = Path("alice_wonderland.txt")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Text saved to {output_file}")
        logger.info(f"First 200 characters:\n{text[:200]}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise

if __name__ == "__main__":
    main()
