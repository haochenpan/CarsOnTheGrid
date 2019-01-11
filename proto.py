"""
Prototyping Cars On The Grid Problem
"""

from collections import defaultdict
import config
import move_lib
import help_lib
import copy
import gc
from pympler.tracker import SummaryTracker


def move(grid: dict):
    next_grid, next_has_source = defaultdict(lambda: []), set()
    for pos, cars in grid.items():
        # print(pos, cars)
        while len(cars) != 0:
            car = cars.pop()
            # curr_dir_and_pos could == ('s', (0, 0))
            curr_dir_and_pos = car["trace"][-1]

            # new_dir_and_pos could == ('↓', (1, 0))
            new_dir_and_pos = move_lib.get_new_dir_and_pos(curr_dir_and_pos[1])
            car["trace"].append(new_dir_and_pos)

            # new_dir_and_pos[1] could == (1, 0)
            next_grid[new_dir_and_pos[1]].append(car)

            if config.CONST_NUM_OF_SOURCE:
                if car["when"] == 0:
                    next_has_source.add(new_dir_and_pos[1])
            else:
                if car["when"] >= 0:
                    next_has_source.add(new_dir_and_pos[1])

    return next_grid, next_has_source


def propagate(curr_round: int, grid: dict, sources: set):
    for source in sources:
        for car in grid[source]:
            if car['when'] == -1:
                car['when'] = curr_round


def run_ui() -> list:
    phrases = []
    round_counter = 0
    grid, broadcasters = help_lib.init_the_grid()
    phrases.append((copy.deepcopy(grid), broadcasters))
    while (round_counter < config.NUM_OF_MOVES and
           len(broadcasters) < config.NUM_OF_ROWS * config.NUM_OF_COLS):
        round_counter += 1
        grid, broadcasters = move(grid)
        propagate(round_counter, grid, broadcasters)
        phrases.append(copy.deepcopy((copy.deepcopy(grid), broadcasters)))
    return phrases


def run():
    round_counter = 0
    grid, broadcasters = help_lib.init_the_grid()
    while (round_counter < config.NUM_OF_MOVES and
           len(broadcasters) < config.NUM_OF_ROWS * config.NUM_OF_COLS):
        round_counter += 1
        grid, broadcasters = move(grid)
        propagate(round_counter, grid, broadcasters)
    return grid, broadcasters


if __name__ == '__main__':
    # grid_list = grid_get_states()
    # for each in grid_list:
    #     help_lib.print_grid(each)
    # tracker = SummaryTracker()
    # # tracker.print_diff()
    # for i in range(10):
    #     # help_lib.print_grid(run())
    #     print(i)
    #     run()
    # gc.collect()
    # tracker.print_diff()
    # grid, sources = run()
    # # help_lib.report_grid(grid, sources, 0, True)
    # # help_lib.report_grid(grid, sources, 1, True)
    # help_lib.report_grid(grid, sources, 2, False)
    # # help_lib.report_grid(grid, sources, 3, True)
    # help_lib.report_grid(grid, sources, 4, False)
    # help_lib.get_report(grid, sources)
    pass

