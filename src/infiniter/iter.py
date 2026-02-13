import itertools
import typing
import functools


class SupportsRichComparison(typing.Protocol):
    def __lt__(self, other: typing.Any) -> bool: ...
    def __gt__(self, other: typing.Any) -> bool: ...


class SupportsSum(typing.Protocol):
    def __add__(self, other: typing.Any) -> typing.Any: ...
    def __radd__(self, other: typing.Any) -> typing.Any: ...


class InfiniteIteratorError(Exception):
    """Raised when an operation cannot be run on a infinite iterator"""

    pass


def requires_finite(error_message: str | None = None):
    """Decorator for methods that do not work on iterators of infinite size/unbounded"""

    def decorator(func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._infinite:
                method_name = func.__name__
                msg = error_message or (
                    f"Cannot call {method_name}() on infinite iterator\nUse .take(n).{method_name}() first to limit the iterator"
                )
                raise InfiniteIteratorError(msg)

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class Iter[T]:
    """
    rust like iterator wrapper.

    Provides method chaining, mathematical sequences and infinite operations

    Provides operator overloads for common operations, even for infinite iterators


    """

    def __init__(self, iterable: typing.Iterable[T], infinite: bool = False):
        self._iter = iter(iterable)
        self._infinite = infinite

    def __iter__(self):
        return self._iter

    def __add__(self, other) -> Iter[T]:
        if isinstance(other, Iter):
            return self.zip(other).map(lambda pair: pair[0] + pair[1])
        else:
            return self.map(lambda x: x + other)

    def __sub__(self, other) -> Iter[T]:
        if isinstance(other, Iter):
            return self.zip(other).map(lambda pair: pair[0] - pair[1])
        else:
            return self.map(lambda x: x - other)

    def __mul__(self, other) -> Iter[T]:
        if isinstance(other, Iter):
            return self.zip(other).map(lambda pair: pair[0] * pair[1])
        else:
            return self.map(lambda x: x * other)

    def __truediv__(self, other) -> Iter[T]:
        if isinstance(other, Iter):
            return self.zip(other).map(lambda pair: pair[0] / pair[1])
        else:
            return self.map(lambda x: x / other)

    def __next__(self) -> T:
        return next(self._iter)

    def __getitem__(self, index) -> T | None:
        for i in self.enumerate():
            if i[0] == index:
                return i[1]

    def __str__(self) -> str:
        text = ""
        for i in self.enumerate():
            text += str(i[0]).ljust(3)
            text += "|  "
            text += str(i[1])
            text += "\n"
            if i[0] >= 10:
                text += "..."
                break
        return text

    def __len__(self) -> int:
        if self._infinite:
            return -1
        else:
            total = 0
            for i in self.enumerate():
                total = i[0]
            return total

    def len(self) -> int:
        return self.__len__()

    def map[U](self, func: typing.Callable[[T], U]) -> Iter[U]:
        """Map each element through a function"""

        return Iter(map(func, self._iter))

    def filter(self, predicate: typing.Callable[[T], bool]) -> Iter[T]:
        """Filter elements using a predicate"""
        return Iter(filter(predicate, self._iter))

    def filter_map[U](self, func: typing.Callable[[T], U | None]) -> Iter[U]:
        """Filter and map in one step."""

        def gen():
            for item in self._iter:
                result = func(item)
                if result is not None:
                    yield result

        return Iter(gen())

    def enumerate(self, start: int = 0) -> Iter[tuple[int, T]]:
        """Return a list of tuples of elements with indices"""
        return Iter(enumerate(self._iter, start))

    def chain(self, *iterables: typing.Iterable) -> Iter:
        """Returns a new iterator with the other items added"""

        def gen():
            for i in self:
                yield i
            for i in iterables:
                for j in i:
                    yield j

        return Iter(gen())

    def zip(self, *iterables: typing.Iterable) -> Iter[tuple]:
        """Zip with other iterables"""
        return Iter(zip(self._iter, *iterables))

    def take(self, items: int) -> Iter[T]:
        """Return a new iterable from the first `items` items from self"""

        def gen():
            for i in self.enumerate():
                if i[0] >= items:
                    break
                else:
                    yield i[1]

        return Iter(gen())

    def take_while(self, predicate: typing.Callable[[T], bool]) -> Iter[T]:
        def gen():
            for i in self:
                if not predicate(i):
                    break
                else:
                    yield i

        return Iter(gen())

    @requires_finite()
    def sum(self: Iter[SupportsSum]) -> int:
        return sum(self._iter)

    @requires_finite()
    def sort(
        self: Iter[SupportsRichComparison], key: None = None, reverse: bool = False
    ) -> Iter:
        """Returns a new iterator sorted"""
        return Iter(sorted(self, key=key, reverse=reverse))

    @requires_finite()
    def collect(self) -> list[T]:
        return list(self)

    @staticmethod
    def range(*args) -> Iter[int]:
        """Create an Iter from a range"""
        return Iter(range(*args))

    @staticmethod
    def count(start: int = 0, step: int = 1) -> Iter[int]:
        return Iter(itertools.count(start, step), infinite=True)

    @staticmethod
    def cycle(iterable: typing.Iterable[T]) -> Iter[T]:
        """Create an infinite iterator that cycles through the given iterable forever"""
        return Iter(itertools.cycle(iterable), infinite=True)

    @staticmethod
    def repeat(value: T, times: int | None = None) -> Iter[T]:
        if times:
            return Iter(itertools.repeat(value, times))
        else:
            return Iter(itertools.repeat(value), infinite=True)

    @staticmethod
    def square(start: int = 0) -> Iter[int]:
        return Iter(Iter.count(start).map(lambda x: x**2), infinite=True)

    @staticmethod
    def fibonacci(a: int = 1, b: int = 1) -> Iter[int]:
        def gen():
            nonlocal a
            nonlocal b
            while True:
                yield a
                a, b = b, a + b

        return Iter(gen(), infinite=True)

    @staticmethod
    def triangle_numbers() -> Iter[int]:
        """Returns infinite iterator over all triangle numbers"""

        def gen():
            n = 1
            total = 1
            while True:
                yield total
                n += 1
                total += n

        return Iter(gen(), infinite=True)

    @staticmethod
    def primes() -> Iter[int]:
        """Prime numbers"""

        def gen():
            yield 2
            primes = [2]
            candidate = 3
            while True:
                is_prime = True
                for p in primes:
                    if p * p > candidate:
                        break

                    if candidate % p == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(candidate)
                    yield candidate
                candidate += 2

        return Iter(gen(), infinite=True)
