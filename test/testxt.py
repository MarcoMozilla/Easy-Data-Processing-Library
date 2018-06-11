import sys
import os
sys.path.append('..')
from lazy import *
from pprint import*
#######################
v =Table.read("s1")



def look(s):
    s="start notepad.exe "+s+".csv"
    #print(s)
    os.system(s)
    return 
    

look("s2")
