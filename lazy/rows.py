from .row import Row


class Rows(list):

    def __init__(self, table, indices):
        self.table = table
        self.indices = indices
        list.__init__(self, [Row(table,index) for index in indices])

    def __getitem__(self, colkey):
        if isinstance(colkey, int):
            l = []
            for row in self:
                l.append(row[colkey])
            return l
        elif isinstance(colkey, str):
            index = self.table.getcolindex(colkey)
            return super().__getitem__(index)
        elif isinstance(colkey, slice):
            start = colkey.start if colkey.start is not None else 0
            stop = colkey.stop+1 if colkey.stop is not None else len(self)+1
            return super().__getitem__(slice(start,stop))
        elif isinstance(colkey, tuple) or isinstance(colkey, list):
            result = []
            for i in range(len(colkey)):
                index = self.table.getcolindex(colkey[i])
                result.append(super().__getitem__(index))
            return result

    def _set(self, colkey, value):
        if isinstance(colkey, int):
            index = colkey
            super().__setitem__(index, value)
            self.table.setentry(self.index, index, value)
        elif isinstance(colkey, str):
            index = self.table.getcolindex(colkey)
            super().__setitem__(index, value)
            self.table.setentry(self.index, index, value)
        elif isinstance(colkey, slice):
            start = 0 if colkey.start is None else colkey
            stop = len(self) if colkey.stop is None else colkey.stop
            for i in range(start, stop+1):
                super().__setitem__(i,value[i])
                self.table.setentry(self.index, i, value[i])
        elif isinstance(colkey, tuple) or isinstance(colkey, list):
            for i in range(len(colkey)):
                index = self.table.getcolindex(colkey[i])
                super().__setitem__(index, value[i])
                self.table.setentry(self.index, i, value[i])

    def __setitem__(self, key, value):
        self._set(key, value)

    def __delitem__(self, key):
        self._set(key, None)