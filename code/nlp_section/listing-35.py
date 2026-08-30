"""Analyze entities from tech news headlines.

This module demonstrates applying entity extraction to news headlines to
identify companies, locations, and monetary values mentioned. Readers learn
how to analyze entity patterns in domain-specific text data.

Chapter: Introduction to Natural Language Processing for Business Analytics
Source: nlp_section.tex
Extracted listing: 35
"""

import logging

logger = logging.getLogger(__name__)

def _extract_entities_fallback(headline: str) -> list[tuple[str, str]]:
    """Fallback entity extraction for the sample headlines (heuristic)."""
    import re

    companies = {"Apple", "Microsoft", "Google", "Amazon", "Tesla"}
    locations = {"Cupertino", "Mountain View", "Texas", "Berlin"}

    ents: list[tuple[str, str]] = []
    for c in companies:
        if c in headline:
            ents.append((c, "ORG"))
    for loc in locations:
        if loc in headline:
            ents.append((loc, "GPE"))

    for m in re.findall(
        r"\$[0-9,.]+(?:\s*(?:billion|million))?", headline, flags=re.IGNORECASE
    ):
        ents.append((m, "MONEY"))

    return ents


def main() -> None:
    """Extract and analyze entities from tech news headlines."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import pandas as pd

    try:
        import spacy
    except ModuleNotFoundError:
        logger.warning("spaCy is not installed. Install with: pip install spacy")
        logger.warning("Falling back to simple headline heuristics (no NER model).")
        spacy = None

    try:
        nlp = spacy.load("en_core_web_sm") if spacy is not None else None
    except OSError:
        logger.warning("spaCy model 'en_core_web_sm' not installed.")
        logger.warning("Install with: python -m spacy download en_core_web_sm")
        logger.warning("Falling back to simple headline heuristics (no NER model).")
        nlp = None

    # Sample tech news headlines
    tech_news = {
        "headline": [
            "Apple launches new iPhone 16 with AI features in Cupertino",
            "Microsoft acquires startup for $2 billion, CEO Satya Nadella announces",
            "Google unveils Gemini AI in Mountain View, competing with ChatGPT",
            "Amazon opens new fulfillment center in Texas, creating 5,000 jobs",
            "Tesla stock rises 15% after Elon Musk announces new factory in Berlin",
        ]
    }

    news_df = pd.DataFrame(tech_news)

    # Extract entities
    all_entities = []
    for idx, text in enumerate(news_df["headline"]):
        raw = str(text)
        if nlp is None:
            ents = _extract_entities_fallback(raw)
        else:
            doc = nlp(raw)
            ents = [(ent.text, ent.label_) for ent in doc.ents]

        for ent_text, ent_type in ents:
            all_entities.append(
                {
                    "document_id": idx,
                    "entity_text": ent_text,
                    "entity_type": ent_type,
                    "original_text": raw[:100] + "...",
                }
            )

    news_entities = pd.DataFrame(all_entities)

    # Analyze patterns
    logger.info("\nTech Industry Entity Analysis:")
    logger.info("\nCompanies mentioned:")
    org_entities = news_entities[news_entities["entity_type"] == "ORG"]
    if len(org_entities) > 0:
        logger.info(f"\n{org_entities['entity_text'].value_counts()}")

    logger.info("\nLocations:")
    gpe_entities = news_entities[news_entities["entity_type"] == "GPE"]
    if len(gpe_entities) > 0:
        logger.info(f"\n{gpe_entities['entity_text'].value_counts()}")

    logger.info("\nMoney values:")
    money_entities = news_entities[news_entities["entity_type"] == "MONEY"]
    if len(money_entities) > 0:
        logger.info(f"\n{money_entities[['entity_text', 'original_text']]}")

if __name__ == "__main__":
    main()
