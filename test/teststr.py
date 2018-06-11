import sys
sys.path.append('..')
from lazy import *
from pprint import*
from random import *




s ="""Meantime, Horwath is criticizing Wynne for what she describes as “mud-slinging” throughout the campaign.
"""


ls = strsep2list(s," ")
pprint(ls)

pprint(max([len(v) for v in ls]))
pprint(strsep2maxlen(s," "))


#d = inilist(8,'\\n')
#k='\\n'
