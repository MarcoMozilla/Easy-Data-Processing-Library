from pprint import *

class Keymap:

    def __init__(self,table,key):
        self.table = table
        #origin table class
        
        self.key = key
        #the primary key of table colon
        #such as [0,2] 表示 table的第0列，和第2列合起来是一个key
        
        self.keymap = {}
        #initialize the self.keymap at here
        #such as {(1,"A"):7, (2,"B"):5}
        #表示 在Table中 第0栏是1 第2栏是"A"的row是第7行
        #               第0栏是1 第2栏是"B"的row是第5行
        #并检查准备加入和row中的key是否已经出现
        #如果出现则raise exception
        #其中的key可以是单个或多个值，如果是单个值也是用tuple表示（1,)
        pass

    def __str__(self):
        sdict = {"key":tuple([self.table[0][i] for i in self.key]), "keymap":self.keymap}
        return pformat(sdict)

    def trackaddrow(self,i):
        #从table中找到第 i row，
        #从第i row到第len(self)row (包括首尾)的
        #key （在self.keymap中）全部加1

    def tackdelrow(self,i):
        #从self.keymap中删除第 i row 的key
        #在self.keymap中 第irow一直到末尾所有的key全部减一



    def tacksetentry(self,i,j,value):
        """
        #如果第j列在self.key中，而且加入value之后所有key不为None
        #如果加入的value使第ith row和self.keymap中的key重复且
        self.keymap[key] != i, raise exception
        #如果i,j entry 是None:
            直接加入keymaps
        else：
            #从self.keymap中删除第irow的key
            #把删除的key的第i项换成value重新做成tuple，装进self.keymap中
        
        """

    #注意了解Table class的架构，和google doc上的介绍
    #可能我有没有考虑到的case，记得提醒我！！！
    #可能会补充其他的后续function







        
        
    
