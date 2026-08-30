"""Analyze word frequency distributions.

This module demonstrates frequency analysis of tokens using NLTK's FreqDist to
identify the most common words in text. Readers learn how to analyze word
distributions and visualize them with matplotlib.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 06
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def analyze_frequency(tokens, top_n=30):
    """Count word frequencies and display results.

    Args:
        tokens: List of token strings to analyze.
        top_n: Number of top words to display.

    Returns:
        nltk.FreqDist: Frequency distribution object.
    """
    import nltk

    if not tokens:
        raise ValueError("Input tokens list cannot be empty")

    # Calculate frequency distribution
    freq_dist = nltk.FreqDist(tokens)

    # Get most common words
    most_common = freq_dist.most_common(top_n)

    # Log top words
    logger.info(f"Top {top_n} most frequent words:")
    for word, count in most_common[:10]:
        logger.info(f"{word:20s}: {count:4d}")

    return freq_dist

def main() -> None:
    """Analyze word frequencies and create a visualization.

    Loads ``alice_wonderland.txt`` (created by listing-03), removes stopwords,
    computes a frequency distribution, and saves a bar-style frequency plot.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import matplotlib.pyplot as plt
    from nltk.corpus import stopwords
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
    stop_words = set(stopwords.words("english"))
    meaningful_tokens = [word for word in tokens if word not in stop_words]

    freq_dist = analyze_frequency(meaningful_tokens)

    plt.figure(figsize=(12, 6))
    freq_dist.plot(30, cumulative=False)
    plt.title("Top 30 Most Frequent Words", fontsize=14)
    plt.xlabel("Words", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = project_root / "img" / "nlp_frequency_analysis.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info("Plot saved to %s", output_path)
    import os

    if os.environ.get("CODE_RUN_ALL") == "1" or not os.environ.get("DISPLAY"):
        plt.close("all")
    else:
        plt.show()

if __name__ == "__main__":
    main()
