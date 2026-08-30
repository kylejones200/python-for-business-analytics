"""Complete NLP pipeline from URL to frequency analysis.

This module demonstrates a complete NLP workflow: fetching text from URLs,
tokenizing, removing stopwords, and analyzing word frequencies. Readers learn
how to combine multiple NLP steps into a cohesive pipeline.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 07
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def analyze_text_from_url(url, top_n=30):
    """Complete NLP pipeline from URL to frequency analysis.

    Args:
        url: URL string to fetch text from.
        top_n: Number of top words to display.

    Returns:
        dict: Dictionary containing analysis results, or None if error occurs.
    """
    import matplotlib.pyplot as plt
    import nltk
    from bs4 import BeautifulSoup
    from nltk.corpus import stopwords
    from nltk.tokenize import RegexpTokenizer
    from urllib.request import urlopen

    # Step 1: Fetch text
    logger.info("Step 1: Fetching text...")
    try:
        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text().lower()
        logger.info(f"Successfully fetched {len(text)} characters")
    except Exception as e:
        logger.error(f"Error fetching text: {e}")
        return None

    # Step 2: Tokenize
    logger.info("Step 2: Tokenizing...")
    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)
    logger.info(f"Found {len(tokens)} tokens")

    # Step 3: Remove stop words
    logger.info("Step 3: Removing stop words...")
    stop_words = set(stopwords.words("english"))
    meaningful_tokens = [word for word in tokens if word not in stop_words]
    logger.info(f"Kept {len(meaningful_tokens)} meaningful tokens")

    # Step 4: Analyze frequency
    logger.info("Step 4: Analyzing frequencies...")
    freq_dist = nltk.FreqDist(meaningful_tokens)
    most_common = freq_dist.most_common(top_n)
    logger.info(f"Top {top_n} most frequent words:")
    for word, count in most_common[:10]:
        logger.info(f"{word:20s}: {count:4d}")

    # Step 5: Create visualization
    logger.info("Step 5: Creating visualization...")
    plt.figure(figsize=(12, 6))
    freq_dist.plot(top_n, cumulative=False)
    plt.title(f"Top {top_n} Most Frequent Words", fontsize=14)
    plt.tight_layout()

    # Save plot before showing
    output_path = Path("img/nlp_pipeline_analysis.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    plt.show()
    plt.close()

    # Return results
    results = {
        "original_text": text,
        "all_tokens": tokens,
        "meaningful_tokens": meaningful_tokens,
        "frequency_distribution": freq_dist,
        "total_words": len(tokens),
        "unique_words": len(set(tokens)),
        "meaningful_words": len(meaningful_tokens),
    }

    return results

def main():
    """Run complete NLP pipeline."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# Use the complete pipeline
    results = analyze_text_from_url(
        "https://www.gutenberg.org/cache/epub/11/pg11-images.html", top_n=30
    )

    if results is None:
        logger.error("Pipeline failed. Exiting.")
        raise SystemExit(1)

    # Log summary statistics
    logger.info("SUMMARY STATISTICS")
    logger.info(f"Total words: {results['total_words']:,}")
    logger.info(f"Unique words: {results['unique_words']:,}")
    logger.info(f"After filtering: {results['meaningful_words']:,}")

if __name__ == "__main__":
    main()
