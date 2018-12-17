import csv
from random import *
from .row import *
from .rows import *
from .keymap import *
from .groupmap import *
from time import *
###############################################################

class Table:
    coding = "utf-8"
    delimiter = ','
    quotechar = '"'
    limit = 1000
    precision=5



    #==================static & preset========================
    #see static location, preset, get and set static variable
    #记得缓存上次打开的目录地址
    def look():
        d ={}
        for key in Table.__dict__:
            if not (key[0] == "_" and key[1] != "_"):
                d[key] = Table.__dict__[key]
        atrid ={}
        fund = {}
        for key in d:
            if callable(d[key]):
                fund[key] = d[key]
            else:
                atrid[key]=d[key]

        pprint(atrid)
        pprint(fund)

    #=========================initialize============================
    def __init__(self, array2d=None, name=None, printable=True):

        self.name = name
        self.array2d = []
        self.colmap = {}

        # index for iterator
        self.imax = -1
        self.imap = []

        #for print
        self.lenmap = None #should be list
        self.sepmap = None  # track seperate seperate symbol

        self.castmap=[]     #use to cast the value
        self.typemap=None    #use to check type of object

        self.keymap = None
        self.groupmap = None

        #the follow statement might not work
        if isinstance(array2d,Table):
            self = array2d

        if not array2d:
            pass
        elif isinstance(array2d, list):
            good = True
            for v in array2d:
                if not isinstance(v, list):
                    good = False
            if good:
                self.array2d = array2d
            else:
                raise Exception("array2d should be 2D-list")
            self.setcolmap()

            if len(self.array2d) < Table.limit and printable:
                self.enableprint()
        else:
            raise Exception("array2d should be 2D-list")


    def enableprint(self):
        self.setsepmap()
        self.setlenmap()

    def make(head, i, name = None, printable = True):
        # error!!!!
        if isinstance(head, str) or isinstance(head, list) or isinstance(head,tuple):
            if isinstance(head, str):
                head = slist(head)
            elif isinstance(head,tuple):
                head = list(head)
            else:
                pass
            array2d = inilist2d(i, len(head))
            result = Table([head] + array2d, printable)
            if name:
                result.name = name
            return result
        else:
            raise Exception("head must be init")

    #================================read & save==============================
    def read(name, castmap=None, printable = True):
        t1 =time()
        result = []
        fname = name + ".csv"
        file = open(fname, "r", encoding=Table.coding, newline='')
        lines = csv.reader(file, delimiter=Table.delimiter, quotechar=Table.quotechar)
        if castmap !=None:

            row = next(lines)
            #print(row)
            if Table.coding=="utf-8":
                row[0]=row[0].replace("\ufeff","")
            vlist = row
            result.append(vlist)
            #print(result)
            for row in lines:
                #print(row)
                vlist = [castmap[i](row[i]) for i in range(len(row))]
                result.append(vlist)
        else:
            for row in lines:
                vlist =[valueof(s) for s in row]
                result.append(vlist)
            if Table.coding=="utf-8":
                result[0][0]=result[0][0].replace("\ufeff","")
        file.close()
        t2 = time()
        #pprint(result)
        result = Table(result, name, printable)
        t3 = time()
        print("READ <{}> FROM {} takes {} + {}".format(name, fname,round(t2-t1,Table.precision),round(t3-t2,Table.precision)))
        result.castmap=castmap
        return result

    def save(self, name=None,show=True):
        t1 = time()
        if Table.coding=="utf-8":
            self[0][0]="\ufeff"+self[0][0]
        # ask for ensure!!!
        if self.name is None and name is None:
            raise Exception("give a name for the array2d to save")
        elif self.name is None and isinstance(name, str):
            self.name = name
        fname = self.name + ".csv"
        file = open(fname, "w", encoding=Table.coding, newline='')
        lines = csv.writer(file, delimiter=Table.delimiter, quotechar=Table.quotechar, quoting=csv.QUOTE_MINIMAL)
        for row in self.array2d:
            lines.writerow(row)
        file.close()

        t2 = time()
        if show:
            print("SAVE <{}> TO {} takes {}".format(self.name, fname,t2-t1))
        return

    def savea(self,show=False):
        t1 = time()
        if self.name is None and name is None:
            raise Exception("give a name for the array2d to save")
        fname = self.name + ".csv"
        file = open(fname, "a", encoding=Table.coding, newline='')
        lines = csv.writer(file, delimiter=Table.delimiter, quotechar=Table.quotechar, quoting=csv.QUOTE_MINIMAL)
        row  = self.array2d[-1]
        lines.writerow(row)
        file.close()
        t2 = time()
        if show:
            print("SAVE <{}> {}-th row TO {} takes {}".format(self.name,len(self), fname,t2-t1))
        return
        
    #===================================valid checking part============================
    def _REatri(self, a):
        return a in self.colmap
    def _REatris(self, lst):
        l = []
        result = True
        for v in lst:
            if v not in self.colmap:
                result = False
                l.append(v)
        if not result:
            raise Exception("No Attribute(s): {}".format(",".join(l)))
        return result

    #============================general help function=================
    def gethead(self):
        return self.array2d[0]

    # include classify, group, etc all vary by different mod
    def getsearchmap(self, ls):
        if isinstance(ls, str):
            ls = slist(ls, ",")
        self._REatris(ls)  # check attributes valid
        result = {}
        for i in range(1, len(self) + 1):
            t = tuple(self.getlist(i, ls))
            if t in result:
                result[t].append(i)
            else:
                result[t] = [i]
        return result



    # ===========================debug, print & str===================================
    # function in this block will not work or minimal information when len(self)> Table.threshold
    #used for debug
    def fsee(self):
        if len(self)<=self.limit:
            pprint(self.__dict__)
        else:
            raise Exception("len(self) > limit full print is not support")

    def asee(self):
        if len(self) <= self.limit:
            pprint(self.array2d)
        else:
            raise Exception("len(self) > limit full print is not support")

    def ksee(self):
        if len(self) <= self.limit:
            pprint(self.keymap)
        else:
            raise Exception("len(self) > limit full print is not support")

    def gsee(self):
        if len(self) <= self.limit:
            pprint(self.groupmap)
        else:
            raise Exception("len(self) > limit full print is not support")

    def see(self):
        d=self.__dict__.copy()
        d["array2d"]="......"
        if d["keymap"] is not None:
            kd = d["keymap"].copy()
            kd["map"] = "......"
            d["keymap"]=kd
        if d["groupmap"] is not None:
            gd = d["groupmap"].copy()
            gd["map"] = "......"
            d["groupmap"] = gd
        pprint(d)

    def _destripC(s, n):
        dis = n - clen(s)
        front = dis // 2
        back = dis - front
        space = " "
        return front * space + s + back * space
    def _destripL(s, n):
        return s + " " * (n - clen(s))
    spacing = _destripC
    def shift():
        if Table.spacing == Table._destripC:
            Table.spacing = Table._destripL
        elif Table.spacing == Table._destripL:
            Table.spacing = Table._destripC

    #delet sepmap only used in print

    def _row2str(self, v, sep="|"):
        seplist = inilist(wid(self), None)
        for j in range(wid(self)):
            seplist[j] = strsep2list(str(v[j]), self.sepmap[j], self.lenmap[j])
        m = max(len(v) for v in seplist)
        for j in range(wid(self)):
            dis = m - len(seplist[j])
            seplist[j] += inilist(dis, "")

        for j in range(wid(self)):
            for i in range(m):
                seplist[j][i] = Table.spacing(seplist[j][i], self.lenmap[j])

        # print(seplist)
        # print("======")
        ls = []
        for i in range(m):
            ls.append(sep.join([seplist[j][i] for j in range(wid(self))]))
        return '\n'.join(ls)
    def _head2str(self, sep="|"):
        head = self.gethead().copy()
        ls = []
        for i in range(len(head)):
            s = str(head[i])
            if self.keymap is not None and head[i] in self.keymap.key:
                s += Keymap.symbol
            if self.groupmap is not None and head[i] in self.groupmap.group:
                s += Groupmap.symbol
            ls.append(s)
        return self._row2str(ls, sep)
    def _head2list(self, sep="|"):
        head = self.gethead()
        ls = []
        for i in range(len(head)):
            s = str(head[i])
            if self.keymap is not None and head[i] in self.keymap.key:
                s += Keymap.symbol
            if self.groupmap is not None and head[i] in self.groupmap.group:
                s += Groupmap.symbol
            ls.append(s)
        return self._row2list(ls, sep)
    def _row2list(self, v, sep="|"):
        seplist = inilist(wid(self), None)
        for j in range(wid(self)):
            seplist[j] = strsep2list(str(v[j]), self.sepmap[j], self.lenmap[j])
        m = max(len(v) for v in seplist)
        for j in range(wid(self)):
            dis = m - len(seplist[j])
            seplist[j] += inilist(dis, "")
        for j in range(wid(self)):
            for i in range(m):
                seplist[j][i] = Table.spacing(seplist[j][i], self.lenmap[j])
        ls = []
        for i in range(m):
            ls.append(sep.join([seplist[j][i] for j in range(wid(self))]))
        return ls

    def _RElimit(self):
        if len(self) > Table.limit:
            raise Exception("length of table surpass the limit")

    #change to
    def __str__(self):
        self._RElimit()
        if self.lenmap is None:
            self.setlenmap()
        if self.sepmap is None:
            self.setsepmap()
        s = ""
        s += self._head2str() + '\n'
        for v in self:
            s += self._row2str(v) + "\n"
        s += str(len(self)) + " row(s)"
        return s

    def __repr__(self):
        # use summerize information
        # return self.row2str(self.row(0)) +"\n"+str(len(self.array2d)-1)+" row(s)"
        return str(self)



    def pl(self):
        self._RElimit()
        if self.lenmap is None:
            self.setlenmap()
        if self.sepmap is None:
            self.setsepmap()
        fstr = str(len(self.array2d)) + " row(s)"
        s = self._head2str()
        command = input(s)

        if command == "exit":
            print(fstr, end="")
            return
        for v in self:
            s = self._row2str(v)
            command = input(s)
            if command == "exit":
                break
        print(fstr, end="")

    def pi(self):
        self._RElimit()
        # problem at here！！！? fixed?
        if self.lenmap is None:
            self.setlenmap()
        if self.sepmap is None:
            self.setsepmap()
        itable = list(range(len(self) + 1))
        itable = Table(rotlist12(itable))
        jtable = [[self.name] + list(range(0, wid(self)))]
        jtable = Table(jtable)
        first = max(jtable.lenmap[0], itable.lenmap[0])
        jtable.lenmap[0] = first
        itable.lenmap[0] = first
        for i in range(1, len(jtable.lenmap)):
            jtable.lenmap[i] = max(jtable.lenmap[i], self.lenmap[i - 1])

        sep = ":"
        s = ""
        length = itable.lenmap[0] + clen(sep)
        s += jtable._head2str(sep) + "\n"
        s += itable._head2str() + sep

        headlist = self._head2list()
        # pprint(selflist)
        for i in range(len(headlist)):

            if i != 0:
                s += " " * length
            s += headlist[i] + "\n"

        for i in range(1, len(self) + 1):
            s += itable._row2str(itable.array2d[i]) + sep

            selflist = self._row2list(self.array2d[i])
            # pprint(selflist)
            for i in range(len(selflist)):

                if i != 0:
                    s += " " * length
                s += selflist[i] + "\n"
        s = s[:-1]
        print(s)

    def setsepmap(self, j=None, sep='\n'):
        if j is None:
            n = wid(self)
            self.sepmap = inilist(n, '\n')
        else:
            if isinstance(j,str):
                j = self._modicolinput(j)
            self.sepmap[j] = sep
            self._setlenmapj(j)

    def setsep(self,**kwargs):
        for key in kwargs:
            self.setsepmap(key,kwargs[key])

    def setlen(self, **kwargs):
        for key in kwargs:
            index = self._modicolinput(key)
            self.lenmap[index]= kwargs[key]

    #set & track lenmap

    def setlenmap(self):
        if len(self) <= Table.limit:
            lenmap = []
            for i in range(wid(self)):
                lenmap.append(max([maxlen(v[i], self.sepmap[i]) for v in self.array2d]))
            self.lenmap = lenmap
        else:
            raise Exception("table is too long, lenmap is not supported")

    def _recaplenmap(self, row):
        # recap lenmap by delete row
        if self.lenmap is not None:
            for j in range(wid(self)):
                if maxlen(row[j], self.sepmap[j]) == self.lenmap[j]:
                    self.lenmap[j] = max([maxlen(v[j], self.sepmap[j]) for v in self.array2d])

    def _setlenmapj(self, j):
        # set lenmap by col
        if self.lenmap is not None:
            self.lenmap[j] = max([maxlen(v[j], self.sepmap[j]) for v in self.array2d])

    def _setlenmapi(self, i):

        # set lenmap by row
        if self.lenmap is not None:
            row = self.array2d[i]
            for j in range(wid(self)):
                self.lenmap[j] = max(self.lenmap[j], maxlen(row[j], self.sepmap[j]))

    def _setlenmapij(self, i, j):
        # refresh entry i,j
        if self.lenmap is not None:
            self.lenmap[j] = max(self.lenmap[j], maxlen(self.array2d[i][j], self.sepmap[j]))

    def setcolmap(self):
        head = self.gethead()
        for i in range(wid(self)):
            self.colmap[head[i]] = i

    # ===========================add & del, col & row===================================
    # need to check
    def _recapcolindex(self, j):
        j = wid(self) + j if j < 0 else j
        if j < 0 or j > wid(self):
            raise Exception("invalid col index")
        return j
    def _recaprowindex(self, i):
        i = len(self) + 1 + i if i < 0 else i
        if i < 0 or i > len(self) + 1:
            raise Exception("invalid row index")
        return i

    def addcol(self, j=-1):
        j = self._recapcolindex(j) + 1 if j < 0 else j
        # track colmap
        top = self.array2d[0]
        for i in range(j, wid(self)):

            key = top[i]
            if key != None:
                self.colmap[key] += 1
        # track bindmap
        # track array2d
        for i in range(0, len(self) + 1):
            self.array2d[i].insert(j, None)
        # track lenmap
        self.lenmap.insert(j, 4)
        
        # name row 0 and track colmap
        i=1
        while "new"+str(i) in self.colmap:
            i+=1
        newcol="new"+str(i)
        
        self.array2d[0][j]=newcol
        self.colmap[newcol]=j
        
        #track sepmap
        self.sepmap.append("\n")

        
    def addcols(self, n, i=-1):
        for x in range(n):
            self.addcol(i)
    def delcol(self, j=-1):
        j = self._recapcolindex(j)
        if self.keymap is not None and self.array2d[0][j] in self.keymap.key:
            self.keymap = None
        if self.groupmap is not None and self.array2d[0][j] in self.groupmap.group:
            self.groupmap = None

        # track colmap
        top = self.array2d[0]
        for i in range(j, wid(self)):
            # print("j=", j)
            key = top[i]
            # print("key = ", key)
            self.colmap[key] -= 1
        del self.colmap[top[j]]
        # tack bindmap

        # actually delete
        for i in range(0, len(self) + 1):
            del self.array2d[i][j]
        # track lenmap
        del self.lenmap[j]

    def addrow(self, i=-1):
        i = self._recaprowindex(i) + 1 if i < 0 else i
        if i == 0:
            raise Exception("invalid row index")
        if self.keymap is not None:
            self.keymap.trackaddrow(i)
        if self.groupmap is not None:
            self.groupmap.trackaddrow(i)
        # track bindmap
        newrow = inilist(wid(self), None)
        self.array2d.insert(i, newrow)
        self._setlenmapi(i)

    def append(self,value):
        self.addrow()
        self[-1][:]=value

    def addrows(self, n, i=-1):
        for x in range(n):
            self.addrow(i)
    def delrow(self, i=-1):
        i = self._recaprowindex(i)
        if i == 0:
            raise Exception("invalid row index")
        if self.keymap is not None:
            self.keymap.trackdelrow(i)
        if self.groupmap is not None:
            self.groupmap.trackdelrow(i)
        # track bindmap
        row = self.array2d.pop(i)
        self._recaplenmap(row)

    def setentry(self, i, j, value):
        i = len(self) + 1 + i if i < 0 else i
        j = wid(self) + 1 + j if j < 0 else j
        if self.array2d[i][j] == value:
            return
        # print("i,j = ",i,j)
        if i == 0:
            # set the head
            if value in self.colmap:
                raise Exception("such attribute already exist in colmap")
            else:
                oldatt = self.array2d[i][j]
                if oldatt in self.colmap:
                    del self.colmap[oldatt]
                self.colmap[value] = j
                # track keymap
                if self.keymap is not None and oldatt in self.keymap.key:
                    self.keymap.updatekey(oldatt, value)
                # track groupmap
                if self.groupmap is not None and oldatt in self.groupmap.group:
                    self.groupmap.updategroup(oldatt, value)
                # track bindmap
        else:
            if self.keymap is not None:
                self.keymap.tracksetentry(i, j, value)
            if self.groupmap is not None:
                self.groupmap.tracksetentry(i, j, value)
            # track bindmap set all in bindmap to such value
        # actually set entry
        self.array2d[i][j] = value
        self._setlenmapij(i, j)

    # ====================len & next & iter====================
    # good
    def __len__(self):
        return len(self.array2d) - 1
    def __next__(self):
        if self.imap[self.imax] == len(self):
            self.imap.pop()
            self.imax -= 1
            raise StopIteration
        self.imap[self.imax] += 1
        return self.array2d[self.imap[self.imax]]
    def __iter__(self):
        self.imax += 1
        self.imap.append(0);
        return self


    #=======================get,set,del===========================
    #取消group 选项, 查找同group的index 用findgroup()
    # fix bug & rearrange help function

    def _modicolinput(self, key):
        #used in Row and Rows
        if isinstance(key, int) or isinstance(key, str):
            index = None
            if isinstance(key, int):
                index = self._recapcolindex(key)
            elif isinstance(key, str):
                index = self.colmap[key]
        return index

    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, str):
            index = None
            if isinstance(key, int):
                index = self._recaprowindex(key)
            elif isinstance(key, str):
                index = self._str2index(key)
                if isinstance(index, list):
                    return self.__getitem__(index)
            # return a Row
            return Row(self, index)

        elif isinstance(key, slice) or isinstance(key, tuple) or isinstance(key, list):
            ls = None
            if isinstance(key, slice):
                sindex = 1 if key.start is None else key.start
                eindex = len(self) if key.stop is None else key.stop
                sindex = self._recaprowindex(sindex)
                eindex = self._recaprowindex(eindex)
                ls = list(range(sindex, eindex + 1))
            elif isinstance(key, tuple) or isinstance(key, list):
                ls = []
                for v in key:
                    if isinstance(v, str):
                        index = self._str2index(v)
                        if isinstance(index, int):
                            ls.append(index)
                        elif isinstance(index, list):
                            ls.extend(index)
                    elif isinstance(v, int):
                        ls.append(self._recaprowindex(v))
            # ls done start make a Rows
            return Rows(self, ls)

        pass
    def __setitem__(self, key, value):
        # need to implement！！！
        if isinstance(key, int) or isinstance(key, str):
            index = None
            if isinstance(key, int):
                index = self._recaprowindex(key)
            elif isinstance(key, str):
                index = self._str2index(key)
                if isinstance(index, list):
                    self.__setitem__(index,value)
                    return
            if isinstance(value, tuple) or isinstance(value, list):
                # check length
                if len(value) == wid(self):
                    for j in range(wid(self)):
                        self.setentry(index, j, value[j])
                else:
                    raise Exception("width not mapping")
            else:
                for j in range(wid(self)):
                    self.setentry(index, j, value)

        # do something
        # slice, list of int list of str
        elif isinstance(key, slice) or isinstance(key, tuple) or isinstance(key, list):
            ls = None
            if isinstance(key, slice):
                sindex = 1 if key.start is None else key.start
                eindex = len(self) if key.stop is None else key.stop
                sindex = self._recaprowindex(sindex)
                eindex = self._recaprowindex(eindex)
                ls = list(range(sindex, eindex + 1))
            elif isinstance(key, tuple) or isinstance(key, list):
                ls = []
                for v in key:
                    if isinstance(v, str):
                        index = self._str2index(v)
                        if isinstance(index, int):
                            ls.append(index)
                        elif isinstance(index, list):
                            ls.extend(index)
                    elif isinstance(v, int):
                        ls.append(self._recaprowindex(v))
            # start assign
            if isinstance(value, list) or isinstance(value, tuple):

                if isinstance(value[0], list) or isinstance(value[0], tuple):
                    # 2D - array
                    # check length
                    if len(value) != len(ls):
                        raise Exception("length not mapping")
                    # check length
                    for v in value:
                        if len(v) != wid(self):
                            raise Exception("width not mapping")
                    vindex = 0
                    for index in ls:
                        for j in range(wid(self)):
                            self.setentry(index, j, value[vindex][j])
                        vindex += 1
                else:
                    # 1D - array
                    # check width
                    if (len(value)) != wid(self):
                        raise Exception("width not mapping")
                    for index in ls:
                        for j in range(wid(self)):
                            self.setentry(index, j, value[j])
            else:
                # single value
                for index in ls:
                    for j in range(wid(self)):
                        self.setentry(index, j, value)

            pass
    def __delitem__(self, key):
        # start for testing!!!
        if isinstance(key, int):
            index = self._recaprowindex(key)
            self.delrow(index)
        elif isinstance(key, str):
            index = self._str2index(key)
            if isinstance(index,int):
                self.delrow(index)
            elif isinstance(index,list):
                index.sort(reverse=True)
                for i in index:
                    self.delrow(i)
                return
            else:
                raise Exception("int or list of int!")
        elif isinstance(key, slice):
            sindex = 1 if key.start is None else key.start
            eindex = len(self) if key.stop is None else key.stop
            sindex = self._recaprowindex(sindex)
            eindex = self._recaprowindex(eindex)

            for i in range(eindex, sindex - 1, -1):
                self.delrow(sindex)
        elif isinstance(key, tuple) or isinstance(key, list):
            ls = []
            for v in key:
                if isinstance(v, str):
                    index = self._str2index(v)
                    if isinstance(index, int):
                        ls.append(index)
                    elif isinstance(index, list):
                        ls.extend(index)
                elif isinstance(v, int):
                    ls.append(self._recaprowindex(v))
            ls.sort(reverse=True)
            for index in ls:
                self.delrow(index)
        pass
    def _str2index(self, key):
        #check all value of
        key = slist(key)
        t = tuple([valueof(v) for v in key])
        if self.keymap is not None and t in self.keymap.map:
            index = self.keymap.map[t]
            return index
        else:
            raise Exception("please set key")

    def iof(self,*args):
        return self.keymap.map[args]

    def getlist(self, i, ls):
        """
        print("i = ",i)
        r = []
        for v in ls:
            print("v=",v)
            j = self.colmap[v]
            print("j = ", j)

            row = self.array2d[i]
            print("row = ",row)
            value = row[j]
            print("value = ",value)
            r.append(value)
        print("r = ",r)
        """

        return [self.array2d[i][self.colmap[v]] for v in ls]
    def _getcolindex(self, key):
        # for Row and Rows usage
        if isinstance(key, int):
            if key >= 0 and key < len(self):
                return key
            else:
                raise Exception("index out of range")
        elif isinstance(key, str):
            if self._REatri(key):
                return self.colmap[key]
            else:
                raise Exception("attribute name not exist")
        else:
            raise KeyError("only int or str is supported")
    def _getrowindex(self, key):
        if self.keymap is not None:
            return self.keymap.map[key]
        else:
            raise Exception("please use setkeymap to set keymap")

    #=====================================SQL part=========================

    def rename(self, s):
        s = decomp(s)
        self._REatris(s[0])
        for i in range(len(s[0])):
            self.colmap[s[1][i]] = self.colmap[s[0][i]]
            del self.colmap[s[0][i]]
            self.array2d[0][self.colmap[s[1][i]]] = s[1][i]
            self.lenmap[self.colmap[s[1][i]]] = max(self.lenmap[self.colmap[s[1][i]]], len(s[1][i]))
            print("RENAME {} TO {}".format(s[0][i], s[1][i]))

    def _getLMR(self, other):
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

    def _join(self, other, on=None, mod="natural"):
        if mod not in {"natural", "left", "right", "full"}:
            raise Exception("invalid mod")
        # check mod valid
        if on is None:
            lmr = self._getLMR(other)
            lmrm = lmr + [lmr[1]]
        else:
            mm = decomp(on)
            self._REatris(mm[0])
            other._REatris(mm[1])
            l = list(set(self.colmap) - set(mm[0]))
            r = list(set(other.colmap) - set(mm[1]))
            lmrm = [l, mm[0], r, mm[1]]
        print(lmrm)
        selfsmap = self.getsearchmap(lmrm[1])
        othersmap = other.getsearchmap(lmrm[3])
        selfset = set(selfsmap)
        otherset = set(othersmap)
        sharedentry = selfset & otherset
        if on is None:
            result = [lmrm[0] + lmrm[1] + lmrm[2]]
        else:
            result = [self.gethead().copy() + other.gethead().copy()]
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

    def join(self,other,on =None):
        return self._join(other,on,mod = "natural")

    def ljoin(self,other,on =None):
        return self._join(other,on,mod = "left")

    def rjoin(self,other,on =None):
        return self._join(other,on,mod = "right")

    def fjoin(self,other,on =None):
        return self._join(other,on,mod = "full")

    def __matmul__(self, other):
        return self._join(other)
    def __mul__(self, other):
        result = [self.gethead().copy() + other.gethead().copy()]
        for i in range(1, len(self) + 1):
            for j in range(1, len(other) + 1):
                sub = self[i] + other[j]
                result.append(sub)
        print("<{}> CROSS <{}> ".format(self.name, other.name))
        return Table(result)

    cross = __mul__

    def __pow__(self, power, modulo=None):
        if power < 0:
            return None
        if power == 0:
            return Table(self.gethead().copy())
        r = self.copy()
        for i in range(power - 1):
            r = r * self
        return r

    def _getset(self):
        return set([tuple(r) for r in self])

    def __or__(self, other):
        selfset = self._getset()
        otherset = other._getset()
        sss = selfset | otherset
        result = [self.gethead().copy()]
        for v in sss:
            result.append(list(v))
        return Table(result)
    def __and__(self, other):
        selfset = self._getset()
        otherset = other._getset()
        sss = selfset & otherset
        result = [self.gethead().copy()]
        for v in sss:
            result.append(list(v))
        return Table(result)
    def __xor__(self, other):
        selfset = self._getset()
        otherset = other._getset()
        sss = selfset ^ otherset
        result = [self.gethead().copy()]
        for v in sss:
            result.append(list(v))
        return Table(result)
    def __sub__(self, other):
        selfset = self._getset()
        otherset = other._getset()
        sss = selfset - otherset
        result = [self.gethead().copy()]
        for v in sss:
            result.append(list(v))
        return Table(result)

    union = __or__

    intersect = __and__

    minus = __sub__

    # select perform function as copy()
    def select(self,mod=all, where = None,**kwargs):
        if self.groupmap is not None:
            head = list(kwargs.keys())
            #print(head)
            length = len(self.groupmap.map)
            result = Table.make(head,length,printable=False)
            # start check
            for key in kwargs:
                if kwargs[key] == '':
                    kwargs[key]=key
                if not callable(kwargs[key]) and kwargs[key] not in self.groupmap.group:
                    raise Exception("select col must be in the group")

            for key in kwargs:
                if callable(kwargs[key]):
                    mp=self.groupmap.map
                    result[:][key]=[kwargs[key](Rows(self,list(mp[gk]))) for gk in mp]
                else:
                    index = self.groupmap.group.index(kwargs[key])
                    mp = self.groupmap.map
                    result[:][key]=[tp[index] for tp in mp]
            #get rid of where = false
            if callable(where):
                i = 1
                while i <= len(result):
                    if not where(Row(result,i)):
                        result.delrow(i)
                        i-=1
                    i+=1
            elif where is None:
                pass
            else:
                raise Exception("where should be a function or None")
            #result
            self.ungroup()
            result.enableprint()
            #print some thing to notify
            return result
        else:
            #group is None
            result = None
            box = None
            adding = None
            getout = None
            if mod == all:
                box = []
                def adding(s,ls):
                    s.append(ls.copy())
                getout = lambda x : x
            elif mod == any:
                box = set()
                def adding(s,ls):
                    s.add(tuple(ls))
                getout = lambda x:[list(v) for v in x]
            else:
                raise Exception("mod must be all or any")

            if kwargs == {}:
                if where is None:
                    for r in self:
                        adding(box,r.copy())
                elif callable(where):
                    for i in range(1,len(self)+1):
                        if where(Row(self,i)):
                            adding(box,self.array2d[i].copy())
                else:
                    raise Exception("where must be None or function")
                result=Table([self.gethead().copy()]+getout(box))
                return result
            else:
                #process kwargs
                for key in kwargs:
                    if kwargs[key] == '':
                        kwargs[key] = key
                    if not callable(kwargs[key]):
                        self._REatri(kwargs[key])
                #start using
                if where is None:
                    for i in range(1,len(self)+1):
                        r =Row(self,i)
                        ls = [r[kwargs[key]] if isinstance(kwargs[key],str) else kwargs[key](r) for key in kwargs]
                        adding(box,ls)
                elif callable(where):
                    for i in range(1,len(self)+1):
                        r= Row(self,i)
                        if where(r):
                            ls = [r[kwargs[key]] if isinstance(kwargs[key],str) else kwargs[key](r) for key in kwargs]
                            adding(box,ls)
                else:
                    raise Exception("where must be None or function")
                #pprint(box)
                result=Table([list(kwargs.keys())]+getout(box))
                return result
            #print("SELECT {} from <{}>".format(",".join(result.gethead()), self.name))

    def makedict(self,kname,vname):
        d={}
        for r in range(1,len(self)+1):
            key= self[r][kname]
            value=self[r][vname]
            if key not in d:
                d[key]=value
            else:
                raise Exception("duplicate keys")
        return d

   
    def orderby(self, key=None, reverse=False):
    # after orderby will return self
        # change when next edition to seperate attribute name and normal entry
        # this should be done at origin vaiable not output another new
        # change case when group is done
        if key is None:
            self.array2d[1:]= sorted(self.array2d[1:],reverse)
        elif callable(key):

            rs = [Row(self,i+1) for i in range(len(self.array2d[1:]))]
            srs =sorted(rs,key=key,reverse=reverse)
            sls = [r.array for r in srs]
            self.array2d[1:]=sls
            #self.array2d[1:]= sorted([Row(self,i+1) for i in range(len(self.array2d[1:]))],key=key,reverse=reverse)
        elif isinstance(key,str):
            s = slist(key)
            self._REatris(s)
            indice =[self._modicolinput(key) for key in s]
            def sfunction(r):
                return [r[i] for i in indice]
            self.array2d[1:] = sorted(self.array2d[1:],key=sfunction,reverse=reverse)
        #refresh all
        if self.keymap is not None:
            self.setkey(self.keymap.key)
        if self.groupmap is not None:
            self._setgroup(self.groupmap.group)
        #other refresh
        return self



    #去掉groupmap 用search map代替
    #思考group by 内容，和功能
    #COUNT, MAX, MIN, SUM, AVG
    #aggregate method
    # could be used with select
    # could apply function to the row or entry
    #group by will return a new table with in group

    def setkey(self, s):
        self.keymap = Keymap.make(self, s)

    def delkey(self):
        self.keymap = None

    def groupby(self, s,having = None):
        # group array2d by attributes in s
        # form a subtable in groupby dictionary
        self.groupmap = Groupmap.make(self, s, having)
        return self

    def ungroup(self):
        self.groupmap=None

    def groupof(self,*args):
        if self.groupmap is not None and args in self.groupmap.map:
            indices = list(self.groupmap.map[args])
            return indices
        else:
            raise  Exception("not have such group")
    #==================================graph part=============================
    plt=None
    paz=None
    try:
        import matplotlib.pyplot as plt
    except:
        print("please install matplotlib")
        displayable = False
    try:
        from .mpl_interaction import PanAndZoom as paz
    except:
        print("please download mpl_interaction.py")
        interable = False

    def bar(self, label, value):
        self.orderby(label)
        fig, ax = Table.plt.subplots()
        ax.bar(self[:][label], self[:][value])
        Table.plt.xlabel(label)
        Table.plt.ylabel(value)
        if Table.paz is not None:
            pan_zoom = Table.paz(fig)
        Table.plt.show()

    def pie(self, label, value):
        fig, ax = Table.plt.subplots(figsize=(6,6))
        ax.pie(self[:][value], labels=self[:][label], autopct='%1.1f%%')
        if Table.paz is not None:
            pan_zoom = Table.paz(fig)
        Table.plt.show()

    def hist(self, value, low, up, num):
        #another optional low up step
        fig, ax = Table.plt.subplots()
        amount = up - low
        block = amount / num
        bins = [low + i * block for i in range(num + 2)]
        ax.hist(self[:][value], bins, facecolor='green', edgecolor="yellowgreen")
        Table.plt.xlabel(value)
        Table.plt.ylabel("number")
        if Table.paz is not None:
            pan_zoom = Table.paz(fig)
        Table.plt.show()

    def plot(self, x, y, line="."):
        # add polar coord
        # add multiple and lines
        # add spline
        fig, ax = Table.plt.subplots()
        ax.plot(self[:][x], self[:][y], line)
        Table.plt.xlabel(x)
        Table.plt.ylabel(y)
        if Table.paz is not None:
            pan_zoom = Table.paz(fig)
        Table.plt.show()

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




    #==============================apply & extend function part =======================
    def apply(self, key, fparamod=None, f=None, *args,**kwargs):
        j = self._modicolinput(key)
        if fparamod == "e":
            for i in range(1, len(self) + 1):
                self[i][j] = f(self[i][j], *args,**kwargs)
        elif fparamod == "r":
            for i in range(1, len(self) + 1):
                self[i][j] = f(self[i], *args,**kwargs)
        elif fparamod == None:
            for i in range(1, len(self) + 1):
                self[i][j] = f(*args,**kwargs)
        if self.lenmap is not None:
            self._setlenmapj(j)

    def shuffle(self):
        if self.bindmap is not None:
            raise Exception("debind self all for shuffle")
        groupmap = self.groupmap
        keymap = self.keymap
        head = self.array2d.pop(0)
        shuffle(self.array2d)
        self.array2d.insert(0, head)
        if groupmap is not None:
            self._setgroup(groupmap.group)
        if keymap is not None:
            self.setkey(keymap.key)
