import matplotlib.pyplot as plt


def m(t):
    return [v/255 for v in t]

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0.01, 0.01, 0.01, 0.01)  # only "explode" the 2nd slice (i.e. 'Hogs')


c = [(25,25,25,255),(50,50,50,255),(100,100,100,255),(200,200,200,255)]
flc = [m(t) for t in c]
prop = {'linewidth': 2}

#print(flc)
plt.rcParams['lines.linewidth'] = 2
fig1, ax1 = plt.subplots()


ax1.pie(sizes, explode=explode,colors =flc, labels=labels, autopct='%1.1f%%',
        wedgeprops=prop)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#plt.rcParams['patch.edgecolor'] = m([0,0,0])
plt.show()
