from random import Random
import matplotlib.pyplot as plt
import numpy as np
from help import *


class Car:
    def __init__(self, index, seed, source_pos, targets=None):
        assert 0 <= index
        self.index = index
        self.when = 0 if index == 0 else -1
        self.rand = Random(f"{seed}+{self.index}")
        if self.index == 0:
            pos = source_pos
        else:
            while True:
                x_pos = self.rand.uniform(0, X_MAX)  # !
                y_pos = self.rand.uniform(0, Y_MAX)
                if x_pos != source_pos[0] or y_pos != source_pos[1]:
                    pos = (x_pos, y_pos)
                    break
        self.courses = [pos]
        self.targets = [pos]
        if targets is not None: self.targets.extend(targets)
        self.target_idx = 1

    def set_target(self):
        assert False, "not implemented"

    def move(self):
        assert False, "not implemented"

    def get_pos(self):
        cx = self.courses[-1][0]
        cy = self.courses[-1][1]
        return cx, cy

    def get_target(self):
        self.set_target()
        tx = self.targets[self.target_idx][0]
        ty = self.targets[self.target_idx][1]
        return tx, ty

    def get_prev_target(self):
        px = self.targets[self.target_idx - 1][0]
        py = self.targets[self.target_idx - 1][1]
        return px, py

    def truncate(self):
        self.set_target()
        self.courses = self.courses[-1:]
        self.targets = self.targets[-2:]
        self.target_idx = 1


class SynCar(Car):
    def move(self):
        step = 1
        while step > 0:
            # if the car sees a repeated target
            # it won't move but stays at the current pos
            px, py = self.get_prev_target()
            tx, ty = self.get_target()
            if tx == px and ty == py:
                self.courses.append((tx, ty))
                return

            cx, cy = self.get_pos()
            dist = get_dist(cx, cy, tx, ty)
            if step >= dist:
                self.courses.append((tx, ty))
                self.target_idx += 1
                step -= dist
            else:
                dx = (tx - cx) * step / dist
                dy = (ty - cy) * step / dist
                cx = cx + dx
                cy = cy + dy
                self.courses.append((cx, cy))
                return


class SynMGCar(Car):
    def __init__(self, index, seed, source_pos, targets=None, type=1):
        super().__init__(index, seed, source_pos, targets)
        if self.index == 0:
            pos = source_pos
        else:
            while True:
                if type == 1:
                    x_pos = self.rand.choice([i for i in range(0, X_MAX + 1)])
                    y_pos = self.rand.choice([i for i in range(0, Y_MAX + 1)])
                else:
                    x_pos = self.rand.choice([i for i in range(0, X_MAX)])
                    y_pos = self.rand.choice([i for i in range(0, Y_MAX)])
                if x_pos != source_pos[0] or y_pos != source_pos[1]:
                    pos = (x_pos, y_pos)
                    break
        self.courses = [pos]
        self.targets = [pos]
        if targets is not None: self.targets.extend(targets)

    def move(self):
        px, py = self.get_prev_target()
        tx, ty = self.get_target()
        if px != tx or py != ty:
            self.target_idx += 1
        self.courses.append((tx, ty))


class Simulation:
    def __init__(self):
        self.cars = []
        self.num_of_broadcasters = []
        self.neighbor_percentage = []

    def cars_move(self):
        [car.move() for car in self.cars]

    def propagate(self, rd):
        assert False, "not implemented"

    def calculate_num_of_broadcasters(self):
        num = 0
        for car in self.cars:
            if car.when >= 0:
                num += 1
        self.num_of_broadcasters.append(num)

    def calculate_neighbor_percentage(self):
        assert False, "not implemented"

    def simulate(self):
        for _ in range(PRE_RUN_COUNT):
            for car in self.cars[1:]:
                car.move()
        for car in self.cars[1:]:
            car.truncate()
        self.calculate_num_of_broadcasters()
        # self.calculate_neighbor_percentage()  ###

        rd = 1
        while self.num_of_broadcasters[-1] != NUM_OF_CARS:
            self.cars_move()
            self.propagate(rd)
            self.calculate_num_of_broadcasters()
            # self.calculate_neighbor_percentage()  ###
            if not EXCEED_MOVES and rd == NUM_OF_MOVES:
                break
            rd += 1

    def summary(self):
        courses = []
        targets = []
        for car in self.cars:
            courses.append(car.courses)
            targets.append(car.targets)
        return courses, targets, self.num_of_broadcasters, self.neighbor_percentage


