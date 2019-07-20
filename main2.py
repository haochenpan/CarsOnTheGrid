import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import redis

X_MAX = 100
Y_MAX = 100
NUM_OF_CARS = 1000
NUM_OF_MOVES = 500
SOURCE_POS = (50, 50)

assert 0 < X_MAX
assert 0 < Y_MAX
assert 0 < NUM_OF_CARS
assert 0 < NUM_OF_MOVES
assert 0 <= SOURCE_POS[0] < X_MAX
assert 0 <= SOURCE_POS[1] < Y_MAX


def get_dist(x1, y1, x2, y2):
    pass
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


"""
    for RWP on torus shape map
"""


class Car:
    def __init__(self, index, seed, pos=None, targets=None):
        assert 0 <= index
        self.index = index
        self.when = 0 if index == 0 else -1
        self.rand = random.Random(f"{seed}+{self.index}")
        if pos is None:
            while True:
                x_pos = self.rand.uniform(0, X_MAX)
                y_pos = self.rand.uniform(0, Y_MAX)
                if x_pos != SOURCE_POS[0] or y_pos != SOURCE_POS[1]:
                    pos = (x_pos, y_pos)
                    break
        self.courses = [pos]
        self.targets = [pos]
        if isinstance(targets, list):
            self.targets.extend(targets)
        self.target_idx = 1

    def move(self):
        step = 1
        while step > 0:
            px, py = self.get_prev_target()
            tx, ty = self.get_target()
            if tx == px and ty == py:  # stand still
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

    def set_target(self):
        if self.target_idx == len(self.targets):
            cx, cy = self.get_pos()
            x_max = cx + 0.5 * X_MAX
            x_min = cx - 0.5 * X_MAX
            y_max = cy + 0.5 * Y_MAX
            y_min = cy - 0.5 * Y_MAX
            tx = self.rand.uniform(x_min, x_max)
            ty = self.rand.uniform(y_min, y_max)

            px, py = self.get_prev_target()
            while tx == px and ty == py:
                tx = self.rand.uniform(x_min, x_max)
                ty = self.rand.uniform(y_min, y_max)

            self.targets.append((tx, ty))
            if self.when == 0:
                print("the source is generating a target at rd=", len(self.courses) - 1)

    def truncate(self):
        self.set_target()
        self.courses = self.courses[-1:]
        self.targets = self.targets[-2:]
        self.target_idx = 1


class Simulation:
    def __init__(self, seed, source_targets=None):
        self.cars = []
        c1 = Car(0, seed, SOURCE_POS, source_targets)
        self.cars.append(c1)
        for i in range(1, NUM_OF_CARS):
            cn = Car(i, seed)
            self.cars.append(cn)

        self.num_of_broadcasters = []  # 0th round (after initialization), and after every move (w or w/o propagate)
        self.neighbor_percentage = []  # same as above

    def cars_move(self):
        for car in self.cars:
            car.move()

    def propagate(self, rd):
        bro_original_positions = [car.get_pos() for car in self.cars if car.when >= 0]
        bro_truncated_positions = list(map(lambda pos: (pos[0] % X_MAX, pos[1] % Y_MAX), bro_original_positions))

        for i, car in enumerate(self.cars):
            if car.when == -1:
                car_x, car_y = car.get_pos()
                car_x, car_y = car_x % X_MAX, car_y % Y_MAX
                for bro_x, bro_y in bro_truncated_positions:
                    if get_dist(car_x, car_y, bro_x, bro_y) <= 1:
                        car.when = rd
                        break

    def calculate_num_of_broadcasters(self):
        broadcasters_cnt = 0
        for car in self.cars:
            if car.when >= 0:
                broadcasters_cnt += 1
        self.num_of_broadcasters.append(broadcasters_cnt)

    def calculate_neighbor_percentage(self):
        original_positions = [car.get_pos() for car in self.cars]
        truncated_positions = list(map(lambda pos: (pos[0] % X_MAX, pos[1] % Y_MAX), original_positions))

        rates = []
        for x1, y1 in truncated_positions:
            num_of_nbrs = -1  # minus itself
            for x2, y2 in truncated_positions:
                dist = get_dist(x1, y1, x2, y2)
                if dist <= 1:
                    num_of_nbrs += 1
            rate = num_of_nbrs / NUM_OF_CARS
            rates.append(rate)
        self.neighbor_percentage.append(sum(rates))

    def simulate(self, exceed_num_of_moves=False):
        for _ in range(50):
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
            # self.calculate_neighbor_percentage()
            # print(self.num_of_broadcasters[-1])
            # print(self.neighbor_percentage[-1])
            if not exceed_num_of_moves and rd == NUM_OF_MOVES:
                break
            rd += 1

    def get_data(self):
        courses = [car.courses for car in self.cars]
        targets = [car.targets for car in self.cars]

        return courses, targets, self.num_of_broadcasters, self.neighbor_percentage


