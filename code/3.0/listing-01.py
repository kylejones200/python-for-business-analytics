"""Activate the book's shared Matplotlib style."""

import sys
from pathlib import Path

# The helper lives at code/minimalist_style.py and is on the import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import minimalist_style
from minimalist_style import set_minimalist_style

colors = set_minimalist_style()
print("Minimalist style activated")
for name, hex_code in colors.items():
    print(f"{name}: {hex_code}")
