

class A:

    def __init__(self):
        self.__dict__ ={"a":1,"b":2,"c":3}
        self.map= {}


    #def __getattr__(self, name):
    #    return self.__dict__[name]

    #def __setattribute__(self,name,value):
    #    self.__dict__[name] = value


k = A()




    
