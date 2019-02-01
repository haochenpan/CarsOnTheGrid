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


def adjust_axis(ax):
    # draw axis
    ax.grid(b=True)
    ax.xaxis.tick_top()
    ax.set_xticks(np.arange(config.FIRST_ROW_INDEX, config.LRI + 1, 1))
    ax.set_yticks(np.arange(config.FIRST_COL_INDEX, config.LCI + 1, 1))

    # shift tick labels
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

    # append axis labels
    ax.set_xlabel("Row Num")
    ax.xaxis.set_label_position('top')
    ax.set_ylabel("Col Num")


class Gui(object):
    def __init__(self, data=None, mode=0, name="snapshot"):
        """

        :param data:
        :param mode: 0 = user control and snapshot; 1 = snapshot only
        :param name:
        """
        assert mode in {0, 1}

        # load simulation data
        if data is None:
            grid, self.stat = main.run()
        elif type(data) is tuple:
            assert len(data) == 2
            grid = data[0]
            self.stat = data[1]
        elif type(data) is str:
            try:
                with open(data, 'rb') as handle:
                    grid, self.stat = pickle.load(handle)
            except FileNotFoundError:
                print("pickle file not found!")
                return
        else:
            raise Exception

        # generate plotting and animation data
        pos_tbl = helplib.get_plotting_pos_tbl(grid)
        x, y = helplib.get_init_plotting_pos(pos_tbl)
        self.frames = helplib.get_ls_tbl(pos_tbl)
        self.colors = helplib.get_color_tbl(grid)
        self.source_pos_tbl = helplib.get_source_pos_tbl(grid)

        # initialize animation variables
        self.forward = True
        self.round_idx = 0
        self.frame_idx = 0
        self.state_ctr = 0

        # composition
        self.fig = plt.figure(figsize=(18, 9))

        # snapshot - source's trace = ax2
        self.ax2 = self.fig.add_subplot(122, xlim=[config.FRI, config.LRI + 1],
                                        ylim=[config.LCI + 1, config.FCI])

        adjust_axis(self.ax2)
        self._set_up_text(-1)
        for move in range(len(self.stat) - 1):
            self.ax2.plot(self.source_pos_tbl[0][move: move + 2], self.source_pos_tbl[1][move: move + 2], 'r--')

        # snapshot - line chart = ax31, additional axis = ax32
        ax1_1 = self.fig.add_subplot(121, xlim=[0, config.NUM_OF_MOVES], ylim=[0, config.NUM_OF_CARS])
        ax3stat = np.column_stack(self.stat)
        ax1_1.plot(ax3stat[0], ax3stat[2], 'b')
        ax1_1.set_ylabel('Num of Cars', color='b')
        ax1_1.tick_params('y', colors='b')
        ax1_2 = ax1_1.twinx()
        ax1_2.set_ylim(0, config.NOR * config.NOC)
        ax1_2.plot(ax3stat[0], ax3stat[1], 'r')
        ax1_2.set_ylabel('Num of Grids', color='r')
        ax1_2.tick_params('y', colors='r')

        # snapshot - save snapshot
        plt.savefig(f"./{name}.png")
        plt.clf()
        if mode != 0:
            plt.close('all')
            return

        # user control - scatter plot
        self.ax2 = self.fig.add_subplot(122, xlim=[config.FRI, config.LRI + 1],
                                        ylim=[config.LCI + 1, config.FCI])
        adjust_axis(self.ax2)
        self._set_up_text(0)

        self.ax1 = self.fig.add_subplot(121, xlim=[config.FRI, config.LRI + 1],
                                        ylim=[config.LCI + 1, config.FCI])
        adjust_axis(self.ax1)
        self.scat = plt.scatter(x, y, c=self.colors[0], alpha=0.8)
        self._show()

    def _set_up_text(self, index):
        self.ax2.text(config.LRI + 1.5, 0, "Configurations:")
        self.ax2.text(config.LRI + 1.5, 0.5, f"Num of rows {config.NOR}")
        self.ax2.text(config.LRI + 1.5, 1, f"Num of cols {config.NOC}")
        self.ax2.text(config.LRI + 1.5, 1.5, f"Num of cars {config.NUM_OF_CARS}")
        self.ax2.text(config.LRI + 1.5, 2, f"allow standing {config.ALLOW_STANDING}")
        self.ax2.text(0, config.LCI + 1.5, "Runtime info:")
        self.ax2.text(0, config.LCI + 2,
                      f"Round: {self.stat[index][0]} / {len(self.stat) - 1},"
                      f" Grid: {self.stat[index][1]},"
                      f" Cars: {self.stat[index][2]}")

    def _on_click_next(self, event):
        self.state_ctr += 1
        self.forward = True

    def _on_click_prev(self, event):
        self.state_ctr += 1
        self.forward = False

    def _update(self, foo):
        self.scat.set_offsets(self.frames[self.round_idx][self.frame_idx])

    def _gen(self):
        local_state_ctr = 0
        while True:
            yield self.frame_idx
            if self.state_ctr > local_state_ctr:
                if self.forward:
                    # already the final state, but pressed forward
                    # if self.round_idx == config.NUM_OF_MOVES - 1:
                    if self.round_idx == len(self.stat) - 2:
                        self.round_idx, self.frame_idx = 0, 0
                        self.scat.set_facecolors(self.colors[0])
                        self.ax2.lines = []
                        self.ax2.texts.pop()
                        self.ax2.text(0, config.LCI + 2,
                                      f"Round: {self.stat[self.round_idx][0]} out of {len(self.stat) - 1},"
                                      f" Grid: {self.stat[self.round_idx][1]},"
                                      f" Cars: {self.stat[self.round_idx][2]}")

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
                        self.ax2.text(0, config.LCI + 2,
                                      f"Round: {self.stat[self.round_idx + 1][0]} out of {len(self.stat) - 1},"
                                      f" Grid: {self.stat[self.round_idx + 1][1]},"
                                      f" Cars: {self.stat[self.round_idx + 1][2]}")

                else:
                    # if the very initial state, but pressed backward
                    if self.frame_idx == 0:
                        # self.round_idx = config.NUM_OF_MOVES - 1
                        self.round_idx = len(self.stat) - 2
                        self.frame_idx = config.FRAMES - 1
                        self.scat.set_facecolors(self.colors[-1])
                        # for move_cars in range(config.NUM_OF_MOVES):
                        for move in range(len(self.stat) - 1):
                            self.ax2.plot(self.source_pos_tbl[0][move: move + 2],
                                          self.source_pos_tbl[1][move: move + 2], 'r--')
                        self.ax2.texts.pop()
                        self.ax2.text(0, config.LCI + 2,
                                      f"Round: {self.stat[self.round_idx + 1][0]} out of {len(self.stat) - 1},"
                                      f" Grid: {self.stat[self.round_idx + 1][1]},"
                                      f" Cars: {self.stat[self.round_idx + 1][2]}")

                    else:
                        while self.frame_idx > 0:
                            self.frame_idx -= 1
                            yield self.frame_idx
                        self.ax2.texts.pop()

                        if self.round_idx > 0:
                            self.round_idx -= 1
                            self.frame_idx = config.FRAMES - 1
                            self.scat.set_facecolors(self.colors[self.round_idx + 1])
                            self.ax2.text(0, config.LCI + 2,
                                          f"Round: {self.stat[self.round_idx + 1][0]} out of {len(self.stat) - 1},"
                                          f" Grid: {self.stat[self.round_idx + 1][1]},"
                                          f" Cars: {self.stat[self.round_idx + 1][2]}")
                        # the state that just pressed once next, and not presses prev
                        else:
                            self.scat.set_facecolors(self.colors[0])
                            self.ax2.text(0, config.LCI + 2,
                                          f"Round: {self.stat[self.round_idx][0]} out of {len(self.stat) - 1},"
                                          f" Grid: {self.stat[self.round_idx][1]},"
                                          f" Cars: {self.stat[self.round_idx][2]}")
                        self.ax2.lines.pop()

                assert self.frame_idx in {0, config.FRAMES - 1}
                local_state_ctr += 1
                # print("(diff from gui) round and frame:", self.round_idx, self.frame_idx)

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
    # g, b = main.run()
    # print(helplib.get_source_pos_tbl(g))
