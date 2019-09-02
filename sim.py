from test import *
from time import time


def RWP1_diag1():
    targets = []
    tgts = [(20, 20), (0, 0)]
    for i in range(100):
        targets.extend(tgts)
    return targets


def RWP1_diag2():
    targets = []
    tgts = [(0, 0), (20, 20)]
    for i in range(100):
        targets.extend(tgts)
    return targets


if __name__ == '__main__':
    pass
    MOB = "RWP1"
    RAND_SEED = "%.30f" % time()
    SOURCE_POS = (0, 0)
    SOURCE_COURSE = RWP1_diag1()
    sim1 = RWP1Simulation(RAND_SEED, SOURCE_POS, SOURCE_COURSE)
    sim1.simulate()
    rd = len(sim1.num_of_broadcasters) - 1
    print(rd)
    print(sim1.cars[0].targets)
    print(sim1.cars[0].courses)
    gui = GUISnapshot(sim1, 6, 5)
    gui.draw()
    gui.show()
