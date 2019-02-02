"""
    When I Wrote It, Only God and I Knew the Meaning; Now God Alone Knows.
    This GUI works well, don't waste your time in attempting to simply it,
"""

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


class Gui(object):
    def __init__(self, data=None, mode=0, path="./snapshot"):
        """
        :param data:
        :param mode: 0 = user control and snapshot;
                     1 = snapshot only
        :param path: the path and name of the png snapshot
        """

        # load simulation data
        if data is None:
            grid, self.stats = main.run()
        elif type(data) is tuple:
            assert len(data) == 2
            grid = data[0]
            self.stats = data[1]
        elif type(data) is str:
            try:
                with open(data, 'rb') as handle:
                    grid, self.stats = pickle.load(handle)
            except FileNotFoundError:
                print("pickle file not found!")
                return
        else:
            raise Exception

        self.trace = self.stats["trace"]
        self.confi = self.stats["confi"]
        self.stats = self.stats["stats"]

        # initialize animation variables
        self.forward = True
        self.round_idx = 0
        self.frame_idx = 0
        self.state_ctr = 0

        # composition:
        # ax1 = scatter plot of cars
        # ax2 = source's trace
        # ax1_1 = num of cars that received the message
        # ax2_2 = num of blocks that received the message
        self.fig = plt.figure(figsize=(18, 9))

        # snapshot - source's trace
        self.ax2 = self.fig.add_subplot(122,
                                        xlim=[self.confi["FIRST_ROW_INDEX"], self.confi["LAST_ROW_INDEX"] + 1],
                                        ylim=[self.confi["LAST_COL_INDEX"] + 1, self.confi["FIRST_COL_INDEX"]])
        self._adjust_axis(self.ax2)
        self._set_up_text(-1)
        self.source_pos_tbl = helplib.get_source_pos_tbl2(self.trace)
        for move in range(len(self.stats) - 1):
            self.ax2.plot(self.source_pos_tbl[0][move: move + 2],
                          self.source_pos_tbl[1][move: move + 2], 'r--')

        # snapshot - statistics
        ax1_1 = self.fig.add_subplot(121, xlim=[0, self.confi["NUM_OF_MOVES"]], ylim=[0, self.confi["NUM_OF_CARS"]])
        ax3stat = np.column_stack(self.stats)
        ax1_1.plot(ax3stat[0], ax3stat[2], 'b')
        ax1_1.set_ylabel('Num of Cars', color='b')
        ax1_1.tick_params('y', colors='b')
        ax1_2 = ax1_1.twinx()
        ax1_2.set_ylim(0, self.confi["NUM_OF_ROWS"] * self.confi["NUM_OF_COLS"])
        ax1_2.plot(ax3stat[0], ax3stat[1], 'r')
        ax1_2.set_ylabel('Num of Grids', color='r')
        ax1_2.tick_params('y', colors='r')

        # snapshot - save snapshot
        plt.savefig(f"{path}.png")
        plt.clf()
        if mode != 0:
            plt.close('all')
            return

        # generate plotting and animation data
        pos_tbl = helplib.get_plotting_pos_tbl(grid)
        x, y = helplib.get_init_plotting_pos(pos_tbl)
        self.frames = helplib.get_ls_tbl(pos_tbl)
        self.colors = helplib.get_color_tbl(grid)

        # user control - scatter plot
        self.ax1 = self.fig.add_subplot(121,
                                        xlim=[self.confi["FIRST_ROW_INDEX"], self.confi["LAST_ROW_INDEX"] + 1],
                                        ylim=[self.confi["LAST_COL_INDEX"] + 1, self.confi["FIRST_COL_INDEX"]])
        self.scat = plt.scatter(x, y, c=self.colors[0], alpha=0.8)
        self.ax2 = self.fig.add_subplot(122,
                                        xlim=[self.confi["FIRST_ROW_INDEX"], self.confi["LAST_ROW_INDEX"] + 1],
                                        ylim=[self.confi["LAST_COL_INDEX"] + 1, self.confi["FIRST_COL_INDEX"]])
        self._adjust_axis(self.ax1)
        self._adjust_axis(self.ax2)
        self._set_up_text(0)
        self._show()

    def _adjust_axis(self, ax):
        # draw axis
        ax.grid(b=True)
        ax.xaxis.tick_top()
        ax.set_xticks(np.arange(self.confi["FIRST_ROW_INDEX"], self.confi["LAST_ROW_INDEX"] + 1, 1))
        ax.set_yticks(np.arange(self.confi["FIRST_COL_INDEX"], self.confi["LAST_COL_INDEX"] + 1, 1))

        # shift tick labels
        # https://stackoverflow.com/questions/28615887/how-to-move-a-ticks-label-in-matplotlib
        shift = -0.5  # Data coordinates
        for lbl in ax.xaxis.get_majorticklabels():
            lbl.customShiftValue = shift
            lbl.set_x = MethodType(lambda s, x:
                                   matplotlib.text.Text.set_x(s, x - s.customShiftValue), lbl)

        for lbl in ax.yaxis.get_majorticklabels():
            lbl.customShiftValue = shift
            lbl.set_y = MethodType(lambda s, y:
                                   matplotlib.text.Text.set_y(s, y - s.customShiftValue), lbl)

        # append axis labels
        ax.set_xlabel("Row Num")
        ax.xaxis.set_label_position('top')
        ax.set_ylabel("Col Num")

    def _set_up_text(self, round_index):
        self.ax2.text(self.confi["LAST_ROW_INDEX"] + 1.5, 0.0, f"Configurations:")
        self.ax2.text(self.confi["LAST_ROW_INDEX"] + 1.5, 0.5, f"Num of rows {self.confi['NUM_OF_ROWS']}")
        self.ax2.text(self.confi["LAST_ROW_INDEX"] + 1.5, 1.0, f"Num of cols {self.confi['NUM_OF_COLS']}")
        self.ax2.text(self.confi["LAST_ROW_INDEX"] + 1.5, 1.5, f"Num of cars {self.confi['NUM_OF_CARS']}")
        self.ax2.text(self.confi["LAST_ROW_INDEX"] + 1.5, 2.0, f"allow standing {self.confi['ALLOW_STANDING']}")
        self.ax2.text(0.0, self.confi["LAST_COL_INDEX"] + 1.5, f"Runtime info:")
        self.ax2.text(0.0, self.confi["LAST_COL_INDEX"] + 2.0,
                      f"Round: {self.stats[round_index][0]} / {len(self.stats) - 1},"
                      f" Grid: {self.stats[round_index][1]},"
                      f" Cars: {self.stats[round_index][2]}")

    def _on_click_next(self, event):
        self.state_ctr += 1
        self.forward = True

    def _on_click_prev(self, event):
        self.state_ctr += 1
        self.forward = False

    def _update(self, foo):
        self.scat.set_offsets(self.frames[self.round_idx][self.frame_idx])

    def _gen(self):
        """
        The round # on the GUI is different from the round # here
        :return:
        """
        local_state_ctr = 0
        while True:
            yield self.frame_idx
            if self.state_ctr > local_state_ctr:
                if self.forward:
                    # already the final state, but pressed forward
                    if self.round_idx == len(self.stats) - 2:
                        self.round_idx, self.frame_idx = 0, 0
                        self.scat.set_facecolors(self.colors[0])
                        self.ax2.lines = []
                        self.ax2.texts.pop()
                        self.ax2.text(0, self.confi["LAST_COL_INDEX"] + 2,
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
                        self.ax2.plot(self.source_pos_tbl[0][self.round_idx: self.round_idx + 2],
                                      self.source_pos_tbl[1][self.round_idx: self.round_idx + 2], 'r--')
                        self.ax2.texts.pop()
                        self.ax2.text(0, self.confi["LAST_COL_INDEX"] + 2,
                                      f"Round: {self.stats[self.round_idx + 1][0]} out of {len(self.stats) - 1},"
                                      f" Grid: {self.stats[self.round_idx + 1][1]},"
                                      f" Cars: {self.stats[self.round_idx + 1][2]}")

                else:
                    # if the very initial state, but pressed backward
                    if self.frame_idx == 0:
                        self.round_idx = len(self.stats) - 2
                        self.frame_idx = config.FRAMES - 1
                        self.scat.set_facecolors(self.colors[-1])
                        for move in range(len(self.stats) - 1):
                            self.ax2.plot(self.source_pos_tbl[0][move: move + 2],
                                          self.source_pos_tbl[1][move: move + 2], 'r--')
                        self.ax2.texts.pop()
                        self.ax2.text(0, self.confi["LAST_COL_INDEX"] + 2,
                                      f"Round: {self.stats[self.round_idx + 1][0]} out of {len(self.stats) - 1},"
                                      f" Grid: {self.stats[self.round_idx + 1][1]},"
                                      f" Cars: {self.stats[self.round_idx + 1][2]}")

                    else:
                        while self.frame_idx > 0:
                            self.frame_idx -= 1
                            yield self.frame_idx
                        self.ax2.texts.pop()

                        if self.round_idx > 0:
                            self.round_idx -= 1
                            self.frame_idx = config.FRAMES - 1
                            self.scat.set_facecolors(self.colors[self.round_idx + 1])
                            self.ax2.text(0, self.confi["LAST_COL_INDEX"] + 2,
                                          f"Round: {self.stats[self.round_idx + 1][0]} out of {len(self.stats) - 1},"
                                          f" Grid: {self.stats[self.round_idx + 1][1]},"
                                          f" Cars: {self.stats[self.round_idx + 1][2]}")
                        # the state that just pressed once next, and not presses prev
                        else:
                            self.scat.set_facecolors(self.colors[0])
                            self.ax2.text(0, self.confi["LAST_COL_INDEX"] + 2,
                                          f"Round: {self.stats[self.round_idx][0]} out of {len(self.stats) - 1},"
                                          f" Grid: {self.stats[self.round_idx][1]},"
                                          f" Cars: {self.stats[self.round_idx][2]}")
                        self.ax2.lines.pop()

                assert self.frame_idx in {0, config.FRAMES - 1}
                local_state_ctr += 1

    # noinspection PyTypeChecker
    def _show(self):
        anim = animation.FuncAnimation(self.fig, self._update, self._gen, interval=1, repeat=False)
        axprev = plt.axes([0.8, 0, 0.1, 0.075])
        axnext = plt.axes([0.9, 0, 0.1, 0.075])
        bprev = Button(axprev, 'Prev')
        bnext = Button(axnext, 'Next')
        bprev.on_clicked(self._on_click_prev)
        bnext.on_clicked(self._on_click_next)
        plt.show()


if __name__ == '__main__':
    gui = Gui(mode=0)
