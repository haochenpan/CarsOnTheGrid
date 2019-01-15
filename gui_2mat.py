import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.animation as animation
from matplotlib.widgets import Button
import matplotlib.text
import numpy as np
import gui_2lib
import run_helplib
import run_main
import pprint
import types
import config
import pickle
import time

pause = True

idx = 0
ctr1, ctr2 = 0, 0


def on_click(event):
    print("pressed")
    global pause
    pause ^= True


def gen():
    global idx, ctr1
    while idx < len(offsets):
        # time.sleep(0.1)
        # print("gen called", ctr1)
        ctr1 += 1
        yield idx
        if not pause:
            idx += 1
            # idx = idx % len(offsets)


def _update(idx):
    global ctr2
    # print("update called", ctr2)
    ctr2 += 1
    scat.set_offsets(offsets[idx])


def get_plt():
    """
    Get the plotting "canvas" with row, col axes and grid lines
    :return:
    """
    fig = plt.figure(figsize=(10, 10))
    # fig.canvas.mpl_connect('button_press_event', on_click)

    # draw axis
    ax = fig.add_subplot(111, xlim=[config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX + 1],
                         ylim=[config.LAST_COL_INDEX + 1, config.FIRST_COL_INDEX])
    ax.grid(b=True)
    ax.xaxis.tick_top()
    ax.set_xticks(np.arange(config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX + 1, 1))
    ax.set_yticks(np.arange(config.FIRST_COL_INDEX, config.LAST_COL_INDEX + 1, 1))

    # shift labels
    # https://stackoverflow.com/questions/28615887/how-to-move-a-ticks-label-in-matplotlib
    shift = -0.5  # Data coordinates
    for lbl in ax.xaxis.get_majorticklabels():
        lbl.customShiftValue = shift
        lbl.set_x = types.MethodType(lambda self, x: matplotlib.text.Text.set_x(self, x - self.customShiftValue), lbl)

    for lbl in ax.yaxis.get_majorticklabels():
        lbl.customShiftValue = shift
        lbl.set_y = types.MethodType(lambda self, y: matplotlib.text.Text.set_y(self, y - self.customShiftValue), lbl)

    return plt, fig


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)
    g, b = run_main.run()
    # with open('g.pickle', 'rb') as handle:
    #     g, b = pickle.load(handle)

    pos_tbl = gui_2lib.get_plotting_pos_tbl(g)
    ls_tbl = gui_2lib.get_ls_tbl(pos_tbl)
    stack_tbl = gui_2lib.get_stack_tbl(ls_tbl)

    offsets = stack_tbl[0]
    # for each in pos_tbl[0]:
    #     print(each)
    # print()
    # print()
    # print()
    # for each in offsets:
    #     print(each[0])

    # ctr_dict = defaultdict(lambda: 0)
    # for each in pos_tbl[0]:
    #     ctr_dict[(int(each[0]), int(each[1]))] += 1
    # for k, v in ctr_dict.items():
    #     print(k, v)

    # print(pos_tbl[0][2], pos_tbl[1][2])
    # print(ls_tbl[0][2])

    x, y = [], []
    for xc, yc in pos_tbl[0]:
        # print(xc, yc)
        x.append(xc)
        y.append(yc)

    plt, fig = get_plt()
    scat = plt.scatter(x, y)
    scat.set_alpha(0.8)

    anim = animation.FuncAnimation(fig, _update, gen, blit=False, interval=5, repeat=False)
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(on_click)
    plt.show()
