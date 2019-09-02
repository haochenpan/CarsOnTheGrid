from random import Random
import matplotlib.pyplot as plt
import numpy as np
from redis import Redis
from help import *

r = Redis(host='localhost', port=6379, db=0)


class Car:
    def __init__(self, index, seed, source_pos, is_source=False, targets=None):

        assert 0 <= index
        self.index = index
        self.when = 0 if index == 0 else -1
        self.rand = Random(f"{seed}+{self.index}")
        if is_source:
            pos = source_pos
        else:
            while True:
                x_pos = self.rand.uniform(0, X_MAX)
                y_pos = self.rand.uniform(0, Y_MAX)
                if x_pos != source_pos[0] or y_pos != source_pos[1]:
                    pos = (x_pos, y_pos)
                    break
        self.courses = [pos]
        self.targets = [pos]
        if targets is not None: self.targets.extend(targets)
        self.target_idx = 1

    def set_target(self):
        pass

    def move(self):
        pass

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
            # if source and see a repeated target
            # won't move but stay at the current pos/target
            px, py = self.get_prev_target()
            tx, ty = self.get_target()
            if tx == px and ty == py:
                pos = (tx, ty)
                self.courses.append(pos)
                return

            cx, cy = self.get_pos()
            dist = get_dist(cx, cy, tx, ty)
            # if dist != 1:
            #     print("errpr!", cx, cy, tx, ty)
            if step >= dist:
                pos = (tx, ty)
                self.courses.append(pos)
                self.target_idx += 1
                step -= dist
            else:
                dx = (tx - cx) * step / dist
                dy = (ty - cy) * step / dist
                cx = cx + dx
                cy = cy + dy
                pos = (cx, cy)
                self.courses.append(pos)
                return


class RWP1Car(SynCar):
    def set_target(self):
        if self.target_idx == len(self.targets):
            px, py = self.get_prev_target()

            # if source and reached the last target,
            # append the previous target so that it won't
            # generate a new one
            if self.index == 0:
                self.targets.append((px, py))
                return

            tx = self.rand.uniform(0, X_MAX)
            ty = self.rand.uniform(0, Y_MAX)
            while tx == px and ty == py:
                tx = self.rand.uniform(0, X_MAX)
                ty = self.rand.uniform(0, Y_MAX)
            self.targets.append((tx, ty))


class RWP2Car(SynCar):
    def set_target(self):
        if self.target_idx == len(self.targets):
            px, py = self.get_prev_target()

            # if source and reached the last target,
            # append the previous target so that it won't
            # generate a new one
            if self.index == 0:
                self.targets.append((px, py))
                return

            cx, cy = self.get_pos()
            x_max = cx + 0.5 * X_MAX
            x_min = cx - 0.5 * X_MAX
            y_max = cy + 0.5 * Y_MAX
            y_min = cy - 0.5 * Y_MAX
            tx = self.rand.uniform(x_min, x_max)
            ty = self.rand.uniform(y_min, y_max)
            while tx == px and ty == py:
                tx = self.rand.uniform(0, X_MAX)
                ty = self.rand.uniform(0, Y_MAX)
            self.targets.append((tx, ty))


class RDCar(SynCar):
    def set_target(self):
        if self.target_idx == len(self.targets):
            px, py = self.get_prev_target()

            # if source and reached the last target,
            # append the previous target so that it won't
            # generate a new one
            if self.index == 0:
                self.targets.append((px, py))
                return

            max_target = 2 * X_MAX + 2 * Y_MAX
            while True:
                raw_target = self.rand.uniform(0, max_target)
                if 0 <= raw_target < X_MAX:
                    target = (raw_target, 0)
                elif X_MAX <= raw_target < X_MAX + Y_MAX:
                    raw_target -= X_MAX
                    target = (X_MAX, raw_target)
                elif X_MAX + Y_MAX <= raw_target < 2 * X_MAX + Y_MAX:
                    raw_target -= (X_MAX + Y_MAX)
                    target = ((X_MAX - raw_target), Y_MAX)
                else:
                    raw_target -= (2 * X_MAX + Y_MAX)
                    target = (0, (Y_MAX - raw_target))

                if px == 0 and target[0] == 0:
                    continue
                if px == X_MAX and target[0] == X_MAX:
                    continue
                if py == 0 and target[1] == 0:
                    continue
                if py == Y_MAX and target[1] == Y_MAX:
                    continue
                break
            self.targets.append(target)


