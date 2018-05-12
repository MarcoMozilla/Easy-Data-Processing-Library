

class A(list):


    def __init__(self,l):
        list.__init__(self,l)




l = [[1,2,3,4,5,6],[1]]
a = A(l)

