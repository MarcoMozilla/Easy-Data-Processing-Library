import sys
sys.path.append('..')
from lazy import *
from pprint import*
#######################

v =Table.read("country")

v.setkeymap("name")



k = v[:]
