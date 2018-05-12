import csv
with open('country.csv') as csvfile:
    lines = csv.reader(csvfile, delimiter=',', quotechar='\'')
    G = (row for row in lines)
    print(next(G))
    for g in G:
        print(g)