class GUI:
    def __init__(self, courses, targets, broadcasters, neighbors):
        self.courses = courses
        self.targets = targets
        self.broadcasters = broadcasters
        self.neighbors = neighbors

        self.fig = plt.figure(figsize=(18, 9))
        self.ax1 = self.fig.add_subplot(121, xlim=[0, X_MAX], ylim=[0, Y_MAX])
        self.ax1.set_xticks(np.arange(0, X_MAX + 1, 5))
        self.ax1.set_yticks(np.arange(0, Y_MAX + 1, 5))

        # self.ax2 = self.fig.add_subplot(122, xlim=[0, NUM_OF_MOVES], ylim=[0, 0.002])  ###
        x_max = NUM_OF_MOVES if len(self.broadcasters) <= NUM_OF_MOVES else len(self.broadcasters)
        self.ax3 = self.fig.add_subplot(122, xlim=[x_max - 500, x_max], ylim=[0, NUM_OF_CARS])

    def draw(self):
        for courses in self.courses:
            last_x, last_y = courses[-1]
            last_x, last_y = last_x % X_MAX, last_y % Y_MAX
            self.ax1.plot(last_x, last_y, "go", markersize=2)

        source_courses = self.courses[0]
        xys = list(zip(*source_courses))
        xs = list(map(lambda x: x % X_MAX, list(xys[0])))
        ys = list(map(lambda y: y % Y_MAX, list(xys[1])))
        self.ax1.plot(xs, ys, "bo", markersize=2)

        source_targets = self.targets[0]
        xys = list(zip(*source_targets))
        xs = list(map(lambda x: x % X_MAX, list(xys[0])))
        ys = list(map(lambda y: y % Y_MAX, list(xys[1])))
        self.ax1.plot(xs, ys, "ro", markersize=4)

        self.ax1.set_xlabel("x axis")
        self.ax1.set_ylabel("y axis")
        self.ax1.set_title("source's position")
        self.ax1.grid(True)

        # round vs # of broadcasters
        xs = [i for i in range(len(self.broadcasters))]
        self.ax3.plot(xs, self.broadcasters, marker='o', markersize=3)

        self.ax3.set_xlabel("simulation round")
        self.ax3.set_ylabel("# of msg received cars")
        self.ax3.set_title("# of msg received cars vs. simulation round \n")
        self.ax3.grid(True)

    def show(self):
        plt.show()
        plt.clf()
        plt.close()

    def save(self, name):
        plt.tight_layout()
        plt.savefig(f"{name}.png")
        plt.clf()
        plt.close()


if __name__ == '__main__':
    pass
    r = redis.Redis(host='localhost', port=6379, db=0)
    targets = {
        # 0: [(100, 100), (0, 0), (100, 100)],
        # 1: [(100, 100), (100, 100)],
        # 2: [(50, 50), (50, 50)],
        # 3: [(50, 50), (100, 0), (50, 50), (0, 0),
        #     (50, 50), (100, 0), (50, 50), (0, 0),
        #     (50, 50), (100, 0), (50, 50), (0, 0)],
        # 4: [(25, 25), (25, 75), (75, 75), (75, 25),
        #     (25, 25), (25, 75), (75, 75), (75, 25),
        #     (25, 25), (25, 75), (75, 75), (75, 25),
        #     (25, 25), (25, 75), (75, 75), (75, 25),
        #     (25, 25), (25, 75), (75, 75), (75, 25)],
        # 5: [(10, 10), (10, 90), (90, 90), (90, 10),
        #     (10, 10), (10, 90), (90, 90), (90, 10),
        #     (10, 10), (10, 90), (90, 90), (90, 10),
        #     (10, 10), (10, 90), (90, 90), (90, 10)],
        # 6: [(75, 75), (75, 25), (25, 25), (25, 75),
        #     (75, 75), (75, 25), (25, 25), (25, 75),
        #     (75, 75), (75, 25), (25, 25), (25, 75),
        #     (75, 75), (75, 25), (25, 25), (25, 75)],
        # 7: [(90, 90), (90, 10), (10, 10), (10, 90),
        #     (90, 90), (90, 10), (10, 10), (10, 90),
        #     (90, 90), (90, 10), (10, 10), (10, 90)],  ###
        # 8: [(50, 100), (50, 0), (50, 100), (50, 0), (50, 100), (50, 0)],
        # 9: [(50, 100), (50, 100)],
        # 10: [(50, 50), (50, 50)],
        # 11: [(50, 50), (100, 50), (50, 50), (50, 0),
        #      (50, 50), (100, 50), (50, 50), (50, 0),
        #      (50, 50), (100, 50), (50, 50), (50, 0)],
        # 12: [(50, 25),
        #      (25, 25), (25, 75), (75, 75), (75, 25),
        #      (25, 25), (25, 75), (75, 75), (75, 25),
        #      (25, 25), (25, 75), (75, 75), (75, 25),
        #      (25, 25), (25, 75), (75, 75), (75, 25),
        #      (25, 25), (25, 75), (75, 75), (75, 25)],
        # 13: [(50, 10),
        #      (10, 10), (10, 90), (90, 90), (90, 10),
        #      (10, 10), (10, 90), (90, 90), (90, 10),
        #      (10, 10), (10, 90), (90, 90), (90, 10),
        #      (10, 10), (10, 90), (90, 90), (90, 10)],
        # 14: [(50, 75),
        #      (75, 75), (75, 25), (25, 25), (25, 75),
        #      (75, 75), (75, 25), (25, 25), (25, 75),
        #      (75, 75), (75, 25), (25, 25), (25, 75),
        #      (75, 75), (75, 25), (25, 25), (25, 75)],
        # 15: [(50, 90),
        #      (90, 90), (90, 10), (10, 10), (10, 90),
        #      (90, 90), (90, 10), (10, 10), (10, 90),
        #      (90, 90), (90, 10), (10, 10), (10, 90)],  ###
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
        for k, v in targets.items():
            sim = Simulation(RAND_SEED, v)
            sim.simulate(True)
            # gui = GUI(*sim.get_data())
            # gui.draw()
            # gui.show()
            results.append(len(sim.num_of_broadcasters) - 1)
            # print("round=", len(sim.num_of_broadcasters) - 1)
        print(results)
        r_set_name = f"torus-{SOURCE_POS}-100"
        r.sadd(r_set_name, str((RAND_SEED, results)))
