import sys
sys.path.append('..')
from lazy import *
from pprint import*
#######################
from lazy.utility import*

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

Table.coding = "gb18030"
castmap = [strof,strof]

print("使用castmap读取 & 不setlenmap")
v =Table.read("中英字典",castmap,fullprint=False)


print("使用智能读取 & setlenmap")
k=Table.read("中英字典")



#v.setkey("name")




#overall bugs checking！table access
# rename and format variable function name
# fix bug at printi and strsep2list

