class Dset:
	
    vmap ={}

    def __init__(self, value):
        print("this is init")
        self.value = value
        self.parent = None
        self.children = []
        self.height = 0
        Dset.vmap[value]=self
        

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

    def __new__(cls,v):
        if v in Dset.vmap:
            return Dset.vmap[v]
        else:
            result = super().__new__(cls)
            return result
            
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

    def __eq__(self,other):
        return self.value == other.value

    def tostring(self):
        s= str(self.value)
        if self.children ==[]:
            return s
        else:
            for child in self.children:
                s+=","+child.tostring()
            return s

    def __repr__(self):
        return "{" + self.tostring()+"}"




a= Dset("a")
b = Dset("b")




















