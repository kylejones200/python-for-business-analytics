"""

This script demonstrates saving figures in multiple formats for different use cases.
Readers learn to export visualizations appropriately for documents, papers, web, and editing software.
"""
import logging
import os
from pathlib import Path
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def main():
    """Demonstrate saving figures in multiple formats."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Create your plot
    fig, ax = plt.subplots(figsize=(10, 6))
    # ... plotting code ...
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3], label="Example")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Example Plot")
    ax.legend()

    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)

    # For documents (Word, PowerPoint, web)
    plt.savefig(
        img_dir / "figure1.png", dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none"
    )
    logger.info(f"Saved high-res PNG to {img_dir / 'figure1.png'}")

    # For academic papers (LaTeX, print)
    plt.savefig(img_dir / "figure1.pdf", bbox_inches="tight", facecolor="white", edgecolor="none")
    logger.info(f"Saved PDF to {img_dir / 'figure1.pdf'}")

    # For editing in Illustrator/Inkscape
    plt.savefig(img_dir / "figure1.svg", bbox_inches="tight", facecolor="white", edgecolor="none")
    logger.info(f"Saved SVG to {img_dir / 'figure1.svg'}")

    # For online use (smaller file size)
    plt.savefig(
        img_dir / "figure1_web.png",
        dpi=150,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
    )
    logger.info(f"Saved web PNG to {img_dir / 'figure1_web.png'}")

if __name__ == "__main__":
    main()
