from test import *
from time import time

if __name__ == '__main__':
    pass
    MOB = "RWP2"
    RAND_SEED = "%.30f" % time()
    SOURCE_POS = (10, 10)
    SOURCE_COURSE = [(i, 10) for i in range(11, 3600)]
    sim1 = RWP2Simulation(RAND_SEED, SOURCE_POS, SOURCE_COURSE)
    sim1.simulate()
    rd = len(sim1.num_of_broadcasters) - 1
    print(rd)
    print(sim1.cars[0].targets)
    print(sim1.cars[0].courses)
    gui = GUIHeatMap(sim1)
    gui.draw()
    gui.show()
