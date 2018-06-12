from .utility import*


class Row:
    # behave all like a list and return list except get,set, del

    def __init__(self, table, index):
        self.table = table
        self.index = index
        self.array= table.array2d[index]

    def __getitem__(self, key):
        if isinstance(key,int) or isinstance(key,str):
            j = None
            if isinstance(key,int):
                j = self.table._recapcolindex(key)
            elif isinstance(key,str):
                j = self.table.colmap[key]
            return self.array[j]
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
            #print(ls)
            return [self.array[j] for j in ls]


    def __setitem__(self, key, value):
        if isinstance(key,int) or isinstance(key,str):
            j = None
            if isinstance(key,int):
                j = self.table._recapcolindex(key)
            elif isinstance(key,str):
                j = self.table.colmap[key]
            self.table.setentry(self.index,j,value)
        elif isinstance(key, slice) or isinstance(key, tuple) or isinstance(key, list):
            ls = None
            if isinstance(key, slice):
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
            #print(ls)
            #array object
            if isinstance(value, list):
                if len(value) == len(ls):
                    for k in range(len(value)):
                        self.table.setentry(self.index, ls[k],value[k])
                else:
                    raise Exception("width not map")
            else:
                for j in ls:
                    self.table.setentry(self.index, j, value)
            
            #set value
                        
    def __delitem__(self, key):
        self.__setitem__(key, None)


    def __iter__(self):
        return iter(self.array)

    def __next__(self):
        return next(self.array)

    def copy(self):
        return self.array.copy()

    def __str__(self):
        return str(self.array)

    def __repr__(self):
        return repr(self.array)

    def __len__(self):
        return len(self.array)