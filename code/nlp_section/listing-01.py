"""Introduction to NLP libraries and setup.

This module demonstrates importing essential NLP libraries including BeautifulSoup
for web scraping, NLTK for text processing, and matplotlib for visualization.
Readers learn how to set up the NLP toolkit for text analysis tasks.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 01
"""

import logging

logger = logging.getLogger(__name__)

def main():
    """Main function to demonstrate NLP library imports."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# Install required packages (run once)
    # pip install beautifulsoup4 nltk matplotlib

    from bs4 import BeautifulSoup  # noqa: F401
    from urllib.request import urlopen  # noqa: F401
    import nltk  # noqa: F401
    from nltk.tokenize import RegexpTokenizer  # noqa: F401
    from nltk.corpus import stopwords  # noqa: F401
    import matplotlib.pyplot as plt  # noqa: F401

    logger.info("NLP libraries imported successfully")

if __name__ == "__main__":
    main()
