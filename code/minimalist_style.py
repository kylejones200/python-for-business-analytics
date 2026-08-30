"""
Minimalist Visualization Configuration for Python for Business Analytics
Author: Kyle Jones

This module provides functions and configurations for creating beautiful,
minimalist visualizations:
- Maximize data-to-ink ratio
- Remove visual clutter
- Use subtle colors and typography
- Emphasize the data, not the decoration
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import patheffects
import numpy as np


def set_minimalist_style():
    """
    Configure matplotlib to use a clean minimalist style.
    
    Call this function at the start of your analysis to apply minimalist
    visualization settings. Returns a dictionary of color values for reference.
    
    Returns:
        dict: Dictionary mapping color names to hex codes:
            - primary: Dark blue-gray for text (#2E3440)
            - secondary: Medium gray (#4C566A)
            - accent: Muted blue accent (#5E81AC)
            - highlight: Muted red for emphasis (#BF616A)
            - success: Muted green (#A3BE8C)
            - grid: Very light gray for grids (#ECEFF4)
            - background: White background (#FFFFFF)
    """
    # Color palette - subtle and professional
    minimalist_colors = {
        "primary": "#2E3440",  # Dark blue-gray for text
        "secondary": "#4C566A",  # Medium gray
        "accent": "#5E81AC",  # Muted blue accent
        "highlight": "#BF616A",  # Muted red for emphasis
        "success": "#A3BE8C",  # Muted green
        "grid": "#ECEFF4",  # Very light gray for grids
        "background": "#FFFFFF",  # White background
    }

    # Set the style parameters
    plt.style.use("seaborn-v0_8-whitegrid")  # Start with clean base

    # Configure default parameters
    mpl.rcParams.update(
        {
            # Figure
            "figure.facecolor": minimalist_colors["background"],
            "figure.edgecolor": "none",
            "figure.figsize": (10, 6),
            "figure.dpi": 100,
            # Axes
            "axes.facecolor": minimalist_colors["background"],
            "axes.edgecolor": minimalist_colors["secondary"],
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.labelcolor": minimalist_colors["primary"],
            "axes.labelsize": 11,
            "axes.labelweight": "normal",
            "axes.titlesize": 13,
            "axes.titleweight": "normal",
            "axes.titlepad": 15,
            "axes.spines.top": False,  # Remove top spine
            "axes.spines.right": False,  # Remove right spine
            # Grid
            "grid.color": minimalist_colors["grid"],
            "grid.linestyle": "-",
            "grid.linewidth": 0.5,
            "grid.alpha": 0.4,
            # Lines
            "lines.linewidth": 1.5,
            "lines.markersize": 6,
            # Fonts
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 10,
            # Legend
            "legend.frameon": False,
            "legend.fontsize": 9,
            "legend.title_fontsize": 10,
            # Ticks
            "xtick.color": minimalist_colors["secondary"],
            "ytick.color": minimalist_colors["secondary"],
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "xtick.direction": "out",
            "ytick.direction": "out",
        }
    )

    return minimalist_colors


def remove_chartjunk(ax):
    """
    Remove unnecessary visual elements (chartjunk) from axes.
    
    Removes top and right spines, lightens remaining spines, minimizes tick marks,
    and adds a subtle y-axis grid to create a cleaner visualization.
    
    Args:
        ax: matplotlib axes object to modify
    """
    # Remove top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Lighten remaining spines
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")

    # Minimize tick marks
    ax.tick_params(axis="both", which="both", length=0)

    # No grid for minimalist style
    ax.set_axisbelow(True)


def minimalist_histogram(
    data,
    ax=None,
    bins=20,
    color="#5E81AC",
    alpha=0.7,
    xlabel="",
    ylabel="Frequency",
    title="",
):
    """
    Create a minimalist histogram

    Args:
        data: array-like data
        ax: matplotlib axes object (optional)
        bins: number of bins
        color: bar color
        alpha: transparency
        xlabel, ylabel, title: labels

    Returns:
        ax: matplotlib axes object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    # Create histogram
    n, bins_edges, patches = ax.hist(
        data, bins=bins, color=color, alpha=alpha, edgecolor="white", linewidth=0.5
    )

    # Apply minimalist styling
    remove_chartjunk(ax)

    # Labels
    ax.set_xlabel(xlabel, fontsize=11, color="#2E3440")
    ax.set_ylabel(ylabel, fontsize=11, color="#2E3440")
    if title:
        ax.set_title(title, fontsize=13, color="#2E3440", pad=15)

    return ax


def minimalist_scatter(
    x,
    y,
    ax=None,
    color="#5E81AC",
    alpha=0.6,
    size=50,
    xlabel="",
    ylabel="",
    title="",
    highlight_points=None,
):
    """
    Create a minimalist scatter plot

    Args:
        x, y: array-like data
        ax: matplotlib axes object (optional)
        color: point color
        alpha: transparency
        size: point size
        xlabel, ylabel, title: labels
        highlight_points: indices of points to highlight

    Returns:
        ax: matplotlib axes object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    # Create scatter plot
    ax.scatter(x, y, c=color, alpha=alpha, s=size, edgecolors="white", linewidth=0.5)

    # Highlight specific points if requested
    if highlight_points is not None:
        ax.scatter(
            x[highlight_points],
            y[highlight_points],
            c="#BF616A",
            alpha=0.8,
            s=size * 1.5,
            edgecolors="white",
            linewidth=1,
            zorder=5,
        )

    # Apply minimalist styling
    remove_chartjunk(ax)

    # Labels
    ax.set_xlabel(xlabel, fontsize=11, color="#2E3440")
    ax.set_ylabel(ylabel, fontsize=11, color="#2E3440")
    if title:
        ax.set_title(title, fontsize=13, color="#2E3440", pad=15)

    return ax


def minimalist_line_plot(
    x,
    y,
    ax=None,
    color="#5E81AC",
    linewidth=2,
    xlabel="",
    ylabel="",
    title="",
    markers=False,
):
    """
    Create a minimalist line plot

    Args:
        x, y: array-like data (or list of arrays for multiple lines)
        ax: matplotlib axes object (optional)
        color: line color (or list of colors)
        linewidth: line width
        xlabel, ylabel, title: labels
        markers: whether to show markers

    Returns:
        ax: matplotlib axes object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    # Handle single or multiple lines
    if isinstance(y, list) and len(y) > 1:
        colors = ["#5E81AC", "#A3BE8C", "#BF616A", "#D08770", "#B48EAD"]
        for i, y_data in enumerate(y):
            marker = "o" if markers else None
            ax.plot(
                x,
                y_data,
                color=colors[i % len(colors)],
                linewidth=linewidth,
                marker=marker,
                markersize=4,
                markeredgewidth=0,
                alpha=0.8,
            )
    else:
        marker = "o" if markers else None
        ax.plot(
            x,
            y,
            color=color,
            linewidth=linewidth,
            marker=marker,
            markersize=4,
            markeredgewidth=0,
            alpha=0.8,
        )

    # Apply minimalist styling
    remove_chartjunk(ax)

    # Labels
    ax.set_xlabel(xlabel, fontsize=11, color="#2E3440")
    ax.set_ylabel(ylabel, fontsize=11, color="#2E3440")
    if title:
        ax.set_title(title, fontsize=13, color="#2E3440", pad=15)

    return ax


def minimalist_bar_chart(
    categories,
    values,
    ax=None,
    color="#5E81AC",
    horizontal=False,
    xlabel="",
    ylabel="",
    title="",
):
    """
    Create a minimalist bar chart

    Args:
        categories: list of category names
        values: list of values
        ax: matplotlib axes object (optional)
        color: bar color
        horizontal: whether to create horizontal bars
        xlabel, ylabel, title: labels

    Returns:
        ax: matplotlib axes object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    # Create bar chart
    if horizontal:
        bars = ax.barh(categories, values, color=color, alpha=0.7, edgecolor="white")
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax.text(
                value,
                i,
                f" {value:.1f}",
                va="center",
                ha="left",
                fontsize=9,
                color="#2E3440",
            )
    else:
        bars = ax.bar(categories, values, color=color, alpha=0.7, edgecolor="white")
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=9,
                color="#2E3440",
            )

    # Apply minimalist styling
    remove_chartjunk(ax)

    # Labels
    ax.set_xlabel(xlabel, fontsize=11, color="#2E3440")
    ax.set_ylabel(ylabel, fontsize=11, color="#2E3440")
    if title:
        ax.set_title(title, fontsize=13, color="#2E3440", pad=15)

    # Rotate x-axis labels if needed
    if not horizontal and len(str(categories[0])) > 8:
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    return ax


def minimalist_boxplot(
    data, labels=None, ax=None, color="#5E81AC", xlabel="", ylabel="", title=""
):
    """
    Create a minimalist box plot

    Args:
        data: list of arrays (one per box)
        labels: list of labels for each box
        ax: matplotlib axes object (optional)
        color: box color
        xlabel, ylabel, title: labels

    Returns:
        ax: matplotlib axes object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    # Create boxplot with minimal styling
    bp = ax.boxplot(
        data,
        tick_labels=labels,
        patch_artist=True,
        boxprops=dict(facecolor=color, alpha=0.3, linewidth=1),
        medianprops=dict(color="#2E3440", linewidth=2),
        whiskerprops=dict(color="#4C566A", linewidth=1),
        capprops=dict(color="#4C566A", linewidth=1),
        flierprops=dict(
            marker="o", markerfacecolor=color, markersize=4, alpha=0.5, linestyle="none"
        ),
    )

    # Apply minimalist styling
    remove_chartjunk(ax)

    # Labels
    ax.set_xlabel(xlabel, fontsize=11, color="#2E3440")
    ax.set_ylabel(ylabel, fontsize=11, color="#2E3440")
    if title:
        ax.set_title(title, fontsize=13, color="#2E3440", pad=15)

    return ax


def add_data_labels(ax, x, y, labels, fontsize=9, color="#2E3440", offset=5):
    """
    Add data labels to points on a plot

    Args:
        ax: matplotlib axes object
        x, y: coordinates
        labels: text labels
        fontsize: label font size
        color: label color
        offset: vertical offset from point
    """
    for xi, yi, label in zip(x, y, labels):
        ax.annotate(
            label,
            (xi, yi),
            xytext=(0, offset),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=fontsize,
            color=color,
        )


# Example color palette for categorical data
MINIMALIST_CATEGORICAL_COLORS = [
    "#5E81AC",  # Muted blue
    "#A3BE8C",  # Muted green
    "#BF616A",  # Muted red
    "#D08770",  # Muted orange
    "#B48EAD",  # Muted purple
    "#88C0D0",  # Light blue
    "#EBCB8B",  # Muted yellow
]


def get_minimalist_colors(n):
    """
    Get n colors from the minimalist categorical palette

    Args:
        n: number of colors needed

    Returns:
        list of color hex codes
    """
    if n <= len(MINIMALIST_CATEGORICAL_COLORS):
        return MINIMALIST_CATEGORICAL_COLORS[:n]
    else:
        # Repeat colors if more are needed
        return (
            MINIMALIST_CATEGORICAL_COLORS
            * ((n // len(MINIMALIST_CATEGORICAL_COLORS)) + 1)
        )[:n]


def main():
    """Demonstrate minimalist style configuration."""
    import logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)
    
    colors = set_minimalist_style()
    logger.info("Minimalist style module loaded successfully.")
    logger.info("Available color palette:")
    for name, hex_code in colors.items():
        logger.info(f"  {name:12s}: {hex_code}")


if __name__ == "__main__":
    main()