class MG1Car(Car):
    def __init__(self, index, seed, source_pos, is_source=False, targets=None):
        super().__init__(index, seed, source_pos, is_source, targets)
        if is_source:
            pos = source_pos
        else:
            while True:
                x_pos = self.rand.choice([i for i in range(0, X_MAX + 1)])
                y_pos = self.rand.choice([i for i in range(0, Y_MAX + 1)])
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

    def set_target(self):
        if self.target_idx == len(self.targets):

            px, py = self.get_prev_target()

            # if source and reached the last target,
            # append the previous target so that it won't
            # generate a new one
            if self.index == 0:
                self.targets.append((px, py))
                return

            cx, cy = self.get_pos()
            dirs = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]
            if cx == 0:
                dirs.remove((cx - 1, cy))
            elif cx == X_MAX:
                dirs.remove((cx + 1, cy))
            if cy == 0:
                dirs.remove((cx, cy - 1))
            elif cy == Y_MAX:
                dirs.remove((cx, cy + 1))
            assert len(dirs) in [2, 3, 4]
            if len(dirs) == 2:
                weights = [0.5 for _ in range(2)]
            elif len(dirs) == 3:
                weights = [1 / 3 for _ in range(3)]
            else:
                weights = [0.25 for _ in range(4)]

            if len(self.courses) == 1:
                dir = self.rand.choices(dirs, weights)
                assert len(dir) == 1
                dir = dir[0]
            else:
                last_x, last_y = self.courses[-2]
                assert (last_x, last_y) in dirs
                last_idx = dirs.index((last_x, last_y))

                if (last_x, last_y) == (cx - 1, cy):
                    opposite = (cx + 1, cy)
                elif (last_x, last_y) == (cx + 1, cy):
                    opposite = (cx - 1, cy)
                elif (last_x, last_y) == (cx, cy - 1):
                    opposite = (cx, cy + 1)
                else:
                    opposite = (cx, cy - 1)

                plus_idx = dirs.index(opposite) if opposite in dirs else -1
                plus_weight, weights[last_idx] = weights[last_idx], 0
                if plus_idx != -1:
                    weights[plus_idx] += plus_weight
                else:
                    for i, wei in enumerate(weights):
                        if wei != 0:
                            weights[i] = wei + plus_weight * (1 / (len(weights) - 1))
                dir = self.rand.choices(dirs, weights)
                assert len(dir) == 1
                dir = dir[0]
            self.targets.append(dir)


class MG2Car(MG1Car):
    def __init__(self, index, seed, source_pos, is_source=False, targets=None):
        super().__init__(index, seed, source_pos, is_source, targets)
        if is_source:
            pos = source_pos
        else:
            while True:
                x_pos = self.rand.choice([i for i in range(0, X_MAX)])
                y_pos = self.rand.choice([i for i in range(0, Y_MAX)])
                if x_pos != source_pos[0] or y_pos != source_pos[1]:
                    pos = (x_pos, y_pos)
                    break
        self.courses = [pos]
        self.targets = [pos]
        if targets is not None: self.targets.extend(targets)

    def set_target(self):
        if self.target_idx == len(self.targets):

            px, py = self.get_prev_target()

            # if source and reached the last target,
            # append the previous target so that it won't
            # generate a new one
            if self.index == 0:
                print("reached")
                self.targets.append((px, py))
                return

            cx, cy = self.get_pos()
            dirs = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]
            dirs = [(x % X_MAX, y % Y_MAX) for (x, y) in dirs]
            weights = [0.25 for _ in range(4)]

            if len(self.courses) == 1:
                dir = self.rand.choices(dirs, weights)
                assert len(dir) == 1
                dir = dir[0]
            else:
                last_x, last_y = self.courses[-2]
                last_x, last_y = last_x % X_MAX, last_y % Y_MAX
                assert (last_x, last_y) in dirs
                last_idx = dirs.index((last_x, last_y))

                if (last_x, last_y) == ((cx - 1) % X_MAX, cy % Y_MAX):
                    opposite = (cx + 1, cy)
                elif (last_x, last_y) == ((cx + 1) % X_MAX, cy % Y_MAX):
                    opposite = (cx - 1, cy)
                elif (last_x, last_y) == (cx % X_MAX, (cy - 1) % Y_MAX):
                    opposite = (cx, cy + 1)
                else:
                    opposite = (cx, cy - 1)
                opposite = opposite[0] % X_MAX, opposite[1] % Y_MAX

                # in torus map, the opposite is always an option
                plus_idx = dirs.index(opposite)
                plus_weight, weights[last_idx] = weights[last_idx], 0
                weights[plus_idx] += plus_weight

                dir = self.rand.choices(dirs, weights)
                assert len(dir) == 1
                dir = dir[0]
            # dir = round(dir[0], 0), round(dir[1], 0)
            self.targets.append(dir)


class Simulation:
    def __init__(self):
        self.cars = []
        self.num_of_broadcasters = []
        self.neighbor_percentage = []

    def cars_move(self):
        [car.move() for car in self.cars]

    def propagate(self, rd):
        pass

    def calculate_num_of_broadcasters(self):
        num = 0
        for car in self.cars:
            if car.when >= 0:
                num += 1
        print(num)
        self.num_of_broadcasters.append(num)

    def calculate_neighbor_percentage(self):
        pass

    def simulate(self):
        for _ in range(PRE_RUN_COUNT):
            for car in self.cars[1:]:
                car.move()
        for car in self.cars[1:]:
            car.truncate()
        self.calculate_num_of_broadcasters()
        # self.calculate_neighbor_percentage()

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


class TorusSynSimulation(Simulation):
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


