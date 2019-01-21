from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import main
import config
import helplib
from types import MethodType
import matplotlib.text
import numpy as np
import pickle

t = "config and round info"


def adjust_axis(ax):
    # draw axis
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


class GUI(object):
    def __init__(self):
        self.forward = True
        self.round_idx = 0
        self.frame_idx = 0
        self.global_state_ctr = 0
        self.grid, self.broadcaster, self.stats = main.run()
        # with open('run.pickle', 'rb') as handle:
        #     self.grid, self.broadcaster, self.stats = pickle.load(handle)
        pos_tbl = helplib.get_plotting_pos_tbl(self.grid)
        self.frames = helplib.get_ls_tbl(pos_tbl)
        self.colors = helplib.get_color_tbl(self.grid)
        self.source_pos_tbl = helplib.get_source_pos_tbl(self.grid)
        x, y = [], []
        for xc, yc in pos_tbl[0]:
            x.append(xc)
            y.append(yc)

        self.fig = plt.figure(figsize=(18, 9))
        ax = self.fig.add_subplot(121, xlim=[config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX + 1],
                                  ylim=[config.LAST_COL_INDEX + 1, config.FIRST_COL_INDEX])
        adjust_axis(ax)
        # handler to the first plot
        self.scat = plt.scatter(x, y, c=self.colors[0], alpha=0.8)

        # handler to the second plot
        self.ax = self.fig.add_subplot(122, xlim=[config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX + 1],
                                       ylim=[config.LAST_COL_INDEX + 1, config.FIRST_COL_INDEX])
        adjust_axis(self.ax)
        self.ax.text(config.LAST_ROW_INDEX + 1.5, 0, "Configurations:")
        self.ax.text(config.LAST_ROW_INDEX + 1.5, 0.5, f"Num of rows {config.NUM_OF_ROWS}")
        self.ax.text(config.LAST_ROW_INDEX + 1.5, 1, f"Num of cols {config.NUM_OF_COLS}")
        self.ax.text(config.LAST_ROW_INDEX + 1.5, 1.5, f"Num of cars {config.NUM_OF_CARS}")
        self.ax.text(config.LAST_ROW_INDEX + 1.5, 2, f"allow standing {config.ALLOW_STANDING}")
        self.ax.text(0, config.LAST_COL_INDEX + 1.5, "Runtime info:")
        self.ax.text(0, config.LAST_COL_INDEX + 2, f"Round: {0} out of {len(self.stats) - 1}, Grid: {1}, Cars: {1}")

    def on_click_next(self, event):
        self.global_state_ctr += 1
        self.forward = True

    def on_click_prev(self, event):
        self.global_state_ctr += 1
        self.forward = False

    def _update(self, foo):
        self.scat.set_offsets(self.frames[self.round_idx][self.frame_idx])

    def gen(self):
        local_state_ctr = 0

        while True:
            yield self.frame_idx
            if self.global_state_ctr > local_state_ctr:
                if self.forward:
                    # already the final state, but pressed forward
                    # if self.round_idx == config.NUM_OF_MOVES - 1:
                    if self.round_idx == len(self.stats) - 2:
                        self.round_idx, self.frame_idx = 0, 0
                        self.scat.set_facecolors(self.colors[0])
                        self.ax.lines = []
                        self.ax.texts.pop()
                        self.ax.text(0, config.LAST_COL_INDEX + 2,
                                     f"Round: {self.stats[self.round_idx][0]} out of {len(self.stats) - 1},"
                                     f" Grid: {self.stats[self.round_idx][1]},"
                                     f" Cars: {self.stats[self.round_idx][2]}")

                    else:
                        # if not the very initial state
                        if self.frame_idx > 0:
                            self.round_idx += 1
                            self.frame_idx = 0

                        # for all states except the the final state
                        while self.frame_idx < config.FRAMES - 1:
                            self.frame_idx += 1
                            yield self.frame_idx
                        self.scat.set_facecolors(self.colors[self.round_idx + 1])
                        self.ax.plot(self.source_pos_tbl[0][self.round_idx: self.round_idx + 2],
                                     self.source_pos_tbl[1][self.round_idx: self.round_idx + 2], 'r--')
                        self.ax.texts.pop()
                        self.ax.text(0, config.LAST_COL_INDEX + 2,
                                     f"Round: {self.stats[self.round_idx + 1][0]} out of {len(self.stats) - 1},"
                                     f" Grid: {self.stats[self.round_idx + 1][1]},"
                                     f" Cars: {self.stats[self.round_idx + 1][2]}")

                else:
                    # if the very initial state, but pressed backward
                    if self.frame_idx == 0:
                        # self.round_idx = config.NUM_OF_MOVES - 1
                        self.round_idx = len(self.stats) - 2
                        self.frame_idx = config.FRAMES - 1
                        self.scat.set_facecolors(self.colors[-1])
                        # for move in range(config.NUM_OF_MOVES):
                        for move in range(len(self.stats) - 1):
                            self.ax.plot(self.source_pos_tbl[0][move: move + 2],
                                         self.source_pos_tbl[1][move: move + 2], 'r--')
                        self.ax.texts.pop()
                        self.ax.text(0, config.LAST_COL_INDEX + 2,
                                     f"Round: {self.stats[self.round_idx + 1][0]} out of {len(self.stats) - 1},"
                                     f" Grid: {self.stats[self.round_idx + 1][1]},"
                                     f" Cars: {self.stats[self.round_idx + 1][2]}")

                    else:
                        while self.frame_idx > 0:
                            self.frame_idx -= 1
                            yield self.frame_idx
                        self.ax.texts.pop()

                        if self.round_idx > 0:
                            self.round_idx -= 1
                            self.frame_idx = config.FRAMES - 1
                            self.scat.set_facecolors(self.colors[self.round_idx + 1])
                            self.ax.text(0, config.LAST_COL_INDEX + 2,
                                         f"Round: {self.stats[self.round_idx + 1][0]} out of {len(self.stats) - 1},"
                                         f" Grid: {self.stats[self.round_idx + 1][1]},"
                                         f" Cars: {self.stats[self.round_idx + 1][2]}")
                        # the state that just pressed once next, and not presses prev
                        else:
                            self.scat.set_facecolors(self.colors[0])
                            self.ax.text(0, config.LAST_COL_INDEX + 2,
                                         f"Round: {self.stats[self.round_idx][0]} out of {len(self.stats) - 1},"
                                         f" Grid: {self.stats[self.round_idx][1]},"
                                         f" Cars: {self.stats[self.round_idx][2]}")
                        self.ax.lines.pop()

                assert self.frame_idx in {0, config.FRAMES - 1}
                local_state_ctr += 1
                # print("(diff from gui) round and frame:", self.round_idx, self.frame_idx)

    def show(self):
        anim = animation.FuncAnimation(self.fig, self._update, self.gen, interval=1, repeat=False)
        axprev = plt.axes([0.8, 0, 0.1, 0.075])
        axnext = plt.axes([0.9, 0, 0.1, 0.075])
        bprev = Button(axprev, 'Prev')
        bnext = Button(axnext, 'Next')
        bprev.on_clicked(self.on_click_prev)
        bnext.on_clicked(self.on_click_next)
        plt.show()


if __name__ == '__main__':
    gui = GUI()
    gui.show()
    # g, b = main.run()
    # print(helplib.get_source_pos_tbl(g))
