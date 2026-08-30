"""Demonstrates custom iterator implementation using __iter__ and __next__.

This script shows how to create custom iterators by implementing the iterator
protocol. Readers learn __iter__ and __next__ methods, StopIteration
exception, and how Python's for loop uses iterators.

"""

import logging

logger = logging.getLogger(__name__)


class MyIterator:
    """Custom iterator class."""

    def __init__(self, data):
        """Initialize iterator with data.

        Args:
            data: The data to iterate over.
        """
        self.data = data
        self.index = 0

    def __iter__(self):
        """Return the iterator object itself."""
        return self

    def __next__(self):
        """Return the next item in the iteration.

        Raises:
            StopIteration: When all items have been iterated.
        """
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value


def main():
    """Main function demonstrating custom iterators."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    my_list = [1, 2, 3, 4, 5]
    my_iterator = MyIterator(my_list)

    for item in my_iterator:
        logger.info(item)

    # Output:
    # 1
    # 2
    # 3
    # 4
    # 5


if __name__ == "__main__":
    main()
