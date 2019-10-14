import numpy as np
from time import time
from collections import defaultdict

seed = str(time()).split(".")
seed = [int(seed[0]), int(seed[1])]
np.random.seed(seed)


class Coordinate:
    def __init__(self, x, y, s=1):
        self.x = x
        self.y = y
        self.s = s

    def __repr__(self):
        return f"({self.x:4.1f}, {self.y:4.1f})"


class SimulationMap:
    def __init__(self, x=10, y=10, map_t="plane", mobility_t="RWP"):
        self.x_max = x
        self.y_max = y
        self.map_type = "torus" if map_t == "torus" else "plane"
        self.mobility_type = mobility_t
        self.map = []
        self.idx = []
        self.prob = []
        self.granularity = 0.5
        self.precision = 1

    def init_map(self, ratio_dict=None):
        for j in np.arange(0, self.y_max, self.granularity):
            row = []
            for i in np.arange(0, self.x_max, self.granularity):
                row.append(Coordinate(round(i, self.precision), round(j, self.precision)))
            self.map.append(row)

        if ratio_dict is not None:
            shares = len(self.map) * len(self.map[0])
            for share, items in ratio_dict.items():
                shares -= len(items)
                shares += len(items) * share
            print("total shares", shares)

            for share, items in ratio_dict.items():
                for item in items:
                    if item[0] >= self.x_max or item[1] >= self.y_max:
                        raise Exception("item[0] >= self.x_max or item[1] >= self.y_max")
                    x_comp, y_comp = int(item[0] / self.granularity), int(item[1] / self.granularity)
                    if self.map[y_comp][x_comp].x != item[0] or self.map[y_comp][x_comp].y != item[1]:
                        raise Exception("receive item", item, "self.map[x_comp][y_comp]", self.map[y_comp][x_comp])
                    self.map[y_comp][x_comp].s = share
                    print(item, self.map[y_comp][x_comp])

            self.idx = [i for i in range(len(self.map) * len(self.map[0]))]
            self.prob = np.array([np.float64(coor.s / shares) for row in self.map for coor in row])
            self.prob /= self.prob.sum()

    def print_map(self):
        for j, row in enumerate(self.map):
            for i, coor in enumerate(row):
                # print(i, coor, self.prob[j * len(self.map[0]) + i], end="\t")
                print(coor, self.prob[j * len(self.map[0]) + i], end="\t")
            print()

    def get_RWP1_target(self):
        idx = np.random.choice(self.idx, 1, True, self.prob)[0]
        y_comp = idx // len(self.map[0])
        x_comp = idx % len(self.map[0])
        coor = self.map[y_comp][x_comp]
        return coor.x, coor.y

    def get_RWP2_target(self, current):
        x_min = current[0] - self.x_max / 2
        x_max = current[0] + self.x_max / 2
        y_min = current[1] - self.y_max / 2
        y_max = current[1] + self.y_max / 2

        print("current", *current)
        print("frame - x", x_min, x_max)
        print("frame - y", y_min, y_max)
        x, y = self.get_RWP1_target()
        print("raw", x, y)
        if x < x_min:
            x += self.x_max
        elif x > x_max:
            x -= self.x_max
        if y < y_min:
            y += self.y_max
        elif y > y_max:
            y -= self.y_max
        x = round(x, self.precision)
        y = round(y, self.precision)
        print("adj", x, y)


if __name__ == '__main__':
    a = SimulationMap()
    shares = {
        50: [(0.5, 0.5), (1, 0.5), (2, 5), (7, 9), (2, 4), (2, 8)],
    }
    a.init_map(shares)
    a.print_map()
    a.get_RWP2_target((3, 3))
    a.get_RWP2_target((3, 3))
