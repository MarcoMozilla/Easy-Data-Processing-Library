import sys
sys.path.append('..')
from lazy import *
from pprint import*
from random import *

t = Table.read("student")

a = t.select(all,where=lambda x:x["IQ"]>=100,\
             name='',IQ="",\
             grade=lambda x:int(x["grade"])).orderby("grade",True)

b =t.groupby("IQ").select(IQ="IQ",\
                          num=lambda x : len(x),\
                          sumgrade=lambda x: sum(x["grade"]) \
                          )

c =t.\
    groupby("IQ").\
    select(where =\
            lambda x: x["sumgrade"]>100,\
            IQ="IQ",\
            num=lambda x : len(x),\
            sumgrade=lambda x: sum(x["grade"]) \
            )

