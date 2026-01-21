import pytest
from infiniter import generator


def test_generator():
    def generate():
        for i in range(10):
            yield i

    a = generator.Generator(generate())
    b = generate()
    for i in range(10):
        assert next(a) == next(b)
