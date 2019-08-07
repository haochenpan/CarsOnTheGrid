from main2 import *


class MGCar(Car):
    def __init__(self, index, seed, pos=None, targets=None):
        assert 0 <= index
        self.index = index
        self.when = 0 if index == 0 else -1
        self.rand = random.Random(f"{seed}+{self.index}")
        if pos is None:
            while True:
                x_pos = self.rand.choice([i for i in range(0, X_MAX + 1)])
                y_pos = self.rand.choice([i for i in range(0, Y_MAX + 1)])
                if x_pos != SOURCE_POS[0] or y_pos != SOURCE_POS[1]:
                    pos = (x_pos, y_pos)
                    break
        self.courses = [pos]
        self.targets = [pos]
        if isinstance(targets, list):
            self.targets.extend(targets)
        self.target_idx = 1

    def set_target(self):
        if self.target_idx == len(self.targets):
            cx, cy = self.get_pos()
            possible_dirs = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]  # left, right, down, up

            if cx == 0:
                possible_dirs.remove((cx - 1, cy))
            if cx == X_MAX:
                possible_dirs.remove((cx + 1, cy))
            if cy == 0:
                possible_dirs.remove((cx, cy - 1))
            if cy == Y_MAX:
                possible_dirs.remove((cx, cy + 1))
            assert len(possible_dirs) in [2, 3, 4]

            if len(possible_dirs) == 2:
                weights = [0.5, 0.5]
            elif len(possible_dirs) == 3:
                weights = [1 / 3, 1 / 3, 1 / 3]
            else:
                weights = [0.25, 0.25, 0.25, 0.25]

            if len(self.courses) == 1:
                dir = random.choices(possible_dirs, weights)[0]
            else:
                last_x, last_y = self.courses[-2]
                assert (last_x, last_y) in possible_dirs
                last_idx = possible_dirs.index((last_x, last_y))

                if (last_x, last_y) == (cx - 1, cy):
                    opposite = (cx + 1, cy)
                elif (last_x, last_y) == (cx + 1, cy):
                    opposite = (cx - 1, cy)
                elif (last_x, last_y) == (cx, cy - 1):
                    opposite = (cx, cy + 1)
                else:
                    opposite = (cx, cy - 1)
                plus_idx = possible_dirs.index(opposite) if opposite in possible_dirs else -1

                weight, weights[last_idx] = weights[last_idx], 0
                if plus_idx == -1:
                    new_weights = []
                    for wei in weights:
                        if wei == 0:
                            new_weights.append(0)
                        else:
                            new_weights.append(wei + weight * (1 / len(weights[1:])))
                else:
                    weights[plus_idx] += weight
                dir = random.choices(possible_dirs, weights)[0]
            self.targets.append(dir)

    def truncate(self):
        self.set_target()
        self.courses = self.courses[-1:]
        self.targets = self.targets[-2:]
        self.target_idx = 1


"""
    yes, I know, quite ad-hoc now...
"""


class Simulation(Simulation):
    def __init__(self, seed, source_targets=None):
        self.cars = []
        c1 = MGCar(0, seed, SOURCE_POS, source_targets)
        self.cars.append(c1)
        for i in range(1, NUM_OF_CARS):
            cn = MGCar(i, seed)
            self.cars.append(cn)

        self.num_of_broadcasters = []  # 0th round (after initialization), and after every move (w or w/o propagate)
        self.neighbor_percentage = []  # same as above

    def propagate(self, rd):
        bro_original_positions = [car.get_pos() for car in self.cars if car.when >= 0]

        for i, car in enumerate(self.cars):
            if car.when == -1:
                car_x, car_y = car.get_pos()
                for bro_x, bro_y in bro_original_positions:
                    if get_dist(car_x, car_y, bro_x, bro_y) <= 1:
                        car.when = rd
                        break

    def calculate_neighbor_percentage(self):
        original_positions = [car.get_pos() for car in self.cars]

        rates = []
        for x1, y1 in original_positions:
            num_of_nbrs = -1  # minus itself
            for x2, y2 in original_positions:
                dist = get_dist(x1, y1, x2, y2)
                if dist <= 1:
                    num_of_nbrs += 1
            rate = num_of_nbrs / NUM_OF_CARS
            rates.append(rate)
        self.neighbor_percentage.append(sum(rates))


if __name__ == '__main__':
    pass
    RAND_SEED = "%.20f" % time.time()
    sim = Simulation(RAND_SEED)
    sim.simulate(True)
    data = sim.get_data()
    courses = data[0][0]  # source
    print(courses)
