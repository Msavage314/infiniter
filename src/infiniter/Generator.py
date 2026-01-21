class Generator:
    """
    Internal class for handling infinite generators

    All functions return this class.

    """

    def __init__(self, generator):
        self.generator = generator
        self._iterator = None

    def __iter__(self):
        self._iterator = iter(self.generator)

        return self

    def __next__(self):
        if self._iterator is None:
            self._iterator = iter(self.generator)
        return next(self._iterator)


def return_generator(func):
    """makes a function return the custom generator class"""

    def inner(*args, **kwargs):
        return Generator(func(*args, **kwargs))

    return inner
