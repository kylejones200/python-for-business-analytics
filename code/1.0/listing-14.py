"""Demonstrates class inheritance and method overriding.

This script introduces inheritance, showing how child classes inherit from
parent classes and can override parent methods. Readers learn inheritance
syntax and polymorphism concepts.

"""
import logging

logger = logging.getLogger(__name__)

class Animal:
    """Base class representing an animal."""
    
    def speak(self):
        """Make the animal speak."""
        logger.info("Animal speaks")

class Dog(Animal):
    """Dog class that inherits from Animal."""
    
    def speak(self):
        """Override parent method to make dog bark."""
        logger.info("Dog barks")

def main():
    """Main function demonstrating inheritance."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    dog = Dog()
    dog.speak()  # Output: Dog barks

if __name__ == "__main__":
    main()
