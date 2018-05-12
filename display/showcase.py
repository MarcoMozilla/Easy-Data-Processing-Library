from Table import *

k =100
g=5
f= 1
t = [
    ["name","grade","IQ","color"],
    ["moka",round(random()*k,g),200*f,"grey"],
    ["sasa",round(random()*k,g),150*f,"pink"],
    ["kadi",round(random()*k,g),80*f,"red"],
    ["maki",round(random()*k,g),75*f,"yello"],
    ["xido",round(random()*k,g),60*f,"grey"],
    ["wade",round(random()*k,g),30*f,"blue"],
    ["cida",round(random()*k,g),100*f,"purple"],
    ]
t = Table(t)
t.save("student")

#t.plot("name","IQ")


"""
for i in range(100):
    ln.append(["cida",round(random()*k,g),int(random()*10)*f,"red"])
"""
