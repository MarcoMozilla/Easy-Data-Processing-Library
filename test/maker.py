

def make():
    s="""def f():
    print("ok")
    return

    k = f
    """

    exec(s)
    return eval("f")



f = make()
f()