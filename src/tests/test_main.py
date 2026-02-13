from infiniter import Iter


for i in Iter([1, 2, 3]).chain([1, 3, 4]):
    print(i)
