"""

This script demonstrates displaying a color palette for visualization reference.
Readers learn about color choices and how to access predefined color palettes.
"""
import logging
import os
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import minimalist_style
from minimalist_style import set_minimalist_style
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def main():
    """Display minimalist color palette."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module

    # Set style
    colors = set_minimalist_style()

    # Display the color palette
    fig, ax = plt.subplots(figsize=(10, 3))

    # Show each color as a bar
    for i, (name, hex_code) in enumerate(colors.items()):
        ax.barh(i, 1, color=hex_code, height=0.8)
        ax.text(
            0.5,
            i,
            f"{name}: {hex_code}",
            ha="center",
            va="center",
            fontsize=11,
            color="white",
            fontweight="bold",
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, len(colors) - 0.5)
    ax.axis("off")
    ax.set_title("Minimalist Color Palette", fontsize=13, pad=10)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_color_palette.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_color_palette.png'}")

if __name__ == "__main__":
    main()
