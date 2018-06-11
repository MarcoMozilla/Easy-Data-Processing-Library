import sys
sys.path.append('..')
from lazy import *
from pprint import*
from random import *

#           attributes    num of row
v = Table.init("A,B,C,D",8)

print(v)
# a function for assign
def f(s):
    result =s[0]
    s[0],s[1] = s[1],s[0]+s[1]
    return result

# a function for assign
def g(s):
    ls = "!@#$%"
    s[0] = (s[0]+1) % len(ls)
    return ls[s[0]]

#assign "A" and the last col to be random    
v.apply("A",random)
v.apply(-1,random)

print(v)
#assign 1, 2 col to be the  function f with para [0,1] and g with para [-1]
v.apply(1,f,[0,1])
v.apply(2,g,[-1])

print(v)
def fun(s):
    s=s*100
    s=round(s)
    s-=50
    return s

#apply fun to the last col
v.apply(-1,fun,para = True)

print(v)




