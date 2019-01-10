"""
Prototyping Cars On The Grid Problem
"""

from collections import defaultdict
import config
import move_lib
import help_lib
import copy


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

            if config.CONSTANT_SOURCE_THROUGHOUT:
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


def grid_get_states() -> list:
    states = []
    round_counter = 0
    grid, sources = help_lib.init_the_grid()
    states.append(copy.deepcopy(grid))
    while (round_counter < config.MAX_MOVE and
           len(sources) < config.NUM_OF_ROWS * config.NUM_OF_COLS):
        round_counter += 1
        grid, sources = move(grid)
        propagate(round_counter, grid, sources)
        states.append(copy.deepcopy(grid))
    return states


if __name__ == '__main__':
    grid_list = grid_get_states()
    for each in grid_list:
        help_lib.print_grid(each)

