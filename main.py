"""
    Simulates CarsOnTheGrid problem
"""

from collections import defaultdict
import pickle
import pprint
import config
import helplib
from test import base_config_assertions

base_config_assertions()


def move(grid: dict):
    """
    Move all cards on the grid
    :param grid: The grid object that want to perform "move" on its car objects
    :return: The new grid object that have performed a "move" on its car objects
    """
    # Iterate a dict while modifying keys is considered as a poor practice,
    # so I create a new dict here
    next_grid, next_broadcasters = defaultdict(lambda: []), set()
    for pos, cars in grid.items():
        while cars:  # while the list cars is not empty
            car = cars.pop()
            # curr_dir_and_pos could == ('s', (0, 0))
            curr_dir_and_pos = car["trace"][-1]
            # print(curr_dir_and_pos)
            # next_dir_and_pos could == ('↓', (1, 0))
            next_dir_and_pos = helplib.get_new_dir_and_pos(curr_dir_and_pos[1])
            car["trace"].append(next_dir_and_pos)

            # new_dir_and_pos[1] could == (1, 0)
            next_grid[next_dir_and_pos[1]].append(car)

            if car["when"] >= 0:
                next_broadcasters.add(next_dir_and_pos[1])
    return next_grid, next_broadcasters


def propagate(grid: dict, broadcasters: set, curr_round: int):
    """
    Broadcasters broadcast messages to cars in the same grid
    :param grid:
    :param broadcasters:
    :param curr_round:
    :return:
    """
    for pos in broadcasters:
        for car in grid[pos]:
            if car['when'] == -1:
                car['when'] = curr_round


def get_stat(grid: dict, broadcasters: set, curr_round: int):
    """
    Could be optimized
    :param grid:
    :param broadcasters:
    :param curr_round:
    :return:
    """
    grid_num = len(broadcasters)
    car_num = 0
    for pos in broadcasters:
        for car in grid[pos]:
            if car['when'] >= 0:
                car_num += 1
    return curr_round, grid_num, car_num


def run():
    """
    Simulate the problem by performing move and propagate NUM_OF_MOVES of times.
    :return: The grid object at its final state and
             a broadcaster set that enables faster lookup on the final state.
    """
    # initialize
    round_counter = 0
    total_blocks = config.NOR * config.NOC
    stats = []

    # the dict "grid" only contains blocks that have cars.
    # key: positions (x, y); value: a list of cars in that block
    # the set "broadcasters" always holds positions (x, y)
    # that has at least one broadcaster (or source)
    grid, broadcasters = helplib.init_grid()
    stats.append(get_stat(grid, broadcasters, round_counter))
    # while round_counter < config.NUM_OF_MOVES and len(broadcasters) < total_blocks:
    while round_counter < config.NUM_OF_MOVES and stats[-1][2] < config.NUM_OF_CARS:
        round_counter += 1
        grid, broadcasters = move(grid)
        # stats.append(get_stat(grid, broadcasters, round_counter))
        propagate(grid, broadcasters, round_counter)
        stats.append(get_stat(grid, broadcasters, round_counter))
    # assert len(stats) % 2 == 1
    return dict(grid), stats


if __name__ == '__main__':
    g, s = run()
    with open('run.pickle', 'wb') as handle:
        pickle.dump((g, s), handle)
        print("saved to pickle")

    # with open('run.pickle', 'rb') as handle:
    #     g, b, s = pickle.load(handle)
    # pp = pprint.PrettyPrinter()
    # pp.pprint(helplib.get_repr(g, b, s)['broadcasters'])

    pass