class SynSimulation(Simulation):
    def propagate(self, rd):
        broadcaster_pos_list = [car.get_pos() for car in self.cars if car.when >= 0]
        for car in self.cars:
            if car.when == -1:
                for pos in broadcaster_pos_list:
                    dist = get_dist(*pos, *car.get_pos())
                    if dist <= 1:
                        car.when = rd
                        break

    def calculate_neighbor_percentage(self):
        rates = []
        for car in self.cars:
            num_of_nbrs = -1
            for c in self.cars:
                if get_dist(*c.get_pos(), *car.get_pos()) <= 1:
                    num_of_nbrs += 1
            rate = num_of_nbrs / NUM_OF_CARS
            rates.append(rate)
        self.neighbor_percentage.append((sum(rates) / NUM_OF_CARS))


class TorSynSimulation(Simulation):
    def propagate(self, rd):
        broadcaster_pos_list = [car.get_pos() for car in self.cars if car.when >= 0]
        mod_pos_list = list(map(lambda p: (p[0] % X_MAX, p[1] % Y_MAX), broadcaster_pos_list))
        for car in self.cars:
            if car.when == -1:
                car_x, car_y = car.get_pos()
                car_x, car_y = car_x % X_MAX, car_y % Y_MAX
                for pos in mod_pos_list:
                    dist = get_euclidean_dist(*pos, car_x, car_y)
                    if dist <= 1:
                        car.when = rd
                        break

    def calculate_neighbor_percentage(self):
        original_positions = [car.get_pos() for car in self.cars]
        mod_positions = list(map(lambda pos: (pos[0] % X_MAX, pos[1] % Y_MAX), original_positions))
        rates = []
        for pos1 in mod_positions:
            num_of_nbrs = -1  # minus itself
            for pos2 in mod_positions:
                if get_euclidean_dist(*pos1, *pos2) <= 1:
                    num_of_nbrs += 1
            rate = num_of_nbrs / NUM_OF_CARS
            rates.append(rate)
        self.neighbor_percentage.append((sum(rates) / NUM_OF_CARS))


class GUI:
    def show(self):
        plt.show()
        plt.clf()
        plt.close()

    def save(self, name):
        plt.tight_layout()
        plt.savefig(f"{name}.png")
        plt.clf()
        plt.close()


class GUIFinalPos(GUI):
    def __init__(self, sim: Simulation, mod, solo):
        self.sim = sim
        self.mod = mod
        self.solo = solo
        if solo:
            self.fig = plt.figure(figsize=fig_size)
        else:
            self.fig = plt.figure(figsize=(fig_size[0] * 2, fig_size[1]))
            self.ax1 = self.fig.add_subplot(121, xlim=[0, X_MAX], ylim=[0, Y_MAX])
            self.ax1.set_xticks(np.arange(0, X_MAX + 1, 5))
            self.ax1.set_yticks(np.arange(0, Y_MAX + 1, 5))

    def draw(self):
        # draw all final positions:
        for car in self.sim.cars:
            fx, fy = car.courses[-1]
            if self.mod:
                self.ax1.plot(fx % X_MAX, fy % X_MAX, "go", markersize=2)
            else:
                self.ax1.plot(fx, fy, "go", markersize=2)

        # for RD, to validate target positions
        # for car in self.sim.cars:
        #     self.ax1.plot(*unzip(car.targets[1:], False), "ro", markersize=2)

        source_courses = self.sim.cars[0].courses
        self.ax1.plot(*unzip(source_courses, self.mod), "bo", markersize=2)
        source_targets = self.sim.cars[0].targets
        self.ax1.plot(*unzip(source_targets, self.mod), "ro", markersize=4)

        self.ax1.set_xlabel("x axis")
        self.ax1.set_ylabel("y axis")
        self.ax1.set_title("final positions & the source's positions")
        self.ax1.grid(True)


