import csv
from pprint import *

from .utility import *
from .row import *
from .rows import *



###############################################################

class Table:
    coding = "utf-8"


    def see(self):
        pprint(self.__dict__)
    # ===========================global function setting===================================
    def _destripC(s, n):
        dis = n - len(s)
        front = dis // 2
        back = dis - front
        space = " "
        return front * space + s + back * space

    def _destripL(s, n):
        return s + " " * (n - len(s))

    spacing = _destripC

    def shift():
        if Table.spacing == Table._destripC:
            Table.spacing = Table._destripL
        elif Table.spacing == Table._destripL:
            Table.spacing = Table._destripC

    """ initialize the class """

    def __init__(self, table=None, name=None):
        # index for iterator
        self.imax = -1
        self.imap = []
        self.name = name
        self.table = []
        self.lenmap = []
        self.colmap = {}
        self.searchmap = None
        self.key=None
        self.keymap = None


        if table is None:
            pass
        elif isinstance(table, str):
            self.table.append(slist(table, ","))
            self.setlenmap()
            self.setcolmap()
        elif isinstance(table, list):
            if isinstance(table[0], list):
                for row in table:
                    self.table.append(row)
            else:
                self.table.append(table)

            self.setlenmap()
            # set colmap
            self.setcolmap()
            # set rowmap
            "need to do!"
        else:
            raise Exception("table should be 2D-list")


    def setentry(self,rowindex,colindex,value):
        if self.searchmap is not None:
            oldrow = tuple(self.table[rowindex])
            del self.searchmap[oldrow]
        if self.key is not None and self.keymap is not None:
            oldkey = tuple(self.getlist(rowindex, self.key))
            del self.keymap[oldkey]

        self.table[rowindex][colindex] = value
        self.refreshlenmap(colindex,value)

        if self.searchmap is not None:
            newrow = tuple(self.table[rowindex])
            self.searchmap[newrow] = rowindex
        if self.key is not None and self.keymap is not None:
            newkey = tuple(self.getlist(rowindex, self.key))
            self.keymap[newkey] = rowindex

    def __contains__(self, item):
        """
        the first search take O(n)
        next search take O(1)
        """
        v = tuple(item) if not isinstance(item, int) else (item,)
        # initialie searchmap if not exits
        if self.searchmap is None:
            self.searchmap = {}
            for i in range(1, len(self)+1):
                self.updatesearchmap(i)
        return v in self.searchmap

    def setkeymap(self, s):
        key = slist(s, ',')
        self._checklist(key)
        self.keymap={}
        for i in range(1,len(self)+1):
            #print("i= ",i)
            #print("getlist = ",self.getlist(i,key))
            t = tuple(self.getlist(i, key))
            if t in self.keymap:
                raise Exception("it is not a primary key")
            else:
                self.keymap[t] = i
            #print(self.keymap)
        self.key=key



    def addkeymap(self):
        i = len(self)
        t = tuple(self.getlist(i, self.key))
        if t in self.keymap:
            raise Exception("it is not a primary key")
        else:
            self.keymap[t] = i

    def updatesearchmap(self, index):
        t = tuple(self.table[index])
        if t in self.searchmap:
            self.searchmap[t].append(index)
        else:
            self.searchmap[t] = [index]

    # over all help functions:
    def append(self, row):

        self.table.append(row)
        self.updatelenmap(row)
        if self.searchmap is not None:
            self.updatesearchmap(len(self))
        if self.keymap is not None:
            self.addkeymap()


    # ====================buildin method part====================
    def __len__(self):
        return len(self.table)-1

    def setlenmap(self):
        for i in range(wid(self)):
            self.lenmap.append(max([len(str(v[i])) for v in self.table]))

    def updatelenmap(self, row):
        for i in range(len(self.lenmap)):
            self.lenmap[i] = max(self.lenmap[i], len(str(row[i])))

    def refreshlenmap(self,i, entry):
        self.lenmap[i] = max(self.lenmap[i],len(str(entry)))

    def setcolmap(self):
        head = self.gethead()
        for i in range(wid(self)):
            self.colmap[head[i]] = i

    def __next__(self):
        if self.imap[self.imax] == len(self):
            self.imap.pop()
            self.imax -= 1
            raise StopIteration
        self.imap[self.imax] += 1
        return self.table[self.imap[self.imax]]

    def __iter__(self):
        self.imax += 1
        self.imap.append(0);
        return self

    def _check(self, a):
        return a in self.colmap

    def _checklist(self, lst):
        l = []
        result = True
        for v in lst:
            if v not in self.colmap:
                result = False
                l.append(v)
        if not result:
            raise Exception("No Attribute(s): {}".format(",".join(l)))
        return result

    def getlist(self, i, ls):
        #print("i=",i)
        #print(type(i))
        #print("self.table[i]=",self.table[i])
        #print("self.colmap = ", self.colmap)
        #for v in ls:
            #print("v= ",v)
            #print("self.colmap[v]=",self.colmap[v])
            #print("######")

        return [self.table[i][self.colmap[v]] for v in ls]

    def getsearchmap(self, ls):
        if isinstance(ls, str):
            ls = slist(ls, ",")
        self._checklist(ls)  # check attributes valid
        result = {}
        for i in range(1, len(self)+1):
            t = tuple(self.getlist(i, ls))
            if t in result:
                result[t].append(i)
            else:
                result[t] = [i]
        return result

    def row2str(self, v):
        return "|".join([Table.spacing(str(v[i]), self.lenmap[i]) for i in range(len(v))])

    def head2str(self):
        head = self.gethead()
        if self.key is not None:
            head = [str(v)+"*" if v in self.key else str(v) for v in head]
            self.updatelenmap(head)
        return self.row2str(head)

    def __str__(self):
        s = ""
        s += self.head2str()+'\n'
        for v in self:
            s += self.row2str(v) + "\n"
        s += str(len(self)) + " row(s)"
        return s

    def p(self):
        for v in self.table:
            s = self.row2str(v)
            command = input(s)
            if command == "exit":
                break
        print(str(len(self.table)) + " row(s)", end="")

    def __repr__(self):

        # return self.row2str(self.row(0)) +"\n"+str(len(self.table)-1)+" row(s)"
        return str(self)

    def getcolindex(self, key):
        # for Row and Rows usage
        if isinstance(key, int):
            if key >= 0 and key < len(self):
                return key
            else:
                raise Exception("index out of range")
        elif isinstance(key, str):
            if self._check(key):
                return self.colmap[key]
            else:
                raise Exception("attribute name not exist")
        else:
            raise KeyError("only int or str is supported")

    def getrowindex(self,key):
        if self.key is not None and self.keymap is not None:
            return self.keymap[key]
        else:
            raise Exception("please use setkeymap to set keymap")

    def __getitem__(self, key):
        if isinstance(key, int):
            return Row(self,key)
        elif isinstance(key,str):
            keys =[valueof(v) for v in slist(key,',')]
            #print(keys)
            index = self.getrowindex(tuple(keys))
            return Row(self,index)
        elif isinstance(key,slice):
            #include key.stop when access
            start = 1 if key.start is None else key.start
            stop = len(self) if key.stop is None else key.start
            indices= list(range(start, stop+1))
            return Rows(self,indices)
        elif isinstance(key,tuple) or isinstance(key,list):
            indices = []
            for i in range(len(key)):
                if isinstance(key[i],str):
                    index = self.getrowindex(tuple(key[i]))
                    indices.append(index)
                elif isinstance(key[i],int):
                    indices.append(key[i])
                else:
                    raise Exception("self getitem invalid input")
            return Rows(self, indices)
        else:
            raise Exception("self getitem invalid input")

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def read(name):
        result = []
        fname = name + ".csv"
        file = open(fname, "r", encoding=Table.coding, newline='')
        lines = csv.reader(file, delimiter=',', quotechar='"')
        for row in lines:
            vlist = [valueof(s) for s in row]
            result.append(vlist)
        file.close()
        print("READ <{}> FROM {}".format(name, fname))
        return Table(result, name=name)

    def save(self, name=None):
        # ask for ensure!!!
        if self.name is None and name is None:
            raise Exception("give a name for the table to save")
        elif self.name is None and isinstance(name, str):
            self.name = name
        fname = self.name + ".csv"
        file = open(fname, "w", encoding=Table.coding, newline='')
        lines = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in self.table:
            lines.writerow(row)
        file.close()
        print("SAVE <{}> TO {}".format(self.name, fname))

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
        for i in range(1, len(self)+1):
            sub = [self.get(i, key) for key in result[0]]
            result.append(sub)
        print("SELECT {} from <{}>".format(",".join(result[0]), self.name))
        return Table(result)

    def rename(self, s):
        s = decomp(s)
        self._checklist(s[0])
        for i in range(len(s[0])):
            self.colmap[s[1][i]] = self.colmap[s[0][i]]
            del self.colmap[s[0][i]]
            self.table[0][self.colmap[s[1][i]]] = s[1][i]
            self.lenmap[self.colmap[s[1][i]]] = max(self.lenmap[self.colmap[s[1][i]]], len(s[1][i]))
            print("RENAME {} TO {}".format(s[0][i], s[1][i]))

    def getLMR(self, other):
        rdict = {}
        for key in self.colmap:
            rdict[key] = 0
        for key in other.colmap:
            if key in rdict:
                rdict[key] = 1
            else:
                rdict[key] = 2

        rlist = [[], [], []]
        for key in rdict:
            rlist[rdict[key]].append(key)
        return rlist

    def gethead(self):
        return self.table[0].copy()

    def _join(self, other, on=None, mod="natural"):
        if mod not in {"natural", "left", "right", "full"}:
            raise Exception("invalid mod")
        # check mod valid
        if on is None:
            lmr = self.getLMR(other)
            lmrm = lmr + [lmr[1]]
        else:
            mm = decomp(on)
            self._checklist(mm[0])
            other._checklist(mm[1])
            l = list(set(self.colmap) - set(mm[0]))
            r = list(set(other.colmap) - set(mm[1]))
            lmrm = [l, mm[0], r, mm[1]]
        selfsmap = self.getsearchmap(lmrm[1])
        othersmap = other.getsearchmap(lmrm[3])
        selfset = set(selfsmap)
        otherset = set(othersmap)
        sharedentry = selfset & otherset
        if on is None:
            result = [lmrm[0] + lmrm[1] + lmrm[2]]
        else:
            result = [self.gethead() + other.gethead()]
        for t in sharedentry:
            mid = list(t)
            for i in selfsmap[t]:
                left = self.getlist(i, lmrm[0])
                for j in othersmap[t]:

                    right = other.getlist(j, lmrm[2])
                    if on is None:
                        sub = left + mid + right
                    else:
                        sub = self[i] + other[j]
                    result.append(sub)
        if (mod == "natural"):
            print("<{}> {} JOIN <{}> ".format(self.name, mod.upper(), other.name), end="")
            if on is None:
                print()
            else:
                print("ON {}".format(on.replace(" ", "")))
            return Table(result)
        if (mod == "left" or mod == "full"):
            leftentry = selfset - otherset
            if on is None:
                right = inilist(len(lmrm[2]))
            else:
                right = inilist(len(lmrm[2]) + len(lmrm[3]))
            for t in leftentry:
                mid = list(t)
                for i in selfsmap[t]:
                    left = self.getlist(i, lmrm[0])
                    if on is None:
                        sub = left + mid + right
                    else:
                        sub = self[i] + right
                    result.append(sub)
        if (mod == "right" or mod == "full"):
            rightentry = otherset - selfset
            if on is None:
                left = inilist(len(lmrm[0]))
            else:
                left = inilist(len(lmrm[0]) + len(lmrm[1]))
            for t in rightentry:
                mid = list(t)
                for j in othersmap[t]:
                    right = other.getlist(j, lmrm[2])
                    if on is None:
                        sub = left + mid + right
                    else:
                        sub = left + other[j]
                    result.append(sub)

        print("<{}> {} JOIN <{}> ".format(self.name, mod.upper(), other.name), end="")
        if on is None:
            print()
        else:
            print("ON {}".format(on.replace(" ", "")))
        return Table(result)

    def __matmul__(self, other):
        return self._join(other)

    def __mul__(self, other):
        result = [self.gethead() + other.gethead()]
        for i in range(1, len(self)+1):
            for j in range(1, len(other)+1):
                sub = self[i] + other[j]
                result.append(sub)
        print("<{}> CROSS <{}> ".format(self.name, other.name))
        return Table(result)

    cross = __mul__

    def copy(self,name=None):
        result =Table([r for r in self.table])
        result.name=name
        return result

    def __pow__(self, power, modulo=None):
        if power < 0:
            return None
        if power == 0:
            return Table(self.gethead())
        r=self.copy()
        for i in range(power-1):
            r=r*self
        return r

    def getset(self):
        return set([tuple(r) for r in self])

    def __or__(self, other):
        selfset= self.getset()
        otherset= other.getset()
        sss=selfset|otherset
        result= [self.gethead()]
        for v in sss:
            result.append(list(v))
        return Table(result)

    def __and__(self,other):
        selfset= self.getset()
        otherset= other.getset()
        sss=selfset&otherset
        result= [self.gethead()]
        for v in sss:
            result.append(list(v))
        return Table(result)

    def __xor__(self,other):
        selfset= self.getset()
        otherset= other.getset()
        sss=selfset^otherset
        result= [self.gethead()]
        for v in sss:
            result.append(list(v))
        return Table(result)

    def __sub__(self,other):
        selfset= self.getset()
        otherset= other.getset()
        sss=selfset-otherset
        result= [self.gethead()]
        for v in sss:
            result.append(list(v))
        return Table(result)

    def union(self, other):
        pass

    def orderby(self, s):
        # this should be done at origin vaiable not output another new
        s = slist(s)
        for v in s:
            if not self._check(v):
                raise Exception("no attribute {} in {}".format(v, self.name))
        else:
            array = []
            for i in range(1, len(self)+1):
                array.append([[self.get(i, v) for v in s], i])
            array.sort()
            result = [self.gethead()]
            for v in array:
                result.append(self.table[v[1]].copy())
            return Table(result)
        pass

    def setlib():
        s = """
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
        return exec(s, globals(), locals())


    def addcol(self, name, array):
        name = name.strip()
        if name not in self.colmap:
            try:
                n = wid(self)
                self.table[0].append(name)
            except:
                n = 0
                self.table.append([name])
            self.colmap[name] = n
            self.lenmap.append(len(str(name)))

            for i in range(len(array)):
                v = array[i]
                if n == 0:
                    self.table.append([v])
                else:
                    self.table[i + 1].append(v)
                # print(self.lenmap,n,str(v))
                self.lenmap[n] = max(self.lenmap[n], len(str(v)))

    def bar(self, label, value):
        Table.setlib()
        self.orderby(label)
        fig, ax = plt.subplots()
        ax.bar([str(v) for v in self.col(label)], self.col(value))
        plt.xlabel(label)
        plt.ylabel(value)
        pan_zoom = PAZ(fig)
        plt.show()

    def pie(self, label, value):
        Table.setlib()
        fig, ax = plt.subplots()
        ax.pie(self.col(value), labels=self.col(label), autopct='%1.1f%%')
        pan_zoom = PAZ(fig)
        plt.show()

    def hist(self, value, low, up, num):
        Table.setlib()
        fig, ax = plt.subplots()
        amount = up - low
        block = amount / num
        bins = [low + i * block for i in range(num + 2)]
        ax.hist(self.col(value), bins, facecolor='green', edgecolor="yellowgreen")
        plt.xlabel(value)
        plt.ylabel("number")
        pan_zoom = PAZ(fig)
        plt.show()

    def plot(self, x, y, line="."):
        # add polar coord
        # add multiple and lines
        # add spline
        Table.setlib()
        fig, ax = plt.subplots()
        ax.plot(self.col(x), self.col(y), line)
        plt.xlabel(x)
        plt.ylabel(y)
        pan_zoom = PAZ(fig)
        plt.show()



    def union(self, other):
        # if one have more attributes include less one with None
        pass

    def intersect(self, other):
        pass

    def minus(self, other):
        pass

    def radar(self):
        # multiple in one graph
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
        # classify the value
        pass

    def groupby(self, s):
        # group table by attributes in s
        # form a subtable in groupby dictionary
        pass
