def newlist(n,s):
    return eval("["+",".join(s*n)+"]")
        
def pdict(d):
    ident = "   "
    for key in d:
        print(str(key)+":",end="")
        if isinstance(d[key],Table):
            print("\n"+ident+str(d[key]).replace("\n","\n"+ident))
        else:
            print(d[key])


def _destripC(s, n):
    dis=n-len(s)
    front = dis//2
    back = dis-front
    space = " "
    return front*space + s +back* space

def _destripL(s,n):
    return s+" "*(n-len(s))

def slist(s):
    s = s.split(",")
    return [v.strip() for v in s]

def isnum(s):
    d={"1","2","3","4","5","6","7","8","9","0","."}
    for i in range(len(s)):
        if s[i] not in d:
            return False
    return True

def valueof(s):
    if s =="" or s == "None":
        return None
    if isnum(s):
        return eval(s)
    else:
        return s


def decomp1(s):
    l = s.split("=")
    for i in range(len(l)):
        l[i] = l[i].split(",")
        for j in range(len(l[i])):
            l[i][j]= l[i][j].strip()
    return l

def decomp2(s):
    l = s.split(",")
    for i in range(len(l)):
        l[i] = l[i].split("=")
        for j in range(len(l[i])):
            l[i][j]= l[i][j].strip()
    t1 =[]
    t2=[]
    for v in l:
        t1.append(v[0])
        t2.append(v[1])
    return [t1,t2]

def decomp(s):
    if s.count("=")== 1:
        return decomp1(s)
    else:
        return decomp2(s)

def getlenmap(table):
    result = newlist(len(table[0]),"0")
    for v in table:
        result = [max(result[i],len(str(v[i]))) for i in range(len(v))]
    return result

    
    

###############################################################



