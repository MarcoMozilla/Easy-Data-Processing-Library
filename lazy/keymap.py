from pprint import *
from .utility import*

class Keymap(dict):

    symbol= "*"

    def __init__(self):
        dict.__init__(self)
        self.table = None
        self.key = []
        self.map = {}
        self["key"] = self.key
        self["map"] = self.map

    def fixlenmap(self):
        for v in self.key:
            self.table.lenmap[self.table.colmap[v]]+=len(Keymap.symbol)

    def __del__(self):
        self.table.setlenmap()
        if self.table.groupmap is not None:
            self.table.groupmap.fixlenmap()

    def make(table,s):
        result = Keymap()
        if isinstance(s,str):
            s = slist(s)
        result.key += s
        result.table = table
        result.table._REatris(result.key)
        for i in range(1,len(result.table)+1):
            t= tuple(result.table.getlist(i,result.key))
            if not t in result.map:
                result.map[t] = i
            else:
                print("row",result.map[t])
                print("row",i)
                raise Exception("{} is not a key".format(result.key))
        if result.table.lenmap is not None:
            result.lenmap = result.table.lenmap.copy()
            result.fixlenmap()
        return result


    def trackaddrow(self,i):

        for index in range(i,len(self.table)+1):
            t = tuple(self.table.getlist(index, self.key))
            self.map[t] +=1

    def trackdelrow(self,i):

        t = tuple(self.table.getlist(i, self.key))
        del self.map[t]
        for index in range(i+1, len(self.table) + 1):
            t = tuple(self.table.getlist(index, self.key))
            self.map[t] -= 1


    def updatekey(self,oldkey, newkey):
        for i in range(len(self.key)):
            if self.key[i] == oldkey:
                self.key[i]=newkey



    def tracksetentry(self,i,j,value):

        attname = self.table.array2d[0][j]
        if self.table.array2d[i][j] == value:
            return
        if attname in self.key:
            #make a key tuple
            r = []
            for s in self.key:
                if s == attname:
                    r.append(value)
                else:
                    r.append(self.table.array2d[i][self.table.colmap[s]])
            newt = tuple(r)
            #check existence
            if newt in self.map:
                raise Exception("key duplicated")
            #start update
            else:
                #try to del old tuple
                oldt = tuple(self.table.getlist(i, self.key))
                if oldt in self.map:
                    del self.map[oldt]
                #assign new tuple to map
                self.map[newt] = i








        
        
    
