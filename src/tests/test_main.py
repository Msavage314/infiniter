from infiniter import Iter


for i in Iter.count().take_while(lambda x: x <= 50):
    print(i)
