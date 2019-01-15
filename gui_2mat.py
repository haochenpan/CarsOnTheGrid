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
forward = True
round_idx = 0  # init
frame_idx = 0
frames = []
idx = 0
ctr1, ctr2 = 0, 0
global_state_ctr = 0


def on_click_next(event):
    global pause, forward
    global round_idx, frame_idx
    global global_state_ctr
    # if pause:
    #     print("pressed")
    #     pause = False
    #     forward = True
    global_state_ctr += 1
    forward = True


def on_click_prev(event):
    global pause, forward
    global round_idx, frame_idx
    global global_state_ctr
    # if pause:
    #     pause = False
    #     forward = False
    global_state_ctr += 1
    forward = False


def gen():
    global pause, round_idx, frame_idx
    for i in range(config.NUM_OF_MOVES):
        while frame_idx < gui_2lib.frames - 1:
            if not pause:
                frame_idx += 1
            yield frame_idx
        pause = True
        round_idx += 1
        frame_idx = 0


def gen2():
    global pause, forward
    global round_idx, frame_idx, ctr1, ctr2
    while True:
        if forward:
            while frame_idx < gui_2lib.frames - 1:
                if not pause:
                    frame_idx += 1
                print("fwd", ctr1, round_idx, frame_idx)
                ctr1 += 1
                yield frame_idx
                if not forward:
                    print("bk", round_idx, frame_idx)
                    break
            else:
                pause = True
                round_idx += 1
                frame_idx = 0
        else:
            print(round_idx, frame_idx)
            # if pause:
            #     print("already paused!")
            round_idx -= 1
            frame_idx = gui_2lib.frames - 1
            print(round_idx, frame_idx)
            while frame_idx >= 0:
                if not pause:
                    frame_idx -= 1
                print("bwd", ctr2, round_idx, frame_idx)
                ctr2 += 1
                yield frame_idx
                if forward:
                    break
            else:
                pause = True
                round_idx -= 1
                frame_idx = gui_2lib.frames - 1


def gen3():
    global pause, forward
    global round_idx, frame_idx, ctr1, ctr2
    local_state_ctr = 0
    while True:
        yield frame_idx
        if global_state_ctr > local_state_ctr:
            if forward:
                while frame_idx < gui_2lib.frames - 1:
                    frame_idx += 1
                    yield frame_idx
                if round_idx < config.NUM_OF_MOVES:
                    round_idx += 1
                    frame_idx = 0
                else:
                    frame_idx -= 1
            else:
                round_idx -= 1
                frame_idx = gui_2lib.frames - 1
                while frame_idx > 0:
                    frame_idx -= 1
                    yield frame_idx
            print(round_idx, frame_idx)
            local_state_ctr = global_state_ctr


def gen4():
    global global_state_ctr, forward
    global frame_idx, round_idx
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
                    while frame_idx < gui_2lib.frames - 1:
                        frame_idx += 1
                        yield frame_idx
            else:
                if frame_idx == 0:
                    print("bck long dist!")
                    round_idx = config.NUM_OF_MOVES - 1
                    frame_idx = gui_2lib.frames - 1
                else:
                    while frame_idx > 0:
                        frame_idx -= 1
                        yield frame_idx
                    if round_idx == 0:
                        pass
                    else:
                        round_idx -= 1
                        frame_idx = gui_2lib.frames - 1

            assert frame_idx in {0, gui_2lib.frames - 1}
            local_state_ctr += 1
            print(round_idx, frame_idx)



def _update(idx):
    # global ctr2
    # print("update called", ctr2)
    # ctr2 += 1
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

    anim = animation.FuncAnimation(fig, _update, gen4, blit=False, interval=5, repeat=False)
    axprev = plt.axes([0.8, 0, 0.1, 0.075])
    axnext = plt.axes([0.9, 0, 0.1, 0.075])
    bprev = Button(axprev, 'Prev')
    bnext = Button(axnext, 'Next')
    bprev.on_clicked(on_click_prev)
    bnext.on_clicked(on_click_next)
    plt.show()
