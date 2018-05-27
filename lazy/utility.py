
def inilist(n, s=None):
    if isinstance(s, str):
        s = "\'" + s + "\'"
    return eval("[" + ",".join([str(s)] * n) + "]")

def inilist2d(i,j, s=None):
    if isinstance(s, str):
        s = "\'" + s + "\'"
    result=[eval("[" + ",".join([str(s)] * j) + "]") for k in range(i)]
    return result

def pdict(d, n=None, sep=""):
    ident = "   "
    for key in d:
        keystr = str(key) + ":" + sep
        length = len(keystr)
        print(keystr, end="")
        if isinstance(d[key], Table):
            print("\n" + ident + str(d[key]).replace("\n", "\n" + ident))
        if isinstance(d[key], list):
            if isinstance(d[key][0], list):
                print(d[key][0])
                indent = (len(key) + 1) * " "
                for i in range(1, len(d[key])):
                    print(indent + str(d[key][i]))
            else:
                s = str(d[key])
                pre = 0
                c = 0
                for i in range(len(s)):
                    if c == n:
                        out = s[pre:i]
                        if pre != 0 or sep == '\n':
                            out = " " * length + out
                        print(out)
                        pre = i
                        c = 0
                    if s[i] == ',':
                        c += 1
                out = " " * length + s[pre:]
                print(out)


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
    result =[]
    for v in ls:
        result+=v
    return result

def wid(t):
    return len(t.array2d[0])