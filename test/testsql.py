import sys
sys.path.append('..')
from lazy import *
from pprint import*
from random import *




t = Table.read("studentstr")



#t.orderby(lambda x:int(x[1]*10)%10)


#p= [[(v,),(v*2,)] for v in range(1,8)]
#t.lenmap[4]=20

#

g = t.select(all,where=lambda x:x["IQ"]>=100,name='',IQ="",grade=lambda x:int(x["grade"]))



"""
k =t.groupby("IQ").select(IQ="IQ",\
                          num=lambda x : len(x),\
                          sumgrade=lambda x: sum(x["grade"]) \
                          )


g =t.\
    groupby("IQ").\
    select(where =\
            lambda x: x["sumgrade"]>100,\
            IQ="IQ",\
            num=lambda x : len(x),\
            sumgrade=lambda x: sum(x["grade"]) \
            )


"""
