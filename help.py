import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import redis
from functools import reduce
from collections import defaultdict

X_MAX = 20
Y_MAX = 20
NUM_OF_CARS = 50
NUM_OF_MOVES = 500
PRE_RUN_COUNT = 100
SOURCE_POS = (10, 10)
EXCEED_MOVES = True
RAND_SEED = "%.20f" % time.time()
SOURCE_COURSE = []

assert 0 < X_MAX
assert 0 < Y_MAX
assert 0 < NUM_OF_CARS
assert 0 < NUM_OF_MOVES
assert 0 <= SOURCE_POS[0] < X_MAX
assert 0 <= SOURCE_POS[1] < Y_MAX


def get_dist(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def get_euclidean_dist(x1, y1, x2, y2):
    comp1 = min(abs(x1 - x2), X_MAX - abs(x1 - x2)) ** 2
    comp2 = min(abs(y1 - y2), Y_MAX - abs(y1 - y2)) ** 2
    return math.sqrt(comp1 + comp2)


def get_targets_s1():
    # tgts = [(1, 10), (19, 10)]
    tgts = [(10, 1), (10, 19)]
    targets = []
    for i in range(1000):
        targets.extend(tgts)
    return targets


def get_targets_s2():
    # tgts = [(5, 10), (15, 10)]
    tgts = [(10, 5), (10, 15)]
    targets = []
    for i in range(1000):
        targets.extend(tgts)
    return targets


def get_targets_s3():
    tgts = [(10, 8), (10, 12)]
    targets = []
    for i in range(1000):
        targets.extend(tgts)
    return targets


if __name__ == '__main__':
    pass
    # tgts = [(i, i), (i + 2, i + 4), (i + 3, i + 1)]
    # tgts = [(i, i), (i + 1, i + 3), (i + 4, i + 2)]

    print(get_targets_s3())
