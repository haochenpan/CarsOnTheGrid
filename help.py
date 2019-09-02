import math

X_MAX = 100
Y_MAX = 100
NUM_OF_CARS = 50
NUM_OF_MOVES = 500
PRE_RUN_COUNT = 100
EXCEED_MOVES = True

assert 0 < X_MAX
assert 0 < Y_MAX
assert 0 < NUM_OF_CARS
assert 0 < NUM_OF_MOVES


def get_dist(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def get_euclidean_dist(x1, y1, x2, y2):
    comp1 = min(abs(x1 - x2), X_MAX - abs(x1 - x2)) ** 2
    comp2 = min(abs(y1 - y2), Y_MAX - abs(y1 - y2)) ** 2
    return math.sqrt(comp1 + comp2)


def unzip(courses, mod):
    xys = list(zip(*courses))
    if mod:
        xs = list(map(lambda x: x % X_MAX, list(xys[0])))
        ys = list(map(lambda y: y % Y_MAX, list(xys[1])))
    else:
        xs = list(map(lambda x: x, list(xys[0])))
        ys = list(map(lambda y: y, list(xys[1])))
    return xs, ys


if __name__ == '__main__':
    pass
