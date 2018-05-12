import os

path = os.getcwd()
print(path)


for filename in os.listdir():
    info = os.stat(filename)
    print(info.st_creator)

#print(type(os.listdir(path)[0]))


#os.system("bash")
