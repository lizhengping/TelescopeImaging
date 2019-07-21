__author__ = 'benlz'

#from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt

# the following line only works in an IPython notebook
#%matplotlib notebo

# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 6))
mpl.rc('image', cmap='gray')

import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience

import pims
import trackpy as tp

frames = pims.ImageSequence('2.jpg', as_grey=True)
print(frames)
plt.imshow(frames[0])
#plt.show()
#f = tp.locate(frames[0], 101, invert=True)
f = tp.locate(frames[0], 101, engine='python')
print(f.head())
plt.figure()  # make a new figure
tp.annotate(f, frames[0], plot_style=dict(marker='x'))
plt.show()
#features = tp.locate(bins_1.jpg,