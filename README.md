# Infiniter - Rust-Inspired Iterators for Python

This library provides a rust-inspired improved iterator system to python

## Features

-  **Rust-like method chaining** - Fluent API similar to Rust's Iterator trait
- **Infinite iterator support** - Safe operations on unbounded sequences
- **Mathematical sequences** - Built-in generators (Fibonacci, primes, triangular numbers, etc.)
- **Operator overloading** - Use `+`, `-`, `*`, `/` on iterators
- **Lazy evaluation** - All operations are lazy until materialization


## Quick Start

```python
from infiniter import Iter

# Basic chaining
result = (Iter.range(1, 20)
          .filter(lambda x: x % 2 == 0)
          .map(lambda x: x ** 2)
          .take(5)
          .collect())
# [4, 16, 36, 64, 100]

# Infinite sequences with operators
squares_of_triangles = Iter.triangle_numbers() ** 2
for val in squares_of_triangles.take(5):
    print(val)
# 1, 9, 36, 100, 225

# Element-wise operations on two iterators
result = (Iter.fibonacci() + Iter.primes()).take(5).collect()
# [3, 4, 7, 10, 16]  (1+2, 1+3, 2+5, 3+7, 5+11)
```

## Creating Iterators

### From Built-ins

```python
# From ranges
Iter.range(1, 10)           # 1, 2, 3, ..., 9
Iter.range(0, 100, 10)      # 0, 10, 20, ..., 90

# From any iterable
Iter([1, 2, 3])
Iter("hello")
Iter({'a': 1, 'b': 2})
```

### Infinite Iterators

```python
# Counting sequences
Iter.count()                # 0, 1, 2, 3, ...
Iter.count(10)              # 10, 11, 12, 13, ...
Iter.count(0, 2)            # 0, 2, 4, 6, ...

# Cycling
Iter.cycle([1, 2, 3])       # 1, 2, 3, 1, 2, 3, ...

# Repeating
Iter.repeat(5)              # 5, 5, 5, 5, ... (infinite)
Iter.repeat(5, 3)           # 5, 5, 5 (finite)
```

### Mathematical Sequences

```python
# Fibonacci sequence
Iter.fibonacci()            # 1, 1, 2, 3, 5, 8, 13, ...
Iter.fibonacci(0, 1)        # 0, 1, 1, 2, 3, 5, 8, ...

# Prime numbers
Iter.primes()               # 2, 3, 5, 7, 11, 13, 17, ...

# Triangular numbers
Iter.triangle_numbers()     # 1, 3, 6, 10, 15, 21, ...

# Perfect squares
Iter.square()               # 0, 1, 4, 9, 16, 25, ...
Iter.square(1)              # 1, 4, 9, 16, 25, ...
```

## Transformations

All transformations are **lazy** - they don't execute until you materialize the iterator.

```python
iter = Iter.range(1, 100)

# Map - transform each element
iter.map(lambda x: x * 2)

# Filter - keep matching elements
iter.filter(lambda x: x % 2 == 0)

# Filter and map combined
iter.filter_map(lambda x: x * 2 if x % 3 == 0 else None)

# Enumerate - add indices
iter.enumerate()            # (0, 1), (1, 2), (2, 3), ...
iter.enumerate(start=10)    # (10, 1), (11, 2), (12, 3), ...

# Zip - combine with other iterables
iter.zip([10, 20, 30])      # (1, 10), (2, 20), (3, 30)
```

## Operator Overloading

### Scalar Operations (Broadcasting)

Apply operations to each element:

```python
# Addition
Iter.range(1, 5) + 10           # 11, 12, 13, 14

# Multiplication
Iter.range(1, 5) * 2            # 2, 4, 6, 8

# Power
Iter.triangle_numbers() ** 2    # 1, 9, 36, 100, 225, ...

# Division
Iter.range(10, 50, 10) / 10     # 1.0, 2.0, 3.0, 4.0

# Subtraction
Iter.range(10, 15) - 5          # 5, 6, 7, 8, 9
```

### Element-wise Operations (Zipping)

Combine two iterators element by element:

```python
# Add corresponding elements
iter1 = Iter.range(1, 5)
iter2 = Iter.range(10, 14)
(iter1 + iter2).collect()       # [11, 13, 15, 17]

# Multiply corresponding elements
(iter1 * iter2).collect()       # [10, 22, 36, 52]

# Complex combinations
fib = Iter.fibonacci()
primes = Iter.primes()
(fib * 2 + primes).take(5).collect()
# [4, 5, 9, 13, 21]  # (1*2+2, 1*2+3, 2*2+5, 3*2+7, 5*2+11)
```

## Slicing & Limiting

```python
# Take first n elements
Iter.count().take(5)            # 0, 1, 2, 3, 4

# Take while condition holds
Iter.count().take_while(lambda x: x < 10)  # 0, 1, 2, ..., 9
```

