"""
    The main simulation program of the CarsOnTheGrid problem
    Friendly reminder, read comments in conf.py if you want to know some terminologies of this project
"""

from collections import defaultdict
import pickle
import conf
import help
from test import test_configs


test_configs()


def move_cars(grid: dict):
    """
    Simulate Moving all cars
    :param grid: The grid object that contains all cars, initially generated by helplib.init_grid()
    :return: A new grid object that have performed a "move_cars" AND
             a set contains all locations of broadcasters
    """

    # Iterate a dict while modifying keys is considered as a poor practice, so I create a new dict here
    next_grid, next_broadcasters = defaultdict(lambda: []), set()
    for pos, cars in grid.items():
        while cars:  # while the current list of cars (i.e. cars in that block, e.g. (1, 1)) is not empty
            car = cars.pop()

            # curr_dir_and_pos could == ('s', (0, 0))
            curr_dir_and_pos = car["trace"][-1]  # fetch the last element of the trace

            # next_dir_and_pos could == ('↓', (1, 0))
            next_dir_and_pos = help.get_new_dir_and_pos(curr_dir_and_pos[1])

            # update the car trace
            car["trace"].append(next_dir_and_pos)

            # update the new grid
            # new_dir_and_pos[1] could == (1, 0)
            next_grid[next_dir_and_pos[1]].append(car)

            # update the new broadcaster set if the current car is a broadcaster
            if car["when"] >= 0:
                next_broadcasters.add(next_dir_and_pos[1])

    return next_grid, next_broadcasters


def propagate(grid: dict, broadcasters: set, curr_round: int):
    """
    Simulate broadcasters propagating the message to non-broadcaster cars at the same position
    :param grid:
    :param broadcasters:
    :param curr_round:
    :return:
   """

    # iterate the set of broadcaster locations
    for pos in broadcasters:

        # now we stamp labels on non-broadcaster cars at that position
        for car in grid[pos]:
            if car['when'] == -1:
                car['when'] = curr_round


def get_stats(grid: dict, broadcasters: set, curr_round: int):
    """
    Call after every propagate
    :param grid:
    :param broadcasters:
    :param curr_round:
    :return:
    """
    grid_num = len(broadcasters)
    car_num = 0
    for pos in broadcasters:
        car_num += len(grid[pos])
    return curr_round, grid_num, car_num


def run():
    """
    Simulate the problem by performing move_cars and propagate NUM_OF_MOVES of times.
    :return: The grid object at its final state and
             a broadcaster set that enables faster lookup on the final state.
    """

    # initialize
    round_counter = 0
    stats = []  # statistics

    # the dict "grid" only contains blocks that have cars.
    # key: positions (x, y); value: a list of cars in that block
    # the set "broadcasters" always holds positions (x, y)
    # that has at least one broadcaster (or source)
    grid, broadcasters = help.init_grid()
    stats.append(get_stats(grid, broadcasters, round_counter))

    # while we have not reached the number of moves AND not all cars received the message
    while round_counter < conf.NUM_OF_MOVES and stats[-1][2] < conf.NUM_OF_CARS:
        round_counter += 1
        grid, broadcasters = move_cars(grid)  # move_cars cars
        propagate(grid, broadcasters, round_counter)  # broadcast the message
        stats.append(get_stats(grid, broadcasters, round_counter))  # log statistics

    # after simulation, locates the source's trace
    # could be optimized
    flag = False
    trace = []
    for pos in broadcasters:
        for car in grid[pos]:
            if car['when'] == 0:
                trace = car['trace']
                flag = True
                break
        if flag:
            break

    # after simulation, gathers configs
    confi = {
        "NUM_OF_ROWS": conf.NUM_OF_ROWS,
        "NUM_OF_COLS": conf.NUM_OF_COLS,
        "NUM_OF_CARS": conf.NUM_OF_CARS,
        "NUM_OF_MOVES": conf.NUM_OF_MOVES,
        "ALLOW_STANDING": conf.ALLOW_STANDING,
        "FIRST_ROW_INDEX": conf.FIRST_ROW_INDEX,
        "FIRST_COL_INDEX": conf.FIRST_COL_INDEX,
        "LAST_ROW_INDEX": conf.LAST_ROW_INDEX,
        "LAST_COL_INDEX": conf.LAST_COL_INDEX,
        "FIRST_CAR_INDEX": conf.FIRST_CAR_INDEX,
    }

    return dict(grid), {"stats": stats, "trace": trace, "confi": confi}


if __name__ == '__main__':
    # a simulation contains a finished grid object, a list of statistics of each round, and the source's trace
    g, s = run()
    with open('run.pickle', 'wb') as handle:
        pickle.dump((g, s), handle)
        print("saved to pickle")
