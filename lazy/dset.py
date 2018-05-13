"""disjoint set"""
from pprint import*
#嵌套结构print直接用pprint来打印
class Dset:
    #staticvariable
    vmap ={}
    #static 变量用来记录value是否存在，一个value只能存在一次	
    #dict of value: Dset(value)
    #staticvariable
    roots=set()
    # set of values
    # static 用来记录一共有多少个集合 
    #1. 每当一个元素变成root的时候把value加到roots中
    #2. 每当一个元素变成child的时候，从roots中删除	

    def __init__(self, value):
        print("this is init")
        #value检查必须是，str，bool，None，tuple，int， float中的一种（hashable不然不能作为vmap的key）               
        #raise exception
        self.value = value
        self.parent = None
        self.children = []
        self.height = 0
        Dset.vmap[value]=self
        #在这里可能需要加上参数来完成其他功能

    def __new__(cls,v):
        if v in Dset.vmap:
            return Dset.vmap[v]
        else:
            result = super().__new__(cls)
            return result
        

    def union(self,other):
        #print("start find")
        selfroot = self.find()
        otheroot =other.find()
        #print("end find")
        if selfroot.height<otheroot.height:
            otheroot.children.append(selfroot)
            selfroot.parent = otheroot
        else:
            selfroot.children.append(otheroot)
            otheroot.parent = selfroot
            if selfroot.height == otheroot.height:
                selfroot.height+=1
        #加上其他内容以满足delete功能，和 roots


            


    def find(self):
        #print("self:",self)
        #print("self.parent:",self.parent)
        if self.parent is None:
            return self
        else:
            curp = self.parent
            #print("self:",self)
            #print("curp.children:",curp.children)
            curp.children.remove(self)
            while curp.parent is not None:
                curp = curp.parent
            curp.children.append(self)
            self.parent= curp
            return curp
        #加上其他功能以满足该类所有要求

    def __eq__(self,other):
        return self.value == other.value

    def tostring(self):
        #debug用
        s= str(self.value)
        if self.children ==[]:
            return s
        else:
            for child in self.children:
                s+=","+child.tostring()
            return s

    def __repr__(self):
        #debug用
        return "{" + self.tostring()+"}"


    def deunion(self):
	#在set中去除该元素(如果在一个集合中)，元素独立存在于vmap中，track所有指针
        pass
    
    def __del__(self):
	#在set中去除该元素，并从vmap中删除
        pass
    
    def getall(self):
	#return 所有和self同一个set中的其他元素
        pass

    def moveto(self,other):
	#如果self在一个set中，从该set中移走，放到other的set中
        pass

    def deunionall(self):
	#把self所在set中的所有元素全部拆分成单个元素，在vmap中
        pass
    
    def delall(self):
	#把self所在set中所有元素全部删除，并从vmap中删除
        pass
    
    def getsize(self):
        #所在集合元素个数
        pass
    
a= Dset("a")
b = Dset("b")
