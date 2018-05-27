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
    if isnum(s) or s == "True" or s == "False" or s == "None":
        return eval(s)
    elif s == "":
        return None
    else:
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
    c = 0
    i = 0
    n = len(s)
    while i < n:
        if s[i] == '\n':
            sub = s[c:i]
            result.append(sub)
            #print("case2:",result)
            c = i + 1
        elif s[i] == sep:
            sub = s[c:i + 1]
            result.append(sub)
            #print("case1:", result)
            c = i + 1

        elif limit != None and i - c + 1 == limit:
            sub = s[c:i + 1]
            result.append(sub)
            #print("case3:",result)
            c = i + 1
        elif i == len(s) - 1:
            sub = s[c:i + 1]
            result.append(sub)
            #print("case4",result)
        i += 1
    return result


def strsep2maxlen(s, sep='\n'):
    result = 0
    c = 0
    i = 0
    n = len(s)
    while i < n:
        if s[i] == '\n':
            sub = i - c
            result = max(result, sub)
            c = i + 1
        elif s[i] == sep:
            sub = i-c+1
            result = max(result, sub)
            c = i + 1
        elif i == len(s) - 1:
            sub = i - c + 1
            result = max(result,sub)
        i += 1
    return result


def maxlen(v, sep='\n'):
    if isinstance(v, str):
        return strsep2maxlen(v, sep)
    else:
        return len(str(v))
