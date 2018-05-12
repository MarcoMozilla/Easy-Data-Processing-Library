


class A:

    def __init__(self,s):
        self.i= s
        
        

    def __getitem__(self,key):
        if type(key) is slice:
            print(key.start)
            print(key.stop)
            print(key.step)
        else:
            print(key)


a = A(list([1,2,3,4,5,6]))







class B:

    def __getitem__(self,key):
        return key

a=B()





