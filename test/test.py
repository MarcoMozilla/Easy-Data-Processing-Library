import sys
sys.path.append('..')
from lazy import *
from pprint import*
#######################

"""
ascii
utf-8          万国语
utf-16         万国语
big5           繁体中文
big5hkscs      繁体中文
gb2312         简体中文
gbk            繁简混合
gb18030        繁简混合
"""

Table.coding = "utf-8"
castmap = [strof,strof,strof,strof]

print("使用castmap读取 & 不setlenmap")
v =Table.read("ecd",castmap,fullprint=False)


dlen={}
v.setkey("word")


for index in range(1,len(v)):
    length = len(v[index][0])
    if length in dlen:
        dlen[length].append(index)
    else:
        dlen[length]=[index]

#v["fabless"]
v[97][0]="fabless"

s = list(dlen.keys())
s.sort()

for c in s:
    if c in dlen:
        print("length = {}, num ={}".format(c,len(dlen[c])))
    else:
        pass

for c in s:
    if c > 50:
        print("c=",c)
        print("dlenp[c]=",dlen[c])
        for index in dlen[c]:
            print("  ",v[index])
        print("========")
    