class GUIHeatMap(GUIFinalPos):
    def __init__(self, sim: Simulation, mod, solo):
        super().__init__(sim, mod, solo)
        if not solo:
            self.ax3 = self.fig.add_subplot(122)
        else:
            self.ax3 = self.fig.add_subplot(111)
        self.ax3.set_xticks(np.arange(0, X_MAX + 1, 5))
        self.ax3.set_yticks(np.arange(0, Y_MAX + 1, 5))

    def draw(self):
        if not self.solo:
            super().draw()

        hot_map = [[0 for _ in range(X_MAX + 1)] for _ in range(Y_MAX + 1)]
        for car in self.sim.cars[1:]:
            for target in car.courses:
                if self.mod:
                    int_target_x = int(target[0]) % X_MAX
                    int_target_y = int(target[1]) % Y_MAX
                else:
                    int_target_x = int(target[0])
                    int_target_y = int(target[1])
                hot_map[int_target_y][int_target_x] += 1
        # hot_map = list(reversed(hot_map))
        im = self.ax3.imshow(hot_map)
        cbar = self.fig.colorbar(im, ax=self.ax3)
        cbar.ax.set_ylabel("frequencies", rotation=-90, va="bottom", fontsize=20)
        self.ax3.set_title("the heat map of all cars' paths", fontsize=20)


class GUINumBro(GUIFinalPos):
    def __init__(self, sim: Simulation, mod, solo):
        super().__init__(sim, mod, solo)
        x_max = NUM_OF_MOVES if len(self.sim.num_of_broadcasters) <= NUM_OF_MOVES else len(self.sim.num_of_broadcasters)
        if not solo:
            self.ax3 = self.fig.add_subplot(122, xlim=[x_max - 500, x_max], ylim=[0, NUM_OF_CARS])
        else:
            self.ax3 = self.fig.add_subplot(111, xlim=[x_max - 500, x_max], ylim=[0, NUM_OF_CARS])

    def draw(self):
        if not self.solo:
            super().draw()

        xs = [i for i in range(len(self.sim.num_of_broadcasters))]
        self.ax3.plot(xs, self.sim.num_of_broadcasters, marker='o', markersize=3)

        self.ax3.set_xlabel("simulation round")
        self.ax3.set_ylabel("# of msg received cars")
        self.ax3.set_title("# of msg received cars vs. simulation round \n")
        self.ax3.grid(True)


class GUINumNei(GUIFinalPos):
    def __init__(self, sim: Simulation, mod, solo):
        super().__init__(sim, mod, solo)
        if not solo:
            self.ax2 = self.fig.add_subplot(122, xlim=[0, NUM_OF_MOVES], ylim=[0, 0.002])
        else:
            self.ax2 = self.fig.add_subplot(111, xlim=[0, NUM_OF_MOVES], ylim=[0, 0.002])

    def draw(self):
        if not self.solo:
            super().draw()

        xs = [i for i in range(len(self.sim.neighbor_percentage))]
        self.ax2.plot(xs, self.sim.neighbor_percentage, marker='o')
        self.ax2.grid(True)


class GUISnapshot(GUI):
    def __init__(self, sim: Simulation, count=6, interval=10):
        assert count in [6, 12]
        assert interval > 0
        self.sim = sim
        self.axs = []
        self.interval = interval
        if count == 6:
            self.fig = plt.figure(figsize=(fig_size[0] * 4, fig_size[1] * 2))
            for i in range(6):
                axi = self.fig.add_subplot(2, 3, i + 1, xlim=[0, X_MAX], ylim=[0, Y_MAX])
                self.axs.append(axi)
        else:
            self.fig = plt.figure(figsize=(fig_size[0] * 3, fig_size[1] * 4))
            for i in range(12):
                axi = self.fig.add_subplot(4, 3, i + 1, xlim=[0, X_MAX], ylim=[0, Y_MAX])
                self.axs.append(axi)
        for axi in self.axs:
            axi.set_xticks(np.arange(0, X_MAX + 1, 5))
            axi.set_yticks(np.arange(0, Y_MAX + 1, 5))

    def draw(self):
        for i, axi in enumerate(self.axs):
            axi.set_title(f"at round {i * self.interval}")
            source_courses = self.sim.cars[0].courses[:i * self.interval + 1]
            xys = list(zip(*source_courses))
            xs = list(map(lambda x: x % X_MAX, list(xys[0])))
            ys = list(map(lambda y: y % Y_MAX, list(xys[1])))
            self.axs[i].plot(xs, ys, "bo", markersize=2)
            self.axs[i].grid(True)

            target_length = i * self.interval
            for car in self.sim.cars:
                acc_length = 0
                for j, pos in enumerate(car.courses[1:]):
                    acc_length += get_dist(*pos, *car.courses[j])
                    if acc_length >= target_length:
                        x = pos[0] % X_MAX
                        y = pos[1] % Y_MAX
                        if car.when <= i * self.interval:
                            self.axs[i].plot(x, y, "go", markersize=4)
                        else:
                            self.axs[i].plot(x, y, "ro", markersize=4)
                        break


if __name__ == '__main__':
    pass
