from infiniter import Iter


for i in Iter.count().take(50).pairwise():
    print(i)
