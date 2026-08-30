"""Demonstrates classes with methods that perform calculations.

This script shows how to define methods within classes that perform operations
on instance attributes. Readers learn instance methods and how to call them
on objects.

"""
import logging

logger = logging.getLogger(__name__)

class Rectangle:
    """Represents a rectangle with width and height."""
    
    def __init__(self, width, height):
        """Initialize a Rectangle instance.
        
        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
        """
        self.width = width
        self.height = height

    def calculate_area(self):
        """Calculate and return the area of the rectangle.
        
        Returns:
            The area (width * height).
        """
        return self.width * self.height

def main():
    """Main function demonstrating class methods."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    rect = Rectangle(5, 3)
    area = rect.calculate_area()
    logger.info(f"The area of the rectangle is: {area}")
    # Output: The area of the rectangle is: 15

if __name__ == "__main__":
    main()
