from pprint import *
from .utility import *
from .row import *

class Groupmap(dict):

    symbol = "&"
    #using having = ...
    def __init__(self):
        self.table = None
        self.group = []
        self.map = {}
        self["group"] = self.group
        self["map"] = self.map


    def updategroup(self, oldgroup, newgroup):
        for i in range(len(self.group)):
            if self.group[i] == oldgroup:
                self.group[i] = newgroup


    def fixlenmap(self):
        for v in self.group:
            self.table.lenmap[self.table.colmap[v]]+=len(Groupmap.symbol)

    def __del__(self):
        self.table.setlenmap()
        if self.table.keymap is not None:
            self.table.keymap.fixlenmap()

    def make(table, s,having=None):
        result = Groupmap()
        if isinstance(s,str):
            s = slist(s)
        result.group+=s
        result.table = table
        result.table._REatris(result.group)
        if callable(having):
            for i in range(1, len(result.table) + 1):
                r = Row(result.table,i)
                if having(r):
                    t = tuple(result.table.getlist(i, result.group))
                    if t in result.map:
                        result.map[t].add(i)
                    else:
                        result.map[t] = {i}
        elif having is None:
            for i in range(1, len(result.table) + 1):
                t = tuple(result.table.getlist(i, result.group))
                if t in result.map:
                    result.map[t].add(i)
                else:
                    result.map[t] = {i}
        else:
            raise Exception("having must be a funtion or None")
        result.lenmap = table.lenmap.copy()
        result.fixlenmap()
        return result

    def trackaddrow(self, i):
        # 从table中找到第 i row，
        # 从第i row到第len(self)row (包括首尾)的
        # self.groupmap中找到value（是一个set），一边从set中删除，一边+1放回到set中
        #
        for index in range(i, len(self.table) + 1):
            t = tuple(self.table.getlist(index, self.group))
            self.map[t].remove(index)
            self.map[t].add(index + 1)

    def trackdelrow(self, i):
        # 从self.groupmap中的对应set中删除第 i-th row
        # 在self.keymap中 第ith row一直到末尾所有的key全部减一

        t = tuple(self.table.getlist(i, self.group))
        self.map[t].remove(i)
        if len(self.map[t]) == 0:
            del self.map[t]
        for index in range(i + 1, len(self.table) + 1):
            #print("index = ",i)
            t = tuple(self.table.getlist(index, self.group))
            #print("t = ", t)
            #pprint(self.map)
            self.map[t].remove(index)
            self.map[t].add(index - 1)

    def tracksetentry(self, i, j, value):
        """
        if
        #如果第j列在self.key中
        #如果i,j entry 是None:
            直接加入对应set中，没有新建一个key和value(set结构的)加进去
        else：
            #从self.keymap中删除第irow的key
            #把删除的key的第i项换成value重新做成tuple，装进self.keymap中
        """
        attname = self.table.array2d[0][j]
        if self.table.array2d[i][j] == value:
            return
        if attname in self.group:
            r = []
            for s in self.group:
                if s == attname:
                    r.append(value)
                else:
                    r.append(self.table.array2d[i][self.table.colmap[s]])
            newt = tuple(r)
            oldt = tuple(self.table.getlist(i, self.group))
            if oldt in self.map:
                self.map[oldt].remove(i)
                if len(self.map[oldt]) == 0:
                    del self.map[oldt]
            if newt in self.map:
                self.map[newt].add(i)
            else:
                self.map[newt] = {i}
