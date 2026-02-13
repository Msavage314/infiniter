from infiniter import Iter


for i in Iter([1, 2, 3, 4, 5, 6, 7, 8, 9]).cumulative_average().take(50):
    print(i)
