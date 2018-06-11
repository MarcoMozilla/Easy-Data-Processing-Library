import sys
sys.path.append('..')
from lazy import *
from pprint import*
from random import *




t = Table.read("studentstr")



t.groupby("IQ,color")
