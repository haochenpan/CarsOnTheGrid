"""
    GUI of CarsOnTheGrid problem
"""
from types import MethodType
from pprint import PrettyPrinter
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.text
import numpy as np
import main
import config
import helplib

forward = True
round_idx = 0  # init
frame_idx = 0
frames = []
global_state_ctr = 0


def on_click_next(event):
    global forward, global_state_ctr
    global_state_ctr += 1
    forward = True


def on_click_prev(event):
    global forward, global_state_ctr
    global_state_ctr += 1
    forward = False


def gen():

    global forward, round_idx, frame_idx, global_state_ctr
    local_state_ctr = 0

    while True:
        yield frame_idx
        if global_state_ctr > local_state_ctr:
            if forward:
                if round_idx == config.NUM_OF_MOVES - 1:
                    print("fwd long dist!")
                    round_idx, frame_idx = 0, 0
                else:
                    if frame_idx > 0:
                        round_idx += 1
                        frame_idx = 0
                    while frame_idx < config.FRAMES - 1:
                        frame_idx += 1
                        yield frame_idx
            else:
                if frame_idx == 0:
                    print("bck long dist!")
                    round_idx = config.NUM_OF_MOVES - 1
                    frame_idx = config.FRAMES - 1
                else:
                    while frame_idx > 0:
                        frame_idx -= 1
                        yield frame_idx
                    if round_idx == 0:
                        pass
                    else:
                        round_idx -= 1
                        frame_idx = config.FRAMES - 1

            assert frame_idx in {0, config.FRAMES - 1}
            local_state_ctr += 1
            print(round_idx, frame_idx)


def _update(foo):
    print(foo)
    scat.set_offsets(frames[round_idx][frame_idx])


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
        lbl.set_x = MethodType(lambda self, x:
                               matplotlib.text.Text.set_x(self, x - self.customShiftValue), lbl)

    for lbl in ax.yaxis.get_majorticklabels():
        lbl.customShiftValue = shift
        lbl.set_y = MethodType(lambda self, y:
                               matplotlib.text.Text.set_y(self, y - self.customShiftValue), lbl)

    return plt, fig


if __name__ == '__main__':
    pp = PrettyPrinter(indent=2)
    g, b = main.run()

    pos_tbl = helplib.get_plotting_pos_tbl(g)
    ls_tbl = helplib.get_ls_tbl(pos_tbl)
    stack_tbl = helplib.get_stack_tbl(ls_tbl)
    # offsets = stack_tbl[0]

    frames = stack_tbl
    print(len(frames))
    print(len(frames[0]))
    x, y = [], []
    for xc, yc in pos_tbl[0]:
        # print(xc, yc)
        x.append(xc)
        y.append(yc)

    plt, fig = get_plt()
    scat = plt.scatter(x, y)
    scat.set_alpha(0.8)

    anim = animation.FuncAnimation(fig, _update, gen, blit=False, interval=5, repeat=False)
    axprev = plt.axes([0.8, 0, 0.1, 0.075])
    axnext = plt.axes([0.9, 0, 0.1, 0.075])
    bprev = Button(axprev, 'Prev')
    bnext = Button(axnext, 'Next')
    bprev.on_clicked(on_click_prev)
    bnext.on_clicked(on_click_next)
    plt.show()
