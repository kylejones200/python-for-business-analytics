"""Abstract base classes and polymorphism via NotImplementedError.
Demonstrates abstract base classes and polymorphism with NotImplementedError.

This script shows how to create abstract base classes that enforce method
implementation in subclasses. Readers learn abstract methods, polymorphism,
and the NotImplementedError exception.

"""

import logging

logger = logging.getLogger(__name__)


class Animal:
    """Abstract base class for animals."""

    def speak(self):
        """Abstract method that must be implemented by subclasses.

        Raises:
            NotImplementedError: If not overridden by subclass.
        """
        raise NotImplementedError("Subclasses must implement speak().")


class Dog(Animal):
    """Dog class implementing Animal interface."""

    def speak(self):
        """Return dog's sound."""
        return "Woof!"


class Cat(Animal):
    """Cat class implementing Animal interface."""

    def speak(self):
        """Return cat's sound."""
        return "Meow!"


class Duck(Animal):
    """Duck class implementing Animal interface."""

    def speak(self):
        """Return duck's sound."""
        return "Quack!"


def animal_sound(animal):
    """Get the sound an animal makes.

    Args:
        animal: An Animal instance.

    Returns:
        The sound the animal makes.
    """
    return animal.speak()


def main():
    """Main function demonstrating polymorphism."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    dog = Dog()
    cat = Cat()
    duck = Duck()

    logger.info(animal_sound(dog))  # Output: Woof!
    logger.info(animal_sound(cat))  # Output: Meow!
    logger.info(animal_sound(duck))  # Output: Quack!


if __name__ == "__main__":
    main()
