"""Visualize entity extraction results.

This module demonstrates creating visualizations to explore entity extraction
results including distributions by type and top mentions. Readers learn how
to create comprehensive dashboards for entity analysis.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 32
"""

import logging

logger = logging.getLogger(__name__)

def _entity_candidates_regex(text: str) -> list[str]:
    """Fallback entity extraction using capitalization heuristics."""
    import re

    return re.findall(r"\b[A-Z][a-zA-Z\.]+(?:\s+[A-Z][a-zA-Z\.]+)*\b", text)


def visualize_entities(entities_df):
    """Create visualizations for entity analysis.

    Args:
        entities_df: DataFrame with extracted entities.
    """
    import matplotlib.pyplot as plt
    import os
    from pathlib import Path

    if entities_df.empty:
        logger.warning("No entities to visualize")
        return

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Entity Types Distribution
    entity_type_counts = entities_df["entity_type"].value_counts()
    axes[0, 0].bar(
        entity_type_counts.index, entity_type_counts.values, color="steelblue"
    )
    axes[0, 0].set_xlabel("Entity Type", fontsize=12)
    axes[0, 0].set_ylabel("Count", fontsize=12)
    axes[0, 0].set_title("Distribution of Entity Types", fontsize=14)
    axes[0, 0].tick_params(axis="x", rotation=45)

    # Plot 2: Top Organizations Mentioned
    org_entities = entities_df[entities_df["entity_type"] == "ORG"]
    if len(org_entities) > 0:
        top_orgs = org_entities["entity_text"].value_counts().head(10)
        axes[0, 1].barh(top_orgs.index, top_orgs.values, color="coral")
        axes[0, 1].set_xlabel("Mentions", fontsize=12)
        axes[0, 1].set_title("Top 10 Organizations Mentioned", fontsize=14)
        axes[0, 1].invert_yaxis()

    # Plot 3: Locations Mentioned (GPE)
    gpe_entities = entities_df[entities_df["entity_type"] == "GPE"]
    if len(gpe_entities) > 0:
        top_locations = gpe_entities["entity_text"].value_counts().head(10)
        axes[1, 0].barh(
            top_locations.index, top_locations.values, color="lightgreen"
        )
        axes[1, 0].set_xlabel("Mentions", fontsize=12)
        axes[1, 0].set_title("Top 10 Locations Mentioned", fontsize=14)
        axes[1, 0].invert_yaxis()

    # Plot 4: Products Mentioned
    product_entities = entities_df[entities_df["entity_type"] == "PRODUCT"]
    if len(product_entities) > 0:
        top_products = product_entities["entity_text"].value_counts().head(10)
        axes[1, 1].barh(top_products.index, top_products.values, color="plum")
        axes[1, 1].set_xlabel("Mentions", fontsize=12)
        axes[1, 1].set_title("Top 10 Products Mentioned", fontsize=14)
        axes[1, 1].invert_yaxis()

    plt.tight_layout()

    # Save plot before showing
    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / "img" / "nlp_entity_visualization.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    if os.environ.get("CODE_RUN_ALL") == "1" or not os.environ.get("DISPLAY"):
        plt.close("all")
    else:
        plt.show()

def main():
    """Create entity visualizations from sample data."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import pandas as pd

    try:
        import spacy
    except ModuleNotFoundError:
        logger.warning("spaCy is not installed. Install with: pip install spacy")
        logger.warning("Falling back to a simple regex-based entity heuristic.")
        spacy = None

    try:
        nlp = spacy.load("en_core_web_sm") if spacy is not None else None
    except OSError:
        logger.warning("spaCy model 'en_core_web_sm' not installed.")
        logger.warning("Install with: python -m spacy download en_core_web_sm")
        logger.warning("Falling back to a simple regex-based entity heuristic.")
        nlp = None

    feedback_data = {
        "feedback_id": range(1, 6),
        "text": [
            "I bought a MacBook Pro from Best Buy in New York last month for $2,500. Great service!",
            "The Samsung Galaxy phone I ordered from Amazon arrived broken. Called support on Monday.",
            "Microsoft Surface tablet purchased at Target in Chicago. Price was $899. Very satisfied.",
            "iPhone battery died after 6 months. Apple Store in Boston replaced it for free on Dec 1st.",
            "Got a Dell laptop from Walmart in Texas for $650. The manager, John Smith, was helpful.",
        ],
    }

    df = pd.DataFrame(feedback_data)

    all_entities = []
    for idx, text in enumerate(df["text"]):
        raw = str(text)
        if nlp is None:
            for cand in _entity_candidates_regex(raw):
                all_entities.append(
                    {
                        "document_id": idx,
                        "entity_text": cand,
                        "entity_type": "CANDIDATE",
                        "original_text": raw[:100] + "...",
                    }
                )
        else:
            doc = nlp(raw)
            for ent in doc.ents:
                all_entities.append(
                    {
                        "document_id": idx,
                        "entity_text": ent.text,
                        "entity_type": ent.label_,
                        "original_text": raw[:100] + "...",
                    }
                )

    entities_df = pd.DataFrame(all_entities)
    visualize_entities(entities_df)

if __name__ == "__main__":
    main()
