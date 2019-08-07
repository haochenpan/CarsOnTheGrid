from main2 import *

import time

"""
    random waypoint with step = 1, pause time = 0
"""


class RDCar(Car):

    def set_target(self):
        if self.target_idx == len(self.targets):
            perimeter = 2 * X_MAX + 2 * Y_MAX
            while True:
                target_raw = self.rand.uniform(0, perimeter)
                while target_raw == 0:
                    target_raw = self.rand.uniform(0, perimeter)
                if 0 < target_raw < X_MAX:
                    target = (target_raw, 0)
                elif X_MAX <= target_raw < X_MAX + Y_MAX:
                    target_raw -= X_MAX
                    target = (X_MAX, target_raw)
                elif X_MAX + Y_MAX <= target_raw < 2 * X_MAX + Y_MAX:
                    target_raw -= (X_MAX + Y_MAX)
                    target = (target_raw, Y_MAX)
                else:
                    target_raw -= (2 * X_MAX + Y_MAX)
                    target = (0, target_raw)

                px, py = self.get_prev_target()
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
            if self.when == 0:
                print("the source is generating a target at rd=", len(self.courses) - 1)


"""
    yes, I know, quite ad-hoc now...
"""


class Simulation(Simulation):
    def __init__(self, seed, source_targets=None):
        self.cars = []
        c1 = RDCar(0, seed, SOURCE_POS, source_targets)
        self.cars.append(c1)
        for i in range(1, NUM_OF_CARS):
            cn = RDCar(i, seed)
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
    gui = GUI(*sim.get_data())
    gui.draw()
    gui.show()
