import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import redis

X_MAX = 100
Y_MAX = 100
NUM_OF_CARS = 700
NUM_OF_MOVES = 500
SOURCE_POS = (50, 50)

assert 0 < X_MAX
assert 0 < Y_MAX
assert 0 < NUM_OF_CARS
assert 0 < NUM_OF_MOVES
assert 0 <= SOURCE_POS[0] < X_MAX
assert 0 <= SOURCE_POS[1] < Y_MAX


class Car:
    """
    does not specify target: random targets
    specify one target same as pos: stand still
    specify one target t1, t2, t3: generate random targets after t3
    specify one target t1, t2, t3, t3: stand still after t3


    """

    def __init__(self, index, seed, is_source, pos=None, targets=None):
        assert 0 <= index
        self.index = index
        self.rand = random.Random(f"{seed}+{self.index}")

        if pos is None:
            while True:
                x_pos = self.rand.uniform(0, X_MAX)
                y_pos = self.rand.uniform(0, Y_MAX)
                if x_pos != SOURCE_POS[0] or y_pos != SOURCE_POS[1]:
                    pos = (x_pos, y_pos)
                    break
        self.trace = [pos]  # the init position + every valid step (after moving)
        self.targets = [pos]  # the init position + every valid targets (after generation)

        if is_source:
            self.when = 0  # which round it becomes a broadcaster (-1: not a broadcaster now)
        else:
            self.when = -1

        if isinstance(targets, list):
            self.targets.extend(targets)
        self.target_idx = 1  # the car is going for the 1st target (2nd elem in the list)

    """
        source's behaviour: if reach the final target, does not generate a target or move further
        other cars: if reach the final target, generate a target and move further
    """

    def move(self):
        # if self.when == 0 and self.targets[self.target_idx] == self.targets[self.target_idx - 1]:  ##
        #     return
        step_rem = 1
        while step_rem > 0:
            step_rem = self._move(step_rem)

    def _move(self, step):
        tx, ty = self.get_target()
        px = self.targets[self.target_idx - 1][0]
        py = self.targets[self.target_idx - 1][1]
        if tx == px and ty == py:
            pos = (tx, ty)
            self.trace.append(pos)
            return -1

        cx, cy = self.get_position()
        dist = math.sqrt((tx - cx) ** 2 + (ty - cy) ** 2)
        if step >= dist:
            pos = (tx, ty)
            self.trace.append(pos)
            self.target_idx += 1
            return step - dist
        else:
            dx = (tx - cx) * step / dist
            dy = (ty - cy) * step / dist
            cx = cx + dx
            cy = cy + dy
            self.trace.append((cx, cy))
            return -1

    def get_target(self):
        """
        get the target position. If there's no target, generate one
        :return:
        """
        self._set_target()
        tx = self.targets[self.target_idx][0]
        ty = self.targets[self.target_idx][1]

        return tx, ty

    def _set_target(self):
        if self.target_idx == len(self.targets):
            tx = self.rand.uniform(0, X_MAX)
            ty = self.rand.uniform(0, Y_MAX)
            px = self.targets[self.target_idx - 1][0]
            py = self.targets[self.target_idx - 1][1]
            if tx != px or ty != py:
                self.targets.append((tx, ty))
            if self.when == 0:
                print("the source is generating a target to go, at rd=", len(self.trace))

    def get_position(self):
        cx = self.trace[-1][0]
        cy = self.trace[-1][1]
        return cx, cy

    def get_dist(self, ax, ay):
        """
        get dist from (ax, ay) to the current position
        :param ax:
        :param ay:
        :return:
        """
        cx, cy = self.get_position()
        dist = math.sqrt((ax - cx) ** 2 + (ay - cy) ** 2)
        return dist

    def truncate(self):
        self.get_target()
        self.trace = self.trace[-1:]
        self.targets = self.targets[-2:]
        self.target_idx = 1