class Table:
    coding = "utf-8"

    def __init__(self, table=None,name=None):
        self.index = 0
        self.name = name
        self.colmap ={}
        "need to do!"
        #colmap should be used in saving!!!, and repr and str!!!
        self.rowmap = {}
        if table is None:
            self.table = []
            self.lenmap = []
        elif isinstance(table,list):
            self.table = table
            self.lenmap = getlenmap(table)
            #set colmap
            top = table[0]
            for i in range(len(top)):
                self.colmap[top[i]]=i
            #set rowmap
            "need to do!"
            self.rowmap = {}
        else:
            raise Exception("table should be 2D-list")

    def __next__(self):
        if self.index == len(self.table)-2:
            raise StopIteration
        self.index = self.index + 1
        return self.table[self.index]

    def __iter__(self):
        return self

    spacing = _destripC

    def shift():
        if Table.spacing == _destripC:
            Table.spacing = _destripL
        elif Table.spacing == _destripL:
            Table.spacing = _destripC
    
        
    def _check(self, a):
        return a in self.colmap

    def _checklist(self, lst):
        l=[]
        result = True
        for v in lst:
            if v not in self.colmap:
                result =False
                l.append(v)
        if not result:
            raise Exception("No Attribute(s): {}".format(",".join(l)))
        return result




    def row2str(self,v):
        return "|".join([Table.spacing(str(v[i]), self.lenmap[i]) for i in range(len(v))])+"\n"

    def __str__(self):
        # using show to print line one by one
        # this should be a summerized string
        s =""
        for v in self.table:
            s += self.row2str(v)
        s+= str(len(self.table)-1)+" row(s)"
        return s

    def p(self):
        for v in self.table:
            print(self.row2str(v),end="")
        print(str(len(self.table)-1)+" row(s)",end="")
        

    def __repr__(self):
        return self.row2str(self.row(0)) + str(len(self.table)-1)+" row(s)"
        
    
    def get(self,index, name):
        return self.table[index][self.colmap[name]]

    def row(self, index):
        return self.table[index]

    def col(self, name):
        return [self.row(i)[self.colmap[name]] for i in range(1,len(self.table))]

    def read(name):
        result = Table(name = name)
        fname = name+".csv"
        file = open(fname,"r",encoding=Table.coding)
        line=file.readline().strip()
        A = slist(line)
        result.lenmap = [len(v) for v in A]
        for i in range(len(A)):
            result.colmap[A[i]] = i
        while line!="":
            sub = slist(line)
            result.lenmap = [max(result.lenmap[i],len(sub[i])) for i in range(len(sub))]
            nsub = [valueof(v) for v in sub]
            result.table.append(nsub)
            line = file.readline().strip()
        file.close()
        print("READ <{}> FROM {}......".format(result.name, fname))
        return result

    def save(self, name =None):
        # ask for ensure!!!
        if self.name is None and name is None:
            raise Exception("give a name for the table to save")
        elif self.name is None and isinstance(name,str):
            self.name = name
        fname = self.name+".csv"
        file = open(fname,"w",encoding=Table.coding)
        for row in self.table:
            line = ",".join([str(v) for v in row])+"\n"
            file.write(line)
        file.close()
        print("SAVE <{}> TO {}......".format(self.name, fname))

    def apply(self,name, f):
        l = []
        for i in range(1,len(self.table)):
            if f(self.get(i, name)):
                l.append(self.table[i])
        return Table(l)

    def select(self, s):
        # using string to input all fix!!!
        l = slist(s)
        result = [[]]
        for v in l:
            if v is None:
                pass
            elif not v in self.colmap:
                print("No Attribute {} Auto Pass".format(v))
            else:
                result[0].append(v)
        for i in range(1,len(self.table)):
            sub = [self.get(i, key) for key in result[0]]
            result.append(sub)
        print("SELECT {} from <{}>......".format(",".join(result[0]), self.name))
        return Table(result)

    def rename(self, s):
        s = decomp(s)
        self._checklist(s[0])
        for i in range(len(s[0])):
            self.colmap[s[1][i]] = self.colmap[s[0][i]]
            del self.colmap[s[0][i]]
            self.table[0][self.colmap[s[1][i]]]=s[1][i]
            self.lenmap[self.colmap[s[1][i]]] = max(self.lenmap[self.colmap[s[1][i]]],len(s[1][i]))
            print("RENAME {} TO {}......".format(s[0][i], s[1][i]))

    def delete(self,mod= None ):
        fname =".csv"
        if isinstance(self.name, str):
            fname = self.name+fname
        else:
            raise Exception("Table do not have a name to delete")
        if mod != "shut up" :
            v = input("Are you sure to delete {}.csv ? Enter y for delete".format(self.name))
            if v != "y":
                print("DELETE CANCELED......")
                return 
        if os.path.isfile(fname):
            os.remove(fname)
        else:   
            raise Exception("NO {} FILE" % fname)

        
    def _join_on(self, other, on):
        array = decomp(on)
        A1 = array[0]
        A2 = array[1]
        B = []
        C =[]
        for v1 in A1:
            if not self._check(v1):
                raise Exception("{} has no attribute {}".format(self.name, v1))
        for v2 in A2:
            if not other._check(v2):
                raise Exception("{} has no attribute {}".format(other.name, v2))
        for key1 in self.colmap:
            if key1 not in A1:
                B.append(key1)
        for key2 in other.colmap:
            if key2 not in A2:
                C.append(key2)
                
        rd={}
        result = [A1.copy()]
        result[0].extend(B)
        result[0].extend(C)
        for i in range(1,len(self.table)):
            key = [self.get(i,name) for name in A1]
            key = tuple(key)
            value = [self.get(i,name) for name in B]
            if key not in rd:
                rd[key] = [value]
            else:
                rd[key].append(value)
        for i in range(1,len(other.table)):
            key = [other.get(i,name) for name in A2]
            key =tuple(key)
            value = [other.get(i,name) for name in C]
            if key in rd:
                for array in rd[key]:
                    sub = list(key)
                    sub.extend(array.copy())
                    sub.extend(value.copy())
                    result.append(sub)
        print("JOIN <{}>, <{}> ON {}......SUCCESS".format(self.name, other.name, on))
        return Table(result)
        #bug issues switch order result change dictionary value should be list of list
        
    
        
    def _join(self, other):
        newd = {}
        for key in self.colmap:
            newd[key] = 1
        for key in other.colmap:
            if key in newd:
                newd[key] = 0
            else:
                newd[key] = -1
        A = []
        B = []
        C = []
        for key in newd:
            if newd[key] == 0:
                A.append(key)
            elif newd[key] == 1:
                B.append(key)
            elif newd[key] == -1:
                C.append(key)
        
        rd={}
        result = [A.copy()]
        result[0].extend(B)
        result[0].extend(C)
        for i in range(1,len(self.table)):
            key = [self.get(i,name) for name in A]
            key = tuple(key)
            value = [self.get(i,name) for name in B]
            if key not in rd:
                rd[key] = [value]
            else:
                rd[key].append(value)
        for i in range(1,len(other.table)):
            key = [other.get(i,name) for name in A]
            key =tuple(key)
            value = [other.get(i,name) for name in C]
            if key in rd:
                for array in rd[key]:
                    sub = list(key)
                    sub.extend(array.copy())
                    sub.extend(value.copy())
                    result.append(sub)
        print("JOIN <{}>, <{}> ON {}......SUCCESS".format(self.name, other.name, ",".join(A)))
        return Table(result)

    def join(self,other, on = None):
        if on is None:
            return self._join(other)
        elif isinstance(on, str):
            return self._join_on(other, on)
        
    def orderby(self,s):
        s = slist(s)
        for v in s:
            if not self._check(v):
                raise Exception("no attribute {} in {}".format(v,self.name))
        else:
            array =[]
            for i in range(1,len(self.table)):
                array.append([[self.get(i,v) for v in s],i])
            array.sort()
            result =[self.table[0].copy()]
            for v in array:
                result.append(self.table[v[1]].copy())
            return Table(result)
        pass

    def setlib():
        s="""
try:
    import matplotlib.pyplot as plot
    global plt
    plt = plot
except Exception:
    print("can not import matplotlib!")
try:
    from mpl_interaction import PanAndZoom
    global PAZ
    PAZ = PanAndZoom
except:
    print("please download mpl_interaction.py")
"""
        return exec(s,globals(),locals())

    def addrow(self,array):
        if (len(array)==len(self.table[0])):
            self.table.append(array.copy())
            self.lenmap=[max(self.lenmap[i],len(str(array[i]))) for i in range(len(array))]
        else:
            raise Exception("length not match")
        
    def addcol(self,name,array):
        name = name.strip()
        if name not in self.colmap:
            try:
                n = len(self.table[0])
                self.table[0].append(name)
            except:
                n =0
                self.table.append([name])
            self.colmap[name]= n
            self.lenmap.append(len(str(name)))
                
            for i in range(len(array)):
                v = array[i]
                if n==0:
                    self.table.append([v])
                else:
                    self.table[i+1].append(v)
                #print(self.lenmap,n,str(v))
                self.lenmap[n] = max(self.lenmap[n],len(str(v)))
                

            
    def bar(self,label,value):
        Table.setlib()
        self.orderby(label)
        fig,ax = plt.subplots()
        ax.bar([str(v) for v in self.col(label)],self.col(value))
        plt.xlabel(label)
        plt.ylabel(value)
        pan_zoom = PAZ(fig)
        plt.show()



    def pie(self,label,value):
        Table.setlib()
        fig,ax = plt.subplots()
        ax.pie(self.col(value),labels=self.col(label), autopct='%1.1f%%')
        pan_zoom = PAZ(fig)    
        plt.show()

    def hist(self,value,low,up,num):
        Table.setlib()
        fig,ax = plt.subplots()
        amount = up-low
        block = amount/num
        bins = [low+i*block for i in range(num+2)]
        ax.hist(self.col(value),bins,facecolor='green',edgecolor = "yellowgreen")
        plt.xlabel(value)
        plt.ylabel("number")
        pan_zoom = PAZ(fig)
        plt.show()

    def plot(self,x,y,line="."):
        #add polar coord
        #add multiple and lines
        #add spline
        Table.setlib()
        fig,ax = plt.subplots()  
        ax.plot(self.col(x),self.col(y))
        plt.xlabel(x)
        plt.ylabel(y)
        pan_zoom = PAZ(fig)
        plt.show()

    def radar(self):
        #multiple in one graph
        pass

    def polar_radar(self):
        pass

    def hist2d(self):
        pass

    def bar2d(self):
        pass

    def scatter(self):
        pass

    def classify(self):
        #classify the value
        pass
    
    def groupby(self,s):
        #group table by attributes in s
        #form a subtable in groupby dictionary
        pass 


from random import *


def rand():
    return random()*100

k =1
g=5
f= 100


"""
ln = [
    ["name","grade","IQ","color"],
    ["moka",round(random()*k,g),10*f,"grey"],
    ["sasa",round(random()*k,g),20*f,"pink"],
    ["kadi",round(random()*k,g),30*f,"red"],
    ["maki",round(random()*k,g),40*f,"red"],
    ["xido",round(random()*k,g),50*f,"red"],
    ["wade",round(random()*k,g),60*f,"red"],
    ["cida",round(random()*k,g),100*f,"red"],
    ]


for i in range(100):
    ln.append(["cida",round(random()*k,g),int(random()*10)*f,"red"])

for i in range(20):
    ln.append(["cida",round(random()*k,g),1000,"red"])
"""
"""
ln = Table()

ln.addcol("name",["A","B","C","D","E","F","G","H"])
#print(ln)
ln.addcol("grade",[10,20,30,40,50,60,70,80])

print(ln)

"""
