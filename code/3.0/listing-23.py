"""

This script demonstrates choosing appropriate figure sizes for different
output formats. Readers learn to select dimensions for PowerPoint slides,
academic papers, dashboards, and social media.
"""

import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def main():
    """Demonstrate figure size options for different use cases."""
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s: %(message)s'
    )
    # PowerPoint slide (16:9)
    fig = plt.figure(figsize=(10, 5.625))
    logger.info("PowerPoint slide (16:9): figsize=(10, 5.625)")
    plt.close(fig)

    # Academic paper (single column)
    fig = plt.figure(figsize=(6, 4))
    logger.info("Academic paper (single column): figsize=(6, 4)")
    plt.close(fig)

    # Academic paper (double column)
    fig = plt.figure(figsize=(12, 4))
    logger.info("Academic paper (double column): figsize=(12, 4)")
    plt.close(fig)

    # Dashboard or report
    fig = plt.figure(figsize=(14, 10))
    logger.info("Dashboard or report: figsize=(14, 10)")
    plt.close(fig)

    # Social media (square)
    fig = plt.figure(figsize=(8, 8))
    logger.info("Social media (square): figsize=(8, 8)")
    plt.close(fig)


if __name__ == "__main__":
    main()
