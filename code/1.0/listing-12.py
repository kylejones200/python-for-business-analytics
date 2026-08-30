"""Demonstrates class definition and object instantiation.

This script introduces object-oriented programming with class definitions,
constructors (__init__), and object creation. Readers learn class syntax,
instance attributes, and object instantiation.

"""
import logging

logger = logging.getLogger(__name__)

class Person:
    """Represents a person with name and age attributes."""
    
    def __init__(self, name, age):
        """Initialize a Person instance.
        
        Args:
            name: The person's name.
            age: The person's age.
        """
        self.name = name
        self.age = age

def main():
    """Main function demonstrating class usage."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    person1 = Person("John", 25)
    person2 = Person("Alice", 30)
    logger.info(person1.name)  # Output: John
    logger.info(person2.age)  # Output: 30

if __name__ == "__main__":
    main()