class Simulation:
    def __init__(self, seed, source_targets):
        self.cars = []
        c1 = Car(0, seed, True, SOURCE_POS, source_targets)
        self.cars.append(c1)
        for i in range(1, NUM_OF_CARS):
            self.cars.append(Car(i, seed, False))

        self.num_of_broadcasters = []  # 0th round (after initialization), and after every move (w or w/o propagate)
        self.neighbor_percentage = []  # same as above

    def cars_move(self):
        for car in self.cars:
            car.move()

    def propagate(self, rd):
        broadcasters_list = []
        for car in self.cars:
            if car.when >= 0:
                broadcasters_list.append(car.get_position())

        for car in self.cars:
            if car.when == -1:
                for ax, ay in broadcasters_list:
                    if car.get_dist(ax, ay) <= 1:
                        car.when = rd

    def calculate_num_of_broadcasters(self):
        broadcasters_cnt = 0
        for car in self.cars:
            if car.when >= 0:
                broadcasters_cnt += 1
        self.num_of_broadcasters.append(broadcasters_cnt)

    def calculate_neighbor_percentage(self):
        """
        warning: extremely time consuming
        fortunately, we only need to run it a few times before simulation
        :return:
        """
        rates = []
        for car in self.cars:
            num_of_nbrs = 0
            for c in self.cars:
                if c.get_dist(*car.get_position()) <= 1:
                    num_of_nbrs += 1
            num_of_nbrs -= 1  # minus itself
            rate = num_of_nbrs / NUM_OF_CARS
            rates.append(rate)
        self.neighbor_percentage.append(sum(rates) / NUM_OF_CARS)

    def simulate(self, override=False):
        """
        override NUM OF MOVES so that the simulation continues until all cars received the msg
        :param override:
        :return:
        """
        # prepare - move all cars except the source
        for _ in range(50):
            for car in self.cars[1:]:
                car.move()
        # prepare - truncate their traces and targets (for graphing)
        for car in self.cars[1:]:
            car.truncate()

        # prepare - should be 1 before propagation
        self.calculate_num_of_broadcasters()
        # self.calculate_neighbor_percentage()  ###
        rd = 1
        while self.num_of_broadcasters[-1] != len(self.cars):
            self.cars_move()
            self.propagate(rd)
            self.calculate_num_of_broadcasters()
            # self.calculate_neighbor_percentage()  ###
            if not override and rd == NUM_OF_MOVES:
                break
            rd += 1

    def get_data(self):
        traces = []
        targets = []
        for car in self.cars:
            traces.append(car.trace)
            targets.append(car.targets)
        # whens = [car.when for car in self.cars]
        # whens.sort()
        # print(whens)
        # print("the 1st car received the msg on rd=", whens[1])
        # print("the last car received the msg on rd=", whens[-1])
        # print("the 5% car received the msg on rd=", whens[int(len(whens) * 0.05)])
        # print("the 95% car received the msg on rd=", whens[int(len(whens) * 0.95)])
        # when = (whens[1], whens[-1], whens[int(len(whens) * 0.05)], whens[int(len(whens) * 0.95)])
        # return traces, targets, self.num_of_broadcasters, self.neighbor_percentage, when

        whens = [car.when for car in self.cars]
        whens.sort()
        when = whens[int(len(whens) * 0.95)]
        # print("the 90th percentile is at round", when)
        whens = [0 if car.when > when else 1 for car in self.cars]  # 0: 90% - 100%, 1: 0% - 90%
        return traces, targets, self.num_of_broadcasters, self.neighbor_percentage, whens


class GUI:
    def __init__(self, traces, targets, broadcasters, neighbors, whens):
        self.traces = traces
        self.targets = targets
        self.broadcasters = broadcasters
        self.neighbors = neighbors
        self.whens = whens

        self.fig = plt.figure(figsize=(18, 9))
        self.ax1 = self.fig.add_subplot(121, xlim=[0, X_MAX], ylim=[0, Y_MAX])
        self.ax1.set_xticks(np.arange(0, X_MAX + 1, 5))
        self.ax1.set_yticks(np.arange(0, Y_MAX + 1, 5))

        # self.ax2 = self.fig.add_subplot(122, xlim=[0, NUM_OF_MOVES], ylim=[0, 0.002])  ###
        x_max = NUM_OF_MOVES if len(self.broadcasters) <= NUM_OF_MOVES else len(self.broadcasters)
        self.ax3 = self.fig.add_subplot(122, xlim=[x_max - 500, x_max], ylim=[0, NUM_OF_CARS])

    def draw(self):
        # all traces and targets
        # for trace in self.traces:
        #     xys = list(zip(*trace))
        #     xs = list(xys[0])
        #     ys = list(xys[1])
        #     self.ax1.plot(xs, ys, linewidth=1, marker='o', markersize=6)
        # for target in self.targets:
        #     xys = list(zip(*target))
        #     xs = list(xys[0])
        #     ys = list(xys[1])
        #     self.ax1.plot(xs, ys, linewidth=1, marker="s", markersize=3)

        for i, trace in enumerate(self.traces):
            last_x, last_y = trace[-1]
            if self.whens[i] == 0:
                self.ax1.plot(last_x, last_y, linewidth=1, marker='s', markersize=6)
            else:
                self.ax1.plot(last_x, last_y, linewidth=1, marker='o', markersize=3)

        # only source's traces and targets
        trace = self.traces[0]
        xys = list(zip(*trace))
        xs = list(xys[0])
        ys = list(xys[1])
        self.ax1.plot(xs, ys, linewidth=1, marker='o', markersize=6)
        #
        target = self.targets[0]
        xys = list(zip(*target))
        xs = list(xys[0])
        ys = list(xys[1])
        self.ax1.plot(xs, ys, linewidth=1, marker="s", markersize=3)

        self.ax1.set_xlabel("x axis")
        self.ax1.set_ylabel("y axis")
        self.ax1.set_title("source's position")
        self.ax1.grid(True)

        # average MN neighbor percentage
        # xs = [i for i in range(len(self.neighbors))]
        # print(self.neighbors)
        # self.ax2.plot(xs, self.neighbors, marker='o')
        # self.ax2.grid(True)

        # round vs # of broadcasters
        xs = [i for i in range(len(self.broadcasters))]
        self.ax3.plot(xs, self.broadcasters, marker='o', markersize=3)

        self.ax3.set_xlabel("simulation round")
        self.ax3.set_ylabel("# of msg received cars")
        self.ax3.set_title("# of msg received cars vs. simulation round \n")
        self.ax3.grid(True)

    def show(self):
        plt.show()

    def save(self, name):
        plt.tight_layout()
        plt.savefig(f"{name}.png")
        plt.clf()
        plt.close()


