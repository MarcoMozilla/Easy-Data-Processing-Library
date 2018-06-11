import sys
sys.path.append('..')
from lazy import *
from pprint import*
Table.coding = "gb18030"
v =Table.read("中英字典")
v.setkey("word")
def find(s):
    i = v.keymap.map[(s,)]
    out = v[i]["translation"]
    out= out.replace("\\n","\n")
    print(out)
    #return out


find("apple")
find("some")
find("people")
