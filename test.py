from random import Random
import matplotlib.pyplot as plt
import numpy as np
from help import *


class GUI3(GUI):
    def __init__(self, names, records):
        assert len(names) == len(records)
        self.names = names
        self.records = records

        low = min(records[0])
        hi = max(records[0])
        for record in records:
            l_low = min(record)
            if l_low < low:
                low = l_low
            l_hi = max(record)
            if l_hi > hi:
                hi = l_hi
        self.lo = low
        self.hi = hi

        self.fig = plt.figure(figsize=(36, 9))
        self.axs = []
        for i in range(len(names)):
            axi = self.fig.add_subplot(int(f"{len(names)}1{i + 1}"))
            self.axs.append(axi)

    def draw(self):
        for i in range(len(self.names)):
            self.axs[i].grid(True)
            y_pos = list(range(self.lo, self.hi + 1))
            x_bars = [0 for i in y_pos]
            for record in self.records[i]:
                x_bars[(record - self.lo)] += 1
            self.axs[i].bar(y_pos, x_bars)
            self.axs[i].set_title(self.names[i])


if __name__ == '__main__':
    pass
    #     r.sadd(f"E-{MOB}-{X_MAX}-{Y_MAX}-{NUM_OF_CARS}-{SOURCE_POS[0]}-{SOURCE_POS[1]}-s0",
    #            str((rd, RAND_SEED)))
