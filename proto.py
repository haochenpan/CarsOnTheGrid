"""
Prototyping Cars On The Grid Problem
"""

from collections import defaultdict
import config
import movelib
import helplib
import copy
import gc
from pympler.tracker import SummaryTracker


def move(grid: dict):
    # Iterate a dict while modifying keys is considered as a poor practice, so I create a new dict here
    next_grid, next_broadcasters = defaultdict(lambda: []), set()
    for pos, cars in grid.items():
        while len(cars) != 0:
            car = cars.pop()
            # curr_dir_and_pos could == ('s', (0, 0))
            curr_dir_and_pos = car["trace"][-1]
            # print(curr_dir_and_pos)
            # next_dir_and_pos could == ('↓', (1, 0))
            next_dir_and_pos = movelib.get_new_dir_and_pos(curr_dir_and_pos[1])
            car["trace"].append(next_dir_and_pos)

            # new_dir_and_pos[1] could == (1, 0)
            next_grid[next_dir_and_pos[1]].append(car)

            if car["when"] >= 0:
                next_broadcasters.add(next_dir_and_pos[1])
    return next_grid, next_broadcasters


def propagate(curr_round: int, grid: dict, broadcasters: set):
    for pos in broadcasters:
        for car in grid[pos]:
            if car['when'] == -1:
                car['when'] = curr_round


def run():
    # initialize
    round_counter = 0
    total_blocks = config.NUM_OF_ROWS * config.NUM_OF_COLS

    # the dict "grid" only contains blocks that have cars. key: positions (x, y); value: a list of cars in that block
    # the set "broadcasters" always holds positions (x, y) that has at least one broadcaster (or source)
    grid, broadcasters = helplib.init_the_grid()
    while round_counter < config.NUM_OF_MOVES and len(broadcasters) < total_blocks:
        round_counter += 1
        grid, broadcasters = move(grid)
        propagate(round_counter, grid, broadcasters)
    return grid, broadcasters


if __name__ == '__main__':
    tracker = SummaryTracker()
    g, b = run()
    u, d, l, r, h = 0, 0, 0, 0, 0
    # helplib.report_grid_intermediate(g, b, 0, False)
    # helplib.report_grid_intermediate(g, b, 1, True)
    # helplib.report_grid_intermediate(g, b, 3, True)
    # helplib.report_grid_final(g, b)

    # for cars in g.values():
    #     for car in cars:
    #         for e in car['trace']:
    #             if e[0] == '↑':
    #                 u += 1
    #                 continue
    #             if e[0] == '↓':
    #                 d += 1
    #                 continue
    #             if e[0] == '←':
    #                 l += 1
    #                 continue
    #             if e[0] == '→':
    #                 r += 1
    #                 continue
    #             if e[0] == '•':
    #                 h += 1
    #                 continue
    # print(u, d, l, r, h)

    del g, b
    # gc.collect()
    # tracker.print_diff()
    pass
