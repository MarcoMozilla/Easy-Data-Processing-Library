import string
from pprint import *

def inilist(n, s=None):
    return [s for i in range(n)]


def inilist2d(i, j, s=None):

    return [[s for x in range(j)] for y in range(i)]


def slist(s, sep=","):
    s = s.split(sep)
    return [v.strip() for v in s]


def isnum(s):

    try:
        s = int(s)
        if isinstance(s, int):
            print(s)
            return True
    except:
        pass
    try:
        s = float(s)
        if isinstance(s, float):
            return True
    except:
        pass
    return False


def valueof(s):
    if s == "True" or s == "False" or s == "None":
        return eval(s)
    if s == "":
        return None
    try:
        s = int(s)
        return s
    except:
        try:
            s = float(s)
            return s
        except:
            return s


def decomp1(s):
    l = s.split("=")
    for i in range(len(l)):
        l[i] = slist(l[i])
    return l


def decomp2(s):
    l = s.split(",")
    for i in range(len(l)):
        l[i] = slist(l[i], "=")
    t = [[], []]
    for v in l:
        t[0].append(v[0])
        t[1].append(v[1])
    return t


def decomp(s):
    if s.count("=") == 1:
        return decomp1(s)
    else:
        return decomp2(s)


def rotlist12(ls):
    return [[v] for v in ls]


def rotlist21(ls):
    result = []
    for v in ls:
        result += v
    return result


def wid(t):
    return len(t.array2d[0])


def strsep2list(s, sep='\n', limit=None):
    result = []
    i = 0
    n = len(s)
    sub = ""
    mlen = 0
    while i < n:
        if s[i] not in string.printable:
            mlen += 2
        else:
            mlen += 1
        sub +=s[i]
        if s[i] == '\n':
            result.append(sub[:-1])
            sub = ""
            mlen = 0
        elif s[i] == sep:
            result.append(sub)
            sub = ""
            mlen = 0
        elif mlen > limit:
            result.append(sub[:-1])
            sub = ""
            mlen = 0
            i-=1
        elif mlen == limit:
            result.append(sub)
            sub = ""
            mlen = 0
        elif i == len(s) - 1:
            result.append(sub)
            sub = ""
            mlen = 0
        else:
            pass

        i += 1
    #print("result = ")
    #pprint(result)
    return result



def clen(s):
    result = 0
    for i in range(len(s)):
        if s[i] not in string.printable:
            result += 2
        else:
            result += 1
    return result

def strsep2maxlen(s, sep='\n'):
    result = 0
    i = 0
    n = len(s)
    length = 0
    while i < n:
        if s[i] not in string.printable:
            adding = 2
        else:
            adding = 1
        length += adding
        if s[i] == '\n':
            sub = length - 1
            result = max(result, sub)
            length = 0
        elif s[i] == sep:
            sub = length
            result = max(result, sub)
            length = 0
        elif i == len(s) - 1:
            sub = length
            result = max(result,sub)
            length = 0
        i += 1
    return result


def maxlen(v, sep='\n'):
    if isinstance(v, str):
        return strsep2maxlen(v, sep)
    else:
        return len(str(v))


def boolof(s):
    booldict = {"True": True, "False": False}
    if s == "" or s == "None":
        return None
    else:
        try:
            return booldict[s]
        except:
            raise Exception("\'{}\' cannot cast to int".format(s))


def intof(s):
    if s == "" or s == "None":
        return None
    else:
        try:
            return int(s)
        except:
            raise Exception("\'{}\' cannot cast to int".format(s))


def floatof(s):
    if s == "" or s == "None":
        return None
    else:
        try:
            return float(s)
        except:
            raise Exception("\'{}\' cannot cast to int".format(s))


def strof(s):
    if s == "" or s == "None":
        return None
    else:
        return s