from help import *


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


class RWP1Car(Car):
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


class RWP2Car(RWP1Car):
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


class Simulation:
    def __init__(self):
        self.cars = [CAR_CLASS(0, RAND_SEED, SOURCE_POS, SOURCE_COURSE)]
        self.cars.extend([CAR_CLASS(i, RAND_SEED) for i in range(1, NUM_OF_CARS)])

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


class RWP1Simulation(Simulation):
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


class RWP2Simulation(Simulation):
    def propagate(self, rd):
        broadcaster_pos_list = [car.get_pos() for car in self.cars if car.when >= 0]
        mod_pos_list = list(map(lambda pos: (pos[0] % X_MAX, pos[1] % Y_MAX), broadcaster_pos_list))
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
    def __init__(self, courses, targets, num_of_broadcasters, neighbor_percentage):
        self.courses = courses
        self.targets = targets
        self.num_of_broadcasters = num_of_broadcasters
        self.neighbor_percentage = neighbor_percentage

        self.fig = plt.figure(figsize=(18, 9))
        # self.fig = plt.figure(figsize=(27, 9))  ###
        self.ax1 = self.fig.add_subplot(121, xlim=[0, X_MAX], ylim=[0, Y_MAX])  ###
        self.ax1.set_xticks(np.arange(0, X_MAX + 1, 5))
        self.ax1.set_yticks(np.arange(0, Y_MAX + 1, 5))

        # self.ax2 = self.fig.add_subplot(132, xlim=[0, NUM_OF_MOVES], ylim=[0, 0.002])  ###
        x_max = NUM_OF_MOVES if len(self.num_of_broadcasters) <= NUM_OF_MOVES else len(self.num_of_broadcasters)
        self.ax3 = self.fig.add_subplot(122, xlim=[x_max - 500, x_max], ylim=[0, NUM_OF_CARS])  ###

    def draw(self):
        for course in self.courses:
            first_x, first_y = course[0]
            # print(first_x, first_y)
            self.ax1.plot(first_x, first_y, "go", markersize=2)

        # source_courses = self.courses[0]
        # xys = list(zip(*source_courses))
        # xs = list(map(lambda x: x % X_MAX, list(xys[0])))
        # ys = list(map(lambda y: y % Y_MAX, list(xys[1])))
        # self.ax1.plot(xs, ys, "bo", markersize=2)
        #
        # source_targets = self.targets[0]
        # xys = list(zip(*source_targets))
        # xs = list(map(lambda x: x % X_MAX, list(xys[0])))
        # ys = list(map(lambda y: y % Y_MAX, list(xys[1])))
        # self.ax1.plot(xs, ys, "ro", markersize=4)

        self.ax1.set_xlabel("x axis")
        self.ax1.set_ylabel("y axis")
        self.ax1.set_title("source's position")
        self.ax1.grid(True)

        # average MN neighbor percentage
        # xs = [i for i in range(len(self.neighbor_percentage))]
        # self.ax2.plot(xs, self.neighbor_percentage, marker='o')
        # self.ax2.grid(True)

        # round vs # of broadcasters
        xs = [i for i in range(len(self.num_of_broadcasters))]
        self.ax3.plot(xs, self.num_of_broadcasters, marker='o', markersize=3)

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
    pos1_list, pos2_list, pos3_list, pos4_list, pos5_list = [], [], [], [], []
    CAR_CLASS = RWP2Car
    SOURCE_COURSE = []
    SOURCE_POS = (0, 0)
    PRE_RUN_COUNT = 100

    for i in range(50):
        RAND_SEED = "%.20f" % time.time()
        SOURCE_POS = (0, 0)
        sim1 = RWP2Simulation()
        sim1.simulate()
        pos1_list.append(len(sim1.num_of_broadcasters) - 1)
        # pos1_list.append(get_index(sim1.num_of_broadcasters))

        SOURCE_POS = (5, 5)
        sim2 = RWP2Simulation()
        sim2.simulate()
        pos2_list.append(len(sim2.num_of_broadcasters) - 1)
        #
        SOURCE_POS = (25, 25)
        sim3 = RWP2Simulation()
        sim3.simulate()
        pos3_list.append(len(sim3.num_of_broadcasters) - 1)

        SOURCE_POS = (50, 50)
        sim4 = RWP2Simulation()
        sim4.simulate()
        pos4_list.append(len(sim4.num_of_broadcasters) - 1)
        #
        SOURCE_POS = (75, 75)
        sim5 = RWP2Simulation()
        sim5.simulate()
        pos5_list.append(len(sim5.num_of_broadcasters) - 1)
        #
        print("sim 1 rounds to finish: ", len(sim1.num_of_broadcasters) - 1)
        print("sim 2 rounds to finish: ", len(sim2.num_of_broadcasters) - 1)
        print("sim 3 rounds to finish: ", len(sim3.num_of_broadcasters) - 1)
        print("sim 4 rounds to finish: ", len(sim4.num_of_broadcasters) - 1)
        print("sim 5 rounds to finish: ", len(sim5.num_of_broadcasters) - 1)

        # gui = GUI(*sim1.summary())
        # gui.draw()
        # gui.save(f"{i}-{RAND_SEED}-1")
        # gui = GUI(*sim2.summary())
        # gui.draw()
        # gui.save(f"{i}-{RAND_SEED}-2")
        # gui = GUI(*sim3.summary())
        # gui.draw()
        # gui.save(f"{i}-{RAND_SEED}-3")
        # gui = GUI(*sim4.summary())
        # gui.draw()
        # gui.save(f"{i}-{RAND_SEED}-4")
        # gui = GUI(*sim5.summary())
        # gui.draw()
        # gui.save(f"{i}-{RAND_SEED}-5")

    print(pos1_list, sum(pos1_list), sum(pos1_list) / len(pos1_list))
    print(pos2_list, sum(pos2_list), sum(pos2_list) / len(pos2_list))
    print(pos3_list, sum(pos3_list), sum(pos3_list) / len(pos3_list))
    print(pos4_list, sum(pos4_list), sum(pos4_list) / len(pos4_list))
    print(pos5_list, sum(pos5_list), sum(pos5_list) / len(pos5_list))
    # gui = GUI(*sim.summary())
    # gui.draw()
    # gui.show()
