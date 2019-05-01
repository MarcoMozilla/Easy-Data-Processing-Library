import json
import pprint
import time

class Node(dict):
    def __new__(cls,data):
        if isinstance(data,list):
            return [Node(e) for e in data]
        if type(data) == dict:
            return super(Node, cls).__new__(cls)
        else:
            return data
        
    def __init__(self,data):
        res = {}
        for key in data:
            res[key] = Node(data[key])
        super().__init__(res)
        self.__dict__=self

    def __add__(self,other):
        n = self & other
        if n != {}:
            raise Exception(str(n))
        res = {}
        for key in self:
            res[key] = self[key]
        for key in other:
            res[key] = other[key]
        return Node(res)

    def __or__(self, other):
        xor = self ^ other # in self or in other
        n = self & other # in self and in other
        res = {}
        for key in xor:
            res[key] = xor[key]
        for key in n:
            res[key] = n[key]
        return Node(res)

    def __and__(self, other):
        res = {}
        a = self
        b = other
        if len(other)<len(self):
            a,b = other,self
        for key in a:
            if key in b:
                if a[key] != b[key]:
                    res[key] = {"0":a[key],"1":b[key]}
                else:
                    res[key] = a[key]
        return Node(res)

    def __xor__(self, other):
        res = {}
        for key in self:
            if not key in other:
                res[key] = self[key]
        for key in other:
            if not key in self:
                res[key] = other[key]
        return Node(res)

    def __sub__(self, other):
        res = {}
        for key in self:
            if not key in other:
                res[key] = self[key]
        return Node(res)

    union = __or__
    intersect = __and__
    minus = __sub__

class Root:

    precision = 2

    def __init__(self,body,name=None):
        self.body  = Node(body)
        self.name = name

    def __str__(self):
        heads = "Root<{}>:\n".format(self.name)
        return heads+pprint.pformat(self.body)

    def __repr__(self):
        return str(self)

    def read(name):
        t1 = time.time()
        fname = name + ".json"
        with open(fname, "r") as read_file:
            k = json.load(read_file)
        t2 = time.time()
        res = Root(k,name)
        t3 = time.time()
        print("READ <{}> FROM {} takes {} + {}".format(name, fname, round(t2 - t1, Root.precision),round(t3 - t2, Root.precision)))
        return res

    def save(self,name=None,show=True):
        if name is not None:
            self.name=name
        if self.name is None:
            raise Exception("Dont have name yet")
        t1 = time.time()
        fname = self.name+".json"
        with open(fname, "w") as write_file:
            write_file.write(str(self.body).replace("\'", "\""))
        t2 = time.time()
        if show:
            print("SAVE <{}> TO {} takes {}".format(self.name, fname,round(t2-t1,Root.precision)))
        return



