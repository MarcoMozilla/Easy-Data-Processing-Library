from random import*
from string import ascii_letters
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
n = 2
k = 100
values=[int(random()*10)*10 for i in range(n)]

labels=[choice(ascii_letters) for i in range(n)]

ax = plt.subplot(projection="polar")
ax.bar(labels,values,facecolor='green',edgecolor = "yellowgreen")
plt.show()
