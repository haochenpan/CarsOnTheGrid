import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import redis
from functools import reduce
from collections import defaultdict

X_MAX = 100
Y_MAX = 100
NUM_OF_CARS = 50
NUM_OF_MOVES = 500
PRE_RUN_COUNT = 100
SOURCE_POS = (0, 0)
EXCEED_MOVES = True

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


def get_targets_1():  # RWP2
    targets = []
    for i in range(0, 1600, 4):
        tgts = [(i, i), (i + 1, i + 3), (i + 3, i + 1)]
        targets.extend(tgts)
    # targets.append((400, 400))
    return targets[1:]


def get_targets_2():  # RWP2
    targets = []
    for i in range(0, 1600, 5):
        tgts = [(i, i), (i + 1, i + 4), (i + 4, i + 1)]
        targets.extend(tgts)
    # targets.append((400, 400))
    return targets[1:]


def get_targets_3():  # RWP2
    targets = []
    for i in range(0, 1600, 5):
        tgts = [(i, i), (i + 2, i + 3), (i + 3, i + 2)]
        targets.extend(tgts)
    # targets.append((400, 400))
    return targets[1:]


def get_targets_4():  # RWP2
    targets = []
    for i in range(0, 1600, 5):
        tgts = [(i, i), (i + 1, i + 3), (i + 4, i + 2)]
        # tgts = [(i, i), (i + 2, i + 2), (i + 1, i + 4), (i + 4, i + 1), (i + 3, i + 3)]
        targets.extend(tgts)
    # targets.append((400, 400))
    return targets[1:]


def get_targets_5():  # RWP2
    targets = []
    for i in range(100):
        tgts = [(10, 10), (20, 0), (10, -10), (0, 0)]
        targets.extend(tgts)
    return targets


if __name__ == '__main__':
    pass
    print(get_targets_5())
