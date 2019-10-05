from time import time
from base import *
from redis import Redis

"""
    multi-source, specified by NUM_OF_SRCS
    size of pos_course_dict must >= NUM_OF_SRCS
    if >, extra ones are positions and courses of non-source
    if a source pass the last specified target, it will generate one
    unless specifying a target in the course that is the same as the last one
"""

r = Redis(host='localhost', port=6379, db=0)


def sim():
    MOB = "RWP2"

    for i in range(300):
        seed = "%.30f" % time()
        print(i, seed)

        pos_course_dict = {
            (0, 0): [(500, 500)],
            (490, 490): [(0, 0)],
        }
        sim = RWP2NSimulation(seed, pos_course_dict)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-2diag", str((rd, seed)))
        print(rd)

        pos_course_dict = {
            (0, 0): [(500, 500)],
            (25, 25): [(25, 25)],
        }
        sim = RWP2NSimulation(seed, pos_course_dict)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-1diag1ctr", str((rd, seed)))
        print(rd)

        pos_course_dict = {
            (1, 0): [(500, 0)],
            (0, 1): [(0, 500)],
        }
        sim = RWP2NSimulation(seed, pos_course_dict)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-1up1right", str((rd, seed)))
        print(rd)

        pos_course_dict = {
            (0, 0): [(0, 0)],
            (25, 25): [(25, 25)],
        }
        sim = RWP2NSimulation(seed, pos_course_dict)
        sim.simulate()
        rd = len(sim.num_of_broadcasters) - 1
        r.sadd(f"E-{MOB}-x{X_MAX}-y{Y_MAX}-c{NUM_OF_CARS}-1cnr1ctr", str((rd, seed)))
        print(rd)


if __name__ == '__main__':
    sim()
