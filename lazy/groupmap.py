from pprint import *

class Groupmap:

    def __init__(self,table,group):
        self.table = table
        #origin table class
        
        self.group = group
        #the primary key of table colon
        #such as [0,2] 表示 table的第0列，和第2列合起来是一个key
        
        self.groupmap = {}
        #initialize the self.keymap at here
        #such as {(1,"A"):{7,8,9}, (2,"B"):{5}}
        #注意value 是set！！！
        #表示 在Table中 第0栏是1 第2栏是"A"的row是第7,8,9行
        #               第0栏是1 第2栏是"B"的row是第5行
        #其中的key可以是单个或多个值，如果是单个值也是用tuple表示（1,)
        pass

    def __str__(self):
        sdict = {"group":tuple([self.table[0][i] for i in self.group]), "groupmap":self.groupmap}
        return pformat(sdict)

    def trackaddrow(self,i):
        #从table中找到第 i row，
        #从第i row到第len(self)row (包括首尾)的
        #self.groupmap中找到value（是一个set），一边从set中删除，一边+1放回到set中
        #

    def tackdelrow(self,i):
        #从self.groupmap中的对应set中删除第 i-th row 
        #在self.keymap中 第ith row一直到末尾所有的key全部减一



    def tacksetentry(self,i,j,value):
        """
        #如果第j列在self.key中
        #如果i,j entry 是None:
            直接加入对应set中，没有新建一个key和value(set结构的)加进去
        else：
            #从self.keymap中删除第irow的key
            #把删除的key的第i项换成value重新做成tuple，装进self.keymap中
        
        """

    pass
    #注意了解Table class 和google doc上的介绍
    #可能我有没有考虑到的case，记得提醒我！！！
    #可能有其他的function









        
        
    
