import inspect
import sys
from lzpy import*

def ack(*args):
    stack=inspect.stack()
    f = stack[2][0].f_globals[stack[1][3]]
    
    ano = f.__annotations__
    names=f.__code__.co_varnames
    num=f.__code__.co_argcount
    ht=Table([["name","value","vartype","valuetype","match"]])
    for i in range(num):
        name=names[i]
        arg = args[i]
        vartype=ano[names[i]]
        valtype=type(arg)
        match = vartype==valtype
        ht.append([name,arg,vartype,valtype,match])

    tail = ")->"+ano["return"].__name__ 
    hinter=f.__name__+"("+",".join([":".join([ht[i]["name"],ht[i]["vartype"].__name__]) for i in range(1,len(ht)+1)])+tail
    passer=f.__name__+"("+",".join([":".join([str(ht[i]["value"]),ht[i]["valuetype"].__name__]) for i in range(1,len(ht)+1)])+tail
    for i in range(num):
        hint = ano[names[i]]
        if not isinstance(args[i],hint):
            es = "\n".join(["",hinter,passer,str(ht)])
            raise Exception(es)
    return 


def rck(*args):
    #print(args)
    stack=inspect.stack()
    f = stack[2][0].f_globals[stack[1][3]] 
    
    #print()
    ht=Table([["name","value","vartype","valuetype","match"]])
    names=f.__code__.co_varnames
    ano = f.__annotations__
    num=f.__code__.co_argcount
        
    name="return"
    if len(args)== 0:
        arg = None
    elif len(args) == 1:
        arg = args[0]
    else:
        raise Exception("not support multiple return yet")
    vartype = ano[name] 
    valtype = type(arg) if vartype is not None else None
    match = vartype==valtype
    ht.append([name,arg,vartype,valtype,match])
    #build str


    head = f.__name__+"(..)->"
    hinter=head + ano["return"].__name__
    passer=head + str(arg)


    if not match:
        es = "\n".join(["",hinter,passer,str(ht)])
        raise Exception(es)
    return arg
    
# multi return value check
# 一种优质的docstring
# more details of function.__code__.

