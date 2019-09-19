import math

X_MAX = 50
Y_MAX = X_MAX
NUM_OF_CARS = 25
NUM_OF_MOVES = 500
PRE_RUN_COUNT = 100
EXCEED_MOVES = True

fig_size = (6, 6)

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


def RWP1_diagonal():
    pair = [(X_MAX, Y_MAX), (0, 0)]
    trace = []
    for i in range(100):
        trace.extend(pair)
    return trace


def RWP2_diagonal():
    trace = [(X_MAX * 100, Y_MAX * 100)]
    return trace


def RD_diagonal():
    return RWP1_diagonal()


def MG1_diagonal():
    x, y = 0, 0
    trace = []
    for i in range(X_MAX):
        trace.append((x, y))
        x += 1
        trace.append((x, y))
        y += 1
    trace.append((x, y))
    course = []
    for i in range(5):
        course.extend(trace[1:])
        course.extend(list(reversed(trace[:-1])))
    return course


def MG2_diagonal():
    x, y = 0, 0
    trace = []
    for i in range(1000):
        x += 1
        trace.append((x, y))
        y += 1
        trace.append((x, y))

    return trace


def RWP2_up():
    return [(0, 5000)]


def RWP2_right():
    return [(5000, 0)]


def RWP2_zigzag_14():
    targets = []
    for i in range(0, 1600, 5):
        tgts = [(i, i), (i + 1, i + 4), (i + 4, i + 1)]
        targets.extend(tgts)
    return targets[1:]


def RWP2_zigzag_23():
    targets = []
    for i in range(0, 1600, 5):
        tgts = [(i, i), (i + 2, i + 3), (i + 3, i + 2)]
        targets.extend(tgts)
    return targets[1:]


if __name__ == '__main__':
    print(RWP2_zigzag_14())
