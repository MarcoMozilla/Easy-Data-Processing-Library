from .utility import*

class Rows:
    # behave all like a list and return list except get,set, del

    def __init__(self, table, indices):
        self.table = table
        self.indices = indices
        #self.array = table.array2d[index]
        self.array2d =[]
        for i in indices:
            self.array2d.append(table.array2d[i])


    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key,str):
            j = None
            if isinstance(key,int):
                j = self.table._recapcolindex(key)
            elif isinstance(key,str):
                self.table._REatri(key)
                j = self.table.colmap[key]
            return [self.table.array2d[i][j] for i in self.indices]
        elif isinstance(key, slice) or isinstance(key, tuple) or isinstance(key, list):
            ls = None
            if isinstance(key, slice):
                #down or up index may modify
                sindex = 0 if key.start is None else key.start
                eindex = wid(self.table)-1 if key.stop is None else key.stop
                sindex = self.table._recapcolindex(sindex)
                eindex = self.table._recapcolindex(eindex)
                ls = list(range(sindex, eindex+1))
            elif isinstance(key, tuple) or isinstance(key, list):
                ls = []
                for v in key:
                    if isinstance(v, str):
                        ls.append(self.table.colmap[v])
                    elif isinstance(v, int):
                        ls.append(self.table._recapcolindex(v))
            result = []
            for i in self.indices:
                sub = [self.table.array2d[i][j] for j in ls]
                result.append(sub)
            return result

            pass

    def __setitem__(self, key, value):
        if isinstance(key, int) or isinstance(key,str):
            j = None
            if isinstance(key,int):
                j = self.table._recapcolindex(key)
            elif isinstance(key,str):
                self.table._REatri(key)
                j = self.table.colmap[key]
            # set item
            if isinstance(value,list):
                #array set
                if len(value) == len(self.indices):
                    for k in range(len(value)):
                        self.table.setentry(self.indices[k],j,value[k])
                else:
                    raise Exception("length not map")
            else:
                #value set
                for i in self.indices:
                    self.table.setentry(i,j,value)


        elif isinstance(key, slice) or isinstance(key, tuple) or isinstance(key, list):
            ls = None
            if isinstance(key, slice):
                #down or up index may modify
                sindex = 0 if key.start is None else key.start
                eindex = wid(self.table)-1 if key.stop is None else key.stop
                sindex = self.table._recapcolindex(sindex)
                eindex = self.table._recapcolindex(eindex)
                ls = list(range(sindex, eindex+1))
            elif isinstance(key, tuple) or isinstance(key, list):
                ls = []
                for v in key:
                    if isinstance(v, str):
                        ls.append(self.table.colmap[v])
                    elif isinstance(v, int):
                        ls.append(self.table._recapcolindex(v))
            #set item
            if isinstance(value, list):
                #check length
                if isinstance(value[0],list):
                    if len(value) == len(self.indices):
                        #set 2d-array
                        #check width
                        for r in value:
                            if not (isinstance(r,list) or isinstance(r,tuple)):
                                raise Exception("only sub list or sub tuple is supported")
                            if len(r) != len(ls):
                                raise Exception("width not map")
                        for i in range(len(value)):
                            for j in range(len(value[0])):
                                self.table.setentry(self.indices[i],ls[j],value[i][j])
                    else:
                        raise Exception("length not map or wid")

                else:
                    if len(value) == len(ls):
                        #set array
                        for i in range(len(self.indices)):
                            for j in range(len(ls)):
                                self.table.setentry(self.indices[i],ls[j],value[j])
                    else:
                        raise Exception("width not map")
            else:
                for i in self.indices:
                    for j in ls:
                        self.table.setentry(i,j,value)

    def __delitem__(self, key):
        self.__setitem__(key,None)

    def __iter__(self):
        return iter(self.array2d)

    def __next__(self):
        return next(self.array2d)

    def copy(self):
        result =[]
        for r in self.array2d:
            result.append(r.copy())
        return result

    def __str__(self):
        return str(self.array2d)

    def __repr__(self):
        return repr(self.array2d)

    def __len__(self):
        return len(self.array2d)





