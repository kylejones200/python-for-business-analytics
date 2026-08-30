"""

This script demonstrates best practices for avoiding 3D visualizations.
Readers learn that 2D visualizations with good labeling are often clearer than 3D charts.
"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Demonstrate visualization best practices."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # DON'T DO THIS:
    # ax.bar3d(...)  # Avoid 3D bars
    # from mpl_toolkits.mplot3d import Axes3D  # Usually unnecessary

    # INSTEAD: Use 2D with good labeling
    # Tufte: "Excessive decoration and chart junk
    #         can impair graphics just as excessive
    #         imprecision can destroy a textual description."

    logger.info("Best practice: Prefer 2D visualizations with clear labeling over 3D charts.")
    logger.info("3D charts often obscure data relationships and are harder to interpret.")

if __name__ == "__main__":
    main()
