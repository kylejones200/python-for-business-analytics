"""Demonstrates parsing JSON strings into Python dictionaries.

This script shows how to deserialize JSON strings to Python dictionaries
using json.loads(). Readers learn JSON parsing and converting JSON data
to Python objects.

"""
import json
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating JSON parsing."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # JSON string
    json_data = '{"name": "Alice", "age": 25, "city": "London"}'

    # Parse JSON string to Python dictionary
    parsed_data = json.loads(json_data)

    logger.info(f"Name: {parsed_data['name']}")
    logger.info(f"Age: {parsed_data['age']}")
    logger.info(f"City: {parsed_data['city']}")

    # Output:
    # Name: Alice
    # Age: 25
    # City: London

if __name__ == "__main__":
    main()
