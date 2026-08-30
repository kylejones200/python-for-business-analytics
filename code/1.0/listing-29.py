"""Demonstrates converting Python dictionaries to JSON strings.

This script shows how to serialize Python dictionaries to JSON format using
json.dumps(). Readers learn JSON serialization and data format conversion.

"""
import json
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating JSON serialization."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Python dictionary
    data = {"name": "John Doe", "age": 30, "city": "New York"}

    # Convert dictionary to JSON string
    json_string = json.dumps(data)

    logger.info(f"JSON string: {json_string}")

    # Output:
    # JSON string: {"name": "John Doe", "age": 30, "city": "New York"}

if __name__ == "__main__":
    main()