class RWP1Simulation(Simulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(RWP1Car(0, seed, source_pos, True, source_source))
        self.cars.extend([RWP1Car(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


class RWP2Simulation(TorusSynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(RWP2Car(0, seed, source_pos, True, source_source))
        self.cars.extend([RWP2Car(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


class RDSimulation(SynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(RDCar(0, seed, source_pos, True, source_source))
        self.cars.extend([RDCar(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


class MG1Simulation(SynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(MG1Car(0, seed, source_pos, True, source_source))
        self.cars.extend([MG1Car(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


class MG2Simulation(TorusSynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(MG2Car(0, seed, source_pos, True, source_source))
        self.cars.extend([MG2Car(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


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


class GUI1(GUI):
    def __init__(self, sim: Simulation):
        self.sim = sim
        self.fig = plt.figure(figsize=(18, 9))
        self.ax1 = self.fig.add_subplot(121, xlim=[0, X_MAX], ylim=[0, Y_MAX])
        self.ax1.set_xticks(np.arange(0, X_MAX + 1, 5))
        self.ax1.set_yticks(np.arange(0, Y_MAX + 1, 5))

    def draw(self):
        # draw all final positions:
        for car in self.sim.cars:
            fx, fy = car.courses[-1]
            self.ax1.plot(fx, fy, "go", markersize=2)

        # for RD, to validate target positions
        # for car_targets in self.targets:
        #     xys = list(zip(*car_targets))
        #     xs = list(map(lambda x: x, list(xys[0])))
        #     ys = list(map(lambda y: y, list(xys[1])))
        #     self.ax1.plot(xs, ys, "ro", markersize=2)

        source_courses = self.sim.cars[0].courses
        xys = list(zip(*source_courses))
        xs = list(map(lambda x: x % X_MAX, list(xys[0])))
        ys = list(map(lambda y: y % Y_MAX, list(xys[1])))
        self.ax1.plot(xs, ys, "bo", markersize=2)

        source_targets = self.sim.cars[0].targets
        xys = list(zip(*source_targets))
        xs = list(map(lambda x: x % X_MAX, list(xys[0])))
        ys = list(map(lambda y: y % Y_MAX, list(xys[1])))
        self.ax1.plot(xs, ys, "ro", markersize=4)

        self.ax1.set_xlabel("x axis")
        self.ax1.set_ylabel("y axis")
        self.ax1.set_title("source's position")
        self.ax1.grid(True)


class GUIHeatMap(GUI1):
    def __init__(self, sim: Simulation):
        super().__init__(sim)
        self.ax3 = self.fig.add_subplot(122)

    def draw(self):
        super().draw()
        hot_map = [[0 for _ in range(X_MAX)] for _ in range(Y_MAX)]
        for car in self.sim.cars[1:]:
            for target in car.courses:
                int_target_x = int(target[0]) % X_MAX
                int_target_y = int(target[1]) % Y_MAX
                hot_map[int_target_y][int_target_x] += 1
        hot_map = list(reversed(hot_map))
        im = self.ax3.imshow(hot_map)
        cbar = self.fig.colorbar(im, ax=self.ax3)
        self.ax3.set_title("courses heat map")


class GUINumBro(GUI1):
    def __init__(self, sim: Simulation):
        super().__init__(sim)
        x_max = NUM_OF_MOVES if len(self.sim.num_of_broadcasters) <= NUM_OF_MOVES else len(self.sim.num_of_broadcasters)
        self.ax3 = self.fig.add_subplot(122, xlim=[x_max - 500, x_max], ylim=[0, NUM_OF_CARS])  ###

    def draw(self):
        super().draw()
        xs = [i for i in range(len(self.sim.num_of_broadcasters))]
        self.ax3.plot(xs, self.sim.num_of_broadcasters, marker='o', markersize=3)

        self.ax3.set_xlabel("simulation round")
        self.ax3.set_ylabel("# of msg received cars")
        self.ax3.set_title("# of msg received cars vs. simulation round \n")
        self.ax3.grid(True)


class GUINumNei(GUI1):
    def __init__(self, sim: Simulation):
        super().__init__(sim)
        self.ax2 = self.fig.add_subplot(132, xlim=[0, NUM_OF_MOVES], ylim=[0, 0.002])  ###

    def draw(self):
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
            self.fig = plt.figure(figsize=(9 * 3, 9 * 2))
            for i in range(6):
                axi = self.fig.add_subplot(2, 3, i + 1, xlim=[0, X_MAX], ylim=[0, Y_MAX])
                self.axs.append(axi)
        else:
            self.fig = plt.figure(figsize=(9 * 4, 9 * 3))
            for i in range(12):
                axi = self.fig.add_subplot(3, 4, i + 1, xlim=[0, X_MAX], ylim=[0, Y_MAX])
                self.axs.append(axi)
        for axi in self.axs:
            axi.set_xticks(np.arange(0, X_MAX + 1, 5))
            axi.set_yticks(np.arange(0, Y_MAX + 1, 5))

    def draw(self):
        for i, axi in enumerate(self.axs):
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
