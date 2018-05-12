
from random import*

def generate(gold):
    return 100*gold*+random()*20

k = 200
golds = [random()*100 for i in range(k)]


score = [generate(gold) for gold in golds]


for i in range(k):
    print(score[i])

print("==================")

for i in range(k):
    print(golds[i])
