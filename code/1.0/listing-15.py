"""Demonstrates multiple inheritance in Python.

This script shows how a class can inherit from multiple parent classes,
demonstrating multiple inheritance. Readers learn multiple inheritance syntax
and method resolution order (MRO).

"""
import logging

logger = logging.getLogger(__name__)

class A:
    """First parent class."""
    
    def method_a(self):
        """Method from class A."""
        logger.info("Method A")

class B:
    """Second parent class."""
    
    def method_b(self):
        """Method from class B."""
        logger.info("Method B")

class C(A, B):
    """Child class inheriting from both A and B."""
    pass

def main():
    """Main function demonstrating multiple inheritance."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    c = C()
    c.method_a()  # Output: Method A
    c.method_b()  # Output: Method B

if __name__ == "__main__":
    main()
