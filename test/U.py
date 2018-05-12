def change(rfilename,wfilename,old,new):
    wfile = open(wfilename,"w")
    rfile = open(rfilename,"r")

    line = "something"
    while line!="":
        line = rfile.readline()
        line = line.replace(old,new)
        wfile.write(line)
    wfile.close()
    rfile.close()
    


if  __name__ == "__main__":
    change("t12.csv","t13.csv",",,",",",)
    
    pass
