from collections import defaultdict
from random import randint, choice

import config


def init_a_car(car_id: int, car_pos: tuple, source_pos: tuple) -> dict:
    """
    Generates a car in the 0th round
    :param car_id:
    :param car_pos: the position of a car, e.g. (1, 3)
    :param source_pos: the position of the source
    :return: a dictionary representation of a car object
    """
    return {
        "id": car_id,
        "trace": [("s", car_pos)],
        "when": -1 if car_pos != source_pos else 0
    }


def init_the_grid():
    # grid = a dictionary only contains blocks that have cars
    grid = defaultdict(lambda: [])
    # enables quick lookup source car(s)
    has_source = set()

    # generate the source car, id = 0
    source_pos = (config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX)
    source_car = init_a_car(0, source_pos, source_pos)
    grid[source_pos].append(source_car)
    has_source.add(source_pos)

    # generate other cars
    for i in range(1, config.NUM_OF_CARS):
        r = randint(config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX)
        c = randint(config.FIRST_COL_INDEX, config.LAST_COL_INDEX)

        # ensure single source
        if config.SINGLE_SOURCE_FIRST_GRID:
            while r == config.FIRST_ROW_INDEX and c == config.FIRST_COL_INDEX:
                r = randint(config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX)
                c = randint(config.FIRST_COL_INDEX, config.LAST_COL_INDEX)

        car = init_a_car(i, (r, c), source_pos)
        grid[(r, c)].append(car)

    return grid, has_source


def print_grid(grid: dict):
    print('\n\n')
    for i, (pos, cars) in enumerate(grid.items()):
        for car in cars:
            if car['when'] > -1:
                print(f'{i:-3d}  {(pos, cars)}')
                break
    print('\n\n')


if __name__ == '__main__':

    # TODO(Haochen): formal assertion tests
    car_count = 0
    g, h = init_the_grid()
    for k, cars in g.items():
        car_count += len(cars)
    assert car_count == config.NUM_OF_CARS
