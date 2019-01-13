import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np
import pickle
import time
import gui2lib
import pprint

# fig = plt.figure(figsize=(10, 10))
# # fig.canvas.mpl_connect('button_press_event', on_click)
# ax = fig.add_subplot(111, xlim=[-1, 11], ylim=[11, -1])
# ax.xaxis.tick_top()
# ax.set_xticks(np.arange(-1, 12, 1))
# ax.set_yticks(np.arange(-1, 12, 1))

pp = pprint.PrettyPrinter(indent=2)
with open('g.pickle', 'rb') as handle:
    g, b = pickle.load(handle)
t = gui2lib.get_plotting_pos_tbl(g)
t = np.asarray(t[0])
# t.reshape(100, 2)
# pp.pprint(t)

# x = np.split(t[0], 2, axis=0)
# print(x)
# pp.pprint(t)
# print(len(t))
