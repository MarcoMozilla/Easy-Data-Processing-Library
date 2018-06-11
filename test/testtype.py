import sys
sys.path.append('..')
from lazy import *
from pprint import*



ls=[bool,tuple,int,float,eval]


def boolof(s):
    booldict = {"True":True,"False":False}
    if s == "" or s=="None":
        return None
    else:
        try:
            return booldict[s]
        except:
            raise Exception("\'{}\' cannot cast to int".format(s))
        
def intof(s):
    if s == "" or s=="None":
        return None
    else:
        try:
            return int(s)
        except:
            raise Exception("\'{}\' cannot cast to int".format(s))


def floatof(s):
    if s == "" or s=="None":
        return None
    else:
        try:
            return float(s)
        except:
            raise Exception("\'{}\' cannot cast to int".format(s))

def strof(s):
    if s == "" or s=="None":
        return None
    else:
        return s





