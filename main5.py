from main4 import *


class TMGCar(MGCar):

    def set_target(self):
        if self.target_idx == len(self.targets):
            cx, cy = self.get_pos()
            print(cx, cy)
            possible_dirs = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]  # left, right, down, up
            print(possible_dirs)
            possible_dirs = [(x % X_MAX, y % Y_MAX) for (x, y) in possible_dirs]
            print(possible_dirs)
            weights = [0.25 for _ in range(4)]
            if len(self.courses) == 1:
                dir = random.choices(possible_dirs, weights)[0]
            else:
                last_x, last_y = self.courses[-2]
                last_x, last_y = last_x % X_MAX, last_y % Y_MAX
                assert (last_x, last_y) in possible_dirs
                last_idx = possible_dirs.index((last_x, last_y))

                if (last_x, last_y) == ((cx - 1) % X_MAX, cy % Y_MAX):
                    opposite = (cx + 1, cy)
                elif (last_x, last_y) == ((cx + 1) % X_MAX, cy % Y_MAX):
                    opposite = (cx - 1, cy)
                elif (last_x, last_y) == (cx % X_MAX, (cy - 1) % Y_MAX):
                    opposite = (cx, cy + 1)
                else:
                    opposite = (cx, cy - 1)
                opposite = opposite[0] % X_MAX, opposite[1] % Y_MAX
                plus_idx = possible_dirs.index(opposite)

                weight, weights[last_idx] = weights[last_idx], 0
                weights[plus_idx] += weight
                dir = random.choices(possible_dirs, weights)[0]
            self.targets.append(dir)


class Simulation(Simulation):
    def __init__(self, seed, source_targets=None):
        self.cars = []
        c1 = TMGCar(0, seed, SOURCE_POS, source_targets)
        self.cars.append(c1)
        for i in range(1, NUM_OF_CARS):
            cn = MGCar(i, seed)
            self.cars.append(cn)

        self.num_of_broadcasters = []  # 0th round (after initialization), and after every move (w or w/o propagate)
        self.neighbor_percentage = []  # same as above


if __name__ == '__main__':
    pass
    RAND_SEED = "%.20f" % time.time()
    sim = Simulation(RAND_SEED)
    sim.simulate(True)
    data = sim.get_data()
    courses = data[0][0]  # source
    print(courses)
