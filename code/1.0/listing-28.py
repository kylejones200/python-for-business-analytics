"""Demonstrates exponential and logarithmic functions from the math module.

This script shows how to calculate exponential and logarithmic values using
the math module. Readers learn exp(), log(), and mathematical function usage.

"""
import logging
import math

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating exponential and logarithmic functions."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Calculate exponential and logarithm
    exp_value = math.exp(2)
    log_value = math.log(10, 2)

    logger.info(f"e^2: {exp_value}")
    logger.info(f"log base 2 of 10: {log_value}")

    # Output:
    # e^2: 7.38905609893065
    # log base 2 of 10: 3.321928094887362

if __name__ == "__main__":
    main()
