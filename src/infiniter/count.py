from .generator import Generator, return_generator


@return_generator
def count():
    n = 0
    while True:
        yield n
        n += 1


for i in count():
    print(i)
