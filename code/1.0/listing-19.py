"""Demonstrates duck typing and polymorphism through common method interfaces.

This script shows how different classes can be used interchangeably if they
implement the same method interface. Readers learn duck typing and how Python's
polymorphism works through method interfaces rather than inheritance.

"""
import logging

logger = logging.getLogger(__name__)

class Rectangle:
    """Represents a rectangle."""
    
    def __init__(self, width, height):
        """Initialize rectangle dimensions.
        
        Args:
            width: Rectangle width.
            height: Rectangle height.
        """
        self.width = width
        self.height = height

    def calculate_area(self):
        """Calculate rectangle area.
        
        Returns:
            The area of the rectangle.
        """
        return self.width * self.height

class Circle:
    """Represents a circle."""
    
    def __init__(self, radius):
        """Initialize circle radius.
        
        Args:
            radius: Circle radius.
        """
        self.radius = radius

    def calculate_area(self):
        """Calculate circle area.
        
        Returns:
            The area of the circle.
        """
        return 3.14 * self.radius**2

def area(shape):
    """Calculate area of any shape with calculate_area method.
    
    Args:
        shape: An object with a calculate_area() method.
    
    Returns:
        The area of the shape.
    """
    return shape.calculate_area()

def main():
    """Main function demonstrating duck typing."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    rectangle = Rectangle(5, 3)
    circle = Circle(2)

    logger.info(area(rectangle))  # Output: 15
    logger.info(area(circle))  # Output: 12.56

if __name__ == "__main__":
    main()
