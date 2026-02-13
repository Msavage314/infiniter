from infiniter import Iter


for i in Iter.primes().cumulative().take(50):
    print(i)
