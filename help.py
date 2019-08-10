import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import redis
from functools import reduce

X_MAX = 100
Y_MAX = 100
NUM_OF_CARS = 500
NUM_OF_MOVES = 500
PRE_RUN_COUNT = 0
SOURCE_POS = (0, 0)
CAR_CLASS = ""
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


if __name__ == '__main__':
    pass
    print(get_euclidean_dist(*(85, 95), *(75, 25)))
    print(get_dist(*(85, -5), *(75, 25)))
