"""Complete Named Entity Recognition analysis pipeline function.

This module provides a reusable function for complete NER analysis including
entity extraction, sentiment analysis, pattern analysis, and visualization.
Readers learn how to create modular NLP analysis pipelines.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 34
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def analyze_entities_with_sentiment(df, text_column, nlp):
    """Extract entities and analyze sentiment for each mention."""
    import pandas as pd
    import nltk

    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception:
        pass

    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()
    results = []

    for idx, text in enumerate(df[text_column]):
        sentiment = sid.polarity_scores(str(text))
        doc = nlp(str(text))
        for ent in doc.ents:
            results.append(
                {
                    "document_id": idx,
                    "entity": ent.text,
                    "entity_type": ent.label_,
                    "sentiment_compound": sentiment["compound"],
                    "sentiment_category": (
                        "Positive" if sentiment["compound"] >= 0.05
                        else ("Negative" if sentiment["compound"] <= -0.05 else "Neutral")
                    ),
                    "text_excerpt": text[:100],
                }
            )

    return pd.DataFrame(results)

def analyze_entity_patterns(entities_df):
    """Analyze and visualize entity patterns."""
    if entities_df.empty:
        return None

    entity_type_counts = entities_df["entity_type"].value_counts()
    logger.info(f"\nEntities by Type:\n{entity_type_counts}")
    return entity_type_counts

def visualize_entities(entities_df):
    """Create visualizations for entity analysis."""
    import matplotlib.pyplot as plt

    if entities_df.empty:
        return

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    entity_type_counts = entities_df["entity_type"].value_counts()
    axes[0, 0].bar(entity_type_counts.index, entity_type_counts.values, color="steelblue")
    axes[0, 0].set_xlabel("Entity Type", fontsize=12)
    axes[0, 0].set_ylabel("Count", fontsize=12)
    axes[0, 0].set_title("Distribution of Entity Types", fontsize=14)
    axes[0, 0].tick_params(axis="x", rotation=45)

    org_entities = entities_df[entities_df["entity_type"] == "ORG"]
    if len(org_entities) > 0:
        top_orgs = org_entities["entity_text"].value_counts().head(10)
        axes[0, 1].barh(top_orgs.index, top_orgs.values, color="coral")
        axes[0, 1].set_xlabel("Mentions", fontsize=12)
        axes[0, 1].set_title("Top 10 Organizations Mentioned", fontsize=14)
        axes[0, 1].invert_yaxis()

    gpe_entities = entities_df[entities_df["entity_type"] == "GPE"]
    if len(gpe_entities) > 0:
        top_locations = gpe_entities["entity_text"].value_counts().head(10)
        axes[1, 0].barh(top_locations.index, top_locations.values, color="lightgreen")
        axes[1, 0].set_xlabel("Mentions", fontsize=12)
        axes[1, 0].set_title("Top 10 Locations Mentioned", fontsize=14)
        axes[1, 0].invert_yaxis()

    product_entities = entities_df[entities_df["entity_type"] == "PRODUCT"]
    if len(product_entities) > 0:
        top_products = product_entities["entity_text"].value_counts().head(10)
        axes[1, 1].barh(top_products.index, top_products.values, color="plum")
        axes[1, 1].set_xlabel("Mentions", fontsize=12)
        axes[1, 1].set_title("Top 10 Products Mentioned", fontsize=14)
        axes[1, 1].invert_yaxis()

    plt.tight_layout()
    output_path = Path("img/nlp_complete_ner_analysis.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    plt.show()
    plt.close()

def complete_ner_analysis(csv_file, text_column, output_file=None, nlp=None):
    """Complete Named Entity Recognition analysis pipeline.

    Args:
        csv_file: Path to CSV with text data.
        text_column: Column containing text.
        output_file: Optional path to save results.
        nlp: Optional spaCy language model instance.

    Returns:
        dict: Dictionary with entities DataFrame and analysis results.
    """
    import pandas as pd

    try:
        import spacy
    except ModuleNotFoundError:
        logger.error("spaCy is not installed. Install with: pip install spacy")
        raise SystemExit(1)

    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.error("spaCy model 'en_core_web_sm' not installed.")
            logger.error("Install with: python -m spacy download en_core_web_sm")
            raise SystemExit(1)

    csv_path = Path(csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    # Load data
    logger.info(f"Loading data from {csv_file}...")
    df = pd.read_csv(csv_file)
    logger.info(f"Loaded {len(df)} documents")

    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame")

    # Extract entities with sentiment
    logger.info("\nExtracting entities...")
    entities_df = analyze_entities_with_sentiment(df, text_column, nlp)

    # Analyze patterns
    logger.info("\nAnalyzing patterns...")
    patterns = analyze_entity_patterns(entities_df)

    # Create visualizations
    logger.info("\nCreating visualizations...")
    visualize_entities(entities_df)

    # Calculate entity-sentiment relationships
    logger.info("KEY INSIGHTS")

    # Organizations with most mentions
    top_orgs = (
        entities_df[entities_df["entity_type"] == "ORG"]["entity"]
        .value_counts()
        .head(5)
    )
    logger.info("\nMost mentioned organizations:")
    logger.info(f"\n{top_orgs}")

    # Products with negative sentiment
    negative_products = entities_df[
        (entities_df["entity_type"] == "PRODUCT")
        & (entities_df["sentiment_category"] == "Negative")
    ]
    logger.info(f"\nProducts mentioned in negative contexts: {len(negative_products)}")

    # Save results
    if output_file:
        output_path = Path(output_file)
        entities_df.to_csv(output_path, index=False)
        logger.info(f"\nResults saved to: {output_file}")

    return {
        "entities": entities_df,
        "patterns": patterns,
        "insights": {"top_orgs": top_orgs, "negative_products": negative_products},
    }

def main() -> None:
    """Show how to call the reusable NER pipeline function.

    This listing primarily defines ``complete_ner_analysis``. When run directly,
    it prints a short usage example.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logger.info("This module provides the complete_ner_analysis() function.")
    logger.info("Usage example:")
    logger.info("  results = complete_ner_analysis(")
    logger.info("      'data/reviews.csv',")
    logger.info("      text_column='text',")
    logger.info("      output_file='entities_extracted.csv'")
    logger.info("  )")

if __name__ == "__main__":
    main()
