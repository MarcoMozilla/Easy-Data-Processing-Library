def change(rfilename,old,new,wfilename):
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
    #change(" .py","head","colmap"," .py")
    
    pass
