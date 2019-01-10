"""
Prototyping Cars On The Grid Problem
"""

from random import randint, choice
from collections import defaultdict
import config
import move_lib
import helper


def move(grid: dict):
    next_grid, next_has_source = defaultdict(lambda: []), set()
    for pos, cars in grid.items():
        while len(cars) != 0:
            car = cars.pop()
            curr_pos = car["trace"][-1][1]
            # next_pos could == ('↓', (1, 0))
            next_pos = move_lib.get_new_pos(curr_pos)
            car["trace"].append(next_pos)
            # next_pos[1] could == (1, 0)
            next_grid[next_pos[1]].append(car)

            # for multi-source
            # if car["when"] > -1:

            # for single-source
            if car["when"] == 0:
                next_has_source.add(next_pos[1])

    return next_grid, next_has_source


def propagate(round: int, grid: dict, sources: set):
    for source in sources:
        for car in grid[source]:
            if car['when'] == -1:
                car['when'] = round


def grid_generator():
    round_counter = 0
    grid, sources = helper.gen_init_grid()
    yield grid
    while (round_counter <= config.MAX_MOVE and
           len(sources) < config.NUM_OF_ROWS * config.NUM_OF_COLS):
        round_counter += 1
        grid, sources = move(grid)
        yield grid
        propagate(round_counter, grid, sources)
    # helper.print_grid(grid)


if __name__ == '__main__':
    gen = grid_generator()
    while True:
        try:
            print(next(gen))
        except StopIteration:
            break
