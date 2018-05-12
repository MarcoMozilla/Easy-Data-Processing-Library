import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot(111)

x = np.random.normal(0,1,1000)
numBins = 50
ax.hist(x,numBins,facecolor='green',labels = True,alpha=0.8)
plt.show()
