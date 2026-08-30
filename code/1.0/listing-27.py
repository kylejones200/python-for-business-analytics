"""Demonstrates trigonometric functions from the math module.

This script shows how to calculate sine and cosine values using the math
module. Readers learn trigonometric functions, radians, and mathematical
computations in Python.

"""
import logging
import math

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating trigonometric functions."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Calculate sine and cosine
    angle = math.pi / 4  # 45 degrees in radians
    sine_value = math.sin(angle)
    cosine_value = math.cos(angle)

    logger.info(f"Sine of 45 degrees: {sine_value}")
    logger.info(f"Cosine of 45 degrees: {cosine_value}")

    # Output:
    # Sine of 45 degrees: 0.7071067811865476
    # Cosine of 45 degrees: 0.7071067811865476

if __name__ == "__main__":
    main()