## Terminal Operations

Terminal operations **consume** the iterator and return a value. 

 **These will raise `InfiniteIteratorError` on infinite iterators:**

```python
# Collect to list
Iter.range(1, 6).collect()      # [1, 2, 3, 4, 5]

# Sort (requires finite iterator)
Iter([3, 1, 4, 1, 5]).sort().collect()
# [1, 1, 3, 4, 5]

Iter(['apple', 'pie', 'a']).sort(key=len).collect()
# ['a', 'pie', 'apple']
```

## Infinite Iterator Safety

The library **prevents accidental infinite loops** by tracking which iterators are infinite.

### Safe Patterns 

```python
# Always use take() with infinite iterators
Iter.fibonacci().take(10).collect()     #  Safe

# take_while terminates naturally
Iter.count().take_while(lambda x: x < 100).collect()  #  Safe

# Zip stops at shortest iterator
Iter.fibonacci().zip(Iter.range(1, 6)).collect()  #  Safe

# Operators preserve safety
(Iter.fibonacci() ** 2).take(5).collect()  #  Safe
```

### Unsafe Patterns 

```python
# These will raise InfiniteIteratorError:
Iter.fibonacci().collect()              #  Error!
Iter.count().sort()                     #  Error!
Iter.primes().collect()                 #  Error!
```

## API Reference

### Creation Methods

| Method | Description |
|--------|-------------|
| `Iter(iterable)` | Wrap any iterable |
| `Iter.range(*args)` | Create from range |
| `Iter.count(start=0, step=1)` | Infinite counting |
| `Iter.cycle(iterable)` | Infinite cycling |
| `Iter.repeat(value, times=None)` | Repeat value |
| `Iter.fibonacci(a=1, b=1)` | Fibonacci sequence |
| `Iter.primes()` | Prime numbers |
| `Iter.triangle_numbers()` | Triangular numbers |
| `Iter.square(start=0)` | Perfect squares |

### Transformation Methods

| Method | Description | Safe for Infinite? |
|--------|-------------|-------------------|
| `map(func)` | Transform elements |  Yes |
| `filter(pred)` | Keep matching |  Yes |
| `filter_map(func)` | Map + filter None |  Yes |
| `enumerate(start=0)` | Add indices |  Yes |
| `zip(*iterables)` | Combine iterables |  Yes* |
| `take(n)` | First n elements |  Yes |
| `take_while(pred)` | Take while true |  Yes |

*Stops at shortest iterator

### Terminal Methods

| Method | Description | Safe for Infinite? |
|--------|-------------|-------------------|
| `collect()` | → list | No |
| `sort(key=None, reverse=False)` | → sorted Iter | No |

### Operators

| Operator | Scalar | Element-wise |
|----------|--------|--------------|
| `+` | Add to each | Zip and add |
| `-` | Subtract from each | Zip and subtract |
| `*` | Multiply each | Zip and multiply |
| `/` | Divide each | Zip and divide |

### Special Methods

| Method | Description |
|--------|-------------|
| `__iter__()` | Use in for loops |
| `__next__()` | Get next element |
| `__getitem__(index)` | Access by index |
| `__str__()` | Pretty print first 10 |

## Design Philosophy

1. **Safety First** - Infinite iterators are clearly marked and unsafe operations are blocked
2. **Lazy Evaluation** - Nothing executes until you call a terminal operation
3. **Chainable** - Methods return new iterators for fluent composition
4. **Pythonic** - Uses Python's protocols and conventions
5. **Type-Safe** - Full type hints for IDE support

## Requirements

- Python 3.12+ (uses new generic syntax `class Iter[T]`)

## License

MIT

## Contributing

Ideas for extensions:
- More mathematical sequences (Catalan, Lucas numbers, etc.)
- More terminal operations (`sum()`, `product()`, `min()`, `max()`)
- Parallel iteration support
- More operators (comparison, bitwise)
- `scan()` for cumulative operations
- `chunk()` and `window()` for grouping

## Examples in Action

```python
# Find the 10th Fibonacci number that's also prime
result = (Iter.fibonacci()
          .filter(lambda f: f in Iter.primes().take(1000).collect())
          .take(10)
          .enumerate()
          .collect())

# Generate powers: 2^1, 3^2, 4^3, 5^4, ...
powers = (Iter.count(2) ** Iter.count(1)).take(10).collect()
# [2, 9, 64, 625, 7776, 117649, 2097152, 43046721, 1000000000, 25937424601]

# Complex mathematical pipeline
result = (
    Iter.triangle_numbers()     # 1, 3, 6, 10, 15, ...
    ** 2                         # 1, 9, 36, 100, 225, ...
    .filter(lambda x: x % 2 == 0) # 36, 100, ...
    .map(lambda x: x // 2)       # 18, 50, ...
    .take(5)
    .collect()
)
```