if __name__ == '__main__':
    pass

    # distribution: rounds needed to finish simulation vs frequency
    # round vs source's area span
    # how the center of the span is far away from the center of the field
    # how borders of the span is far away from borders of the field
    # TODO analysis some trend: area vs neighbor rate vs infection rate
    # TODO: more unit tests
    # RWM: # of broadcasters distribution

    # want to investigate: how different if the source choose different routes
    # if target is over, then stand still.3

    # todo: quantative analysis
    # 100? 500? 1000? how well they different
    # torus shape map
    # new mobility model

    r = redis.Redis(host='localhost', port=6379, db=0)
    targets = {
        0: [(100, 100), (0, 0), (100, 100)],
        1: [(100, 100), (100, 100)],
        2: [(50, 50), (50, 50)],
        3: [(50, 50), (100, 0), (50, 50), (0, 0),
            (50, 50), (100, 0), (50, 50), (0, 0),
            (50, 50), (100, 0), (50, 50), (0, 0)],
        4: [(25, 25), (25, 75), (75, 75), (75, 25),
            (25, 25), (25, 75), (75, 75), (75, 25),
            (25, 25), (25, 75), (75, 75), (75, 25),
            (25, 25), (25, 75), (75, 75), (75, 25),
            (25, 25), (25, 75), (75, 75), (75, 25)],
        5: [(10, 10), (10, 90), (90, 90), (90, 10),
            (10, 10), (10, 90), (90, 90), (90, 10),
            (10, 10), (10, 90), (90, 90), (90, 10),
            (10, 10), (10, 90), (90, 90), (90, 10)],
        6: [(75, 75), (75, 25), (25, 25), (25, 75),
            (75, 75), (75, 25), (25, 25), (25, 75),
            (75, 75), (75, 25), (25, 25), (25, 75),
            (75, 75), (75, 25), (25, 25), (25, 75)],
        7: [(90, 90), (90, 10), (10, 10), (10, 90),
            (90, 90), (90, 10), (10, 10), (10, 90),
            (90, 90), (90, 10), (10, 10), (10, 90)],  ###
        8: [(50, 100), (50, 0), (50, 100), (50, 0), (50, 100), (50, 0)],
        9: [(50, 100), (50, 100)],
        10: [(50, 50), (50, 50)],  ##
        11: [(50, 50), (100, 50), (50, 50), (50, 0),
             (50, 50), (100, 50), (50, 50), (50, 0),
             (50, 50), (100, 50), (50, 50), (50, 0)],
        12: [(50, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25)],
        13: [(50, 10),
             (10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10)],
        14: [(50, 75),
             (75, 75), (75, 25), (25, 25), (25, 75),
             (75, 75), (75, 25), (25, 25), (25, 75),
             (75, 75), (75, 25), (25, 25), (25, 75),
             (75, 75), (75, 25), (25, 25), (25, 75)],
        15: [(50, 90),
             (90, 90), (90, 10), (10, 10), (10, 90),
             (90, 90), (90, 10), (10, 10), (10, 90),
             (90, 90), (90, 10), (10, 10), (10, 90)],  ###
        16: [(50, 50)],
        17: [(10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10)],
        18: [(25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25)],
        19: [(50, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25),
             (25, 25), (25, 75), (75, 75), (75, 25)],
        20: [(50, 10),
             (10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10),
             (10, 10), (10, 90), (90, 90), (90, 10)],
    }

    for i in range(100):
        RAND_SEED = "%.20f" % time.time()
        print(i, RAND_SEED)
        results = []
        if SOURCE_POS == (0, 0):
            ra = range(0, 8)
        elif SOURCE_POS == (50, 0):
            ra = range(8, 16)
        elif SOURCE_POS == (50, 50):
            ra = range(16, 21)
        else:
            ra = []

        for k in ra:
            sim = Simulation(RAND_SEED, targets[k])
            sim.simulate(True)
            results.append(len(sim.num_of_broadcasters) - 1)
        print(results)
        # r_set_name = f"normal-{SOURCE_POS}-100"
        r_set_name = f"normal-{SOURCE_POS}-c{NUM_OF_CARS}"
        r.sadd(r_set_name, str((RAND_SEED, results)))
