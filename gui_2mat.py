import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import matplotlib.text
import numpy as np
import pickle
import time
import gui_2lib
import run_helplib
import pprint
import types


def get_plt():
    fig = plt.figure(figsize=(10, 10))
    # fig.canvas.mpl_connect('button_press_event', on_click)

    # draw axis
    ax = fig.add_subplot(111, xlim=[0, 10], ylim=[10, 0])
    ax.grid(b=True)
    ax.xaxis.tick_top()
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 10, 1))

    # shift labels
    # https://stackoverflow.com/questions/28615887/how-to-move-a-ticks-label-in-matplotlib
    shift = -0.5  # Data coordinates
    for lbl in ax.xaxis.get_majorticklabels():
        lbl.customShiftValue = shift
        lbl.set_x = types.MethodType(lambda self, x: matplotlib.text.Text.set_x(self, x - self.customShiftValue), lbl)

    for lbl in ax.yaxis.get_majorticklabels():
        lbl.customShiftValue = shift
        lbl.set_y = types.MethodType(lambda self, y: matplotlib.text.Text.set_y(self, y - self.customShiftValue), lbl)

    return plt


pp = pprint.PrettyPrinter(indent=2)
# with open('g.pickle', 'rb') as handle:
#     g, b = pickle.load(handle)
g, b = run_helplib.init_the_grid()
t = gui_2lib.get_plotting_pos_tbl(g)
x, y = [], []
for xc, yc in t[0]:
    # print(xc, yc)
    x.append(xc)
    y.append(yc)
scat = get_plt().scatter(x, y)
scat.set_alpha(0.8)
run_helplib.report_grid_intermediate(g, b, 0, False)
plt.show()
