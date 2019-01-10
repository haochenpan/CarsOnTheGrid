from collections import defaultdict
from random import randint, choice

import config


def gen_car(car_id: int, car_pos: tuple, source_pos: tuple) -> dict:
    return {
        "id": car_id,
        "trace": [("s", car_pos)],
        "when": -1 if car_pos != source_pos else 0
    }


def gen_init_grid():
    grid = defaultdict(lambda: [])
    has_source = set()

    # generate the source car (id = 0)
    source_pos = (config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX)
    source_car = gen_car(0, source_pos, source_pos)
    grid[source_pos].append(source_car)
    has_source.add(source_pos)

    # generate other cars
    for i in range(1, config.NUM_OF_CARS):
        r = randint(config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX)
        c = randint(config.FIRST_COL_INDEX, config.LAST_COL_INDEX)

        # ensure single source
        while r == config.FIRST_ROW_INDEX and c == config.FIRST_COL_INDEX:
            r = randint(config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX)
            c = randint(config.FIRST_COL_INDEX, config.LAST_COL_INDEX)

        car = gen_car(i, (r, c), source_pos)
        grid[(r, c)].append(car)

    return grid, has_source


def print_grid(grid: dict):
    for k, v in grid.items():
        print(k, v)


def is_done(has_source: set):
    return
