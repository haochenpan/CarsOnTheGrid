from time import time
from base import *


class RWP1Car(SynCar):
    def set_target(self):
        if self.target_idx == len(self.targets):
            px, py = self.get_prev_target()

            # if the source has reached the last target,
            # append the previous target so that it won't generate a new one
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

            # if the source has reached the last target,
            # append the previous target so that it won't generate a new one
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
                tx = self.rand.uniform(x_min, x_max)
                ty = self.rand.uniform(y_min, y_max)
            self.targets.append((tx, ty))


class RDCar(SynCar):
    def set_target(self):
        if self.target_idx == len(self.targets):
            px, py = self.get_prev_target()

            # if the source has reached the last target,
            # append the previous target so that it won't generate a new one
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


class MG1Car(SynMGCar):
    def __init__(self, index, seed, source_pos, targets=None):
        super().__init__(index, seed, source_pos, targets, 1)

    def set_target(self):
        if self.target_idx == len(self.targets):
            px, py = self.get_prev_target()

            # if the source has reached the last target,
            # append the previous target so that it won't generate a new one
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


class MG2Car(SynMGCar):
    def __init__(self, index, seed, source_pos, targets=None):
        super().__init__(index, seed, source_pos, targets, 2)

    def set_target(self):
        if self.target_idx == len(self.targets):

            px, py = self.get_prev_target()

            # if the source has reached the last target,
            # append the previous target so that it won't generate a new one
            if self.index == 0:
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


class RWP1Simulation(SynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(RWP1Car(0, seed, source_pos, source_source))
        self.cars.extend([RWP1Car(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


class RWP2Simulation(TorSynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(RWP2Car(0, seed, source_pos, source_source))
        self.cars.extend([RWP2Car(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


class RDSimulation(SynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(RDCar(0, seed, source_pos, source_source))
        self.cars.extend([RDCar(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


class MG1Simulation(SynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(MG1Car(0, seed, source_pos, source_source))
        self.cars.extend([MG1Car(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


class MG2Simulation(TorSynSimulation):
    def __init__(self, seed, source_pos, source_source):
        super().__init__()
        self.cars.append(MG2Car(0, seed, source_pos, source_source))
        self.cars.extend([MG2Car(i, seed, source_pos) for i in range(1, NUM_OF_CARS)])


if __name__ == '__main__':
    pass
    typ = "RWP2"
    RAND_SEED = "%.30f" % time()
    SOURCE_POS = (0, 0)
    sim = RWP2Simulation(RAND_SEED, SOURCE_POS, RWP2_zigzag_14())
    sim.simulate()
    print(sim.cars[0].courses)

    gui = GUINumBro(sim, True, False)
    gui.draw()
    gui.save(f"{typ}_x{X_MAX}_y{Y_MAX}_c{NUM_OF_CARS}_14")
