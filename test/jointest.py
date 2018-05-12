import sys
sys.path.append('..')
from lazy.table import *
from time import *

#natrual join on=None


v =Table.read("values")

s1 = time()
vv = v@v
s2 = time()
print("use time:",s2 - s1)
print(vv)

l =[9,"i"]


print()

"""
todo
pset
plist
pdict

exchange row
set operations on table
chinese words full length

"""