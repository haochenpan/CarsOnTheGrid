from collections import defaultdict
from random import randint
import config


def get_rand_pos():
    r = randint(config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX)
    c = randint(config.FIRST_COL_INDEX, config.LAST_COL_INDEX)
    return r, c


def init_a_car(car_id: int, car_pos: tuple, when: int = -1) -> dict:
    """
    Initiates a car, may use many times in the 0th round
    :param car_id:
    :param car_pos: The position of a car, in the format (x, y)
    :param when: Indicates the round that the car becomes a broadcaster.
                 If when == -1, it has not received the message
    :return: A dictionary representation of a car object
    """
    return {
        "id": car_id,
        "when": when,
        "trace": [("s", car_pos)]
    }


def init_the_grid():
    """
    Initiates the grid, may use once in the 0th round
    :return: A dictionary representation of a grid object
    """
    # The grid only contains blocks that have cars
    grid = defaultdict(lambda: [])

    # generate the source car, id = FIRST_CAR_INDEX
    source_pos = get_rand_pos()
    source_car = init_a_car(config.FIRST_CAR_INDEX, source_pos, when=0)
    grid[source_pos].append(source_car)

    # generate other cars, ids in [FIRST_CAR_INDEX + 1, NUM_OF_CARS + FIRST_CAR_INDEX - 1]
    for i in range(config.FIRST_CAR_INDEX + 1, config.NUM_OF_CARS + config.FIRST_CAR_INDEX):
        pos = get_rand_pos()
        # ensure single source
        while pos == source_pos:
            pos = get_rand_pos()
        car = init_a_car(i, pos)
        grid[pos].append(car)

    return grid, source_pos


def print_grid(grid: dict, broadcasters: set, mode: int = 0, trace: bool = False):
    """

    :param grid:
    :param broadcasters:
    :param mode: 0 == all blocks with cars
                 1 == blocks with at least one broadcaster (or source), show every car
                 2 == blocks with at least one broadcaster (or source), but only show broadcaster(s) and source(s)
                 3 == blocks with at least one source, show every car
                 4 == blocks with at least one source, but only show source(s)
    :param trace: show traces of cars
    :return:
    """

    def print_idx_and_pos(idx: int, pos: tuple):
        """

        :param idx: an integer, the index of the enumeration
        :param pos: a tuple in the format (x, y)
        :return:
        """
        print(f'{idx: 5d}: ({pos[0]: 3d}, {pos[1]: 3d})', end='   ')

    def print_a_car_wo_trace(car: dict):
        """
        Print a car without its trace
        :param car:
        :return:
        """
        print(f' id:{car["id"]: 3d}, when:{car["when"]: 3d}', end='   ')

    def print_all_cars(idx: int, pos: tuple, cars: list):
        if trace:
            print(f'{idx: 5d}: ({pos[0]: 3d}, {pos[1]: 3d})   {cars}')
        else:
            print_idx_and_pos(idx, pos)
            for car in cars:
                print_a_car_wo_trace(car)
            print()

    # print('\n\n')
    print(f'--report mode:{mode}')
    if mode == 0:
        for idx, (pos, cars) in enumerate(grid.items()):
            print_all_cars(idx, pos, cars)
    elif mode in {1, 2}:
        for idx, pos in enumerate(broadcasters):
            # all cars in the set are broadcasters
            print_all_cars(idx, pos, grid[pos])
    else:
        for idx, pos in enumerate(broadcasters):
            for car in grid[pos]:
                if car['when'] == 0:
                    if mode == 3:
                        print_all_cars(idx, pos, grid[pos])
                    else:  # mode == 4
                        print_idx_and_pos(idx, pos)
                        print(car)
                    return
    # print('\n\n')


def report_grid(grid: dict, broadcasters: set):
    """

    :param grid: the grid at its final round
    :param broadcasters: positions (x, y) that has at least one broadcaster
    :return:
    """
    num_of_cars_has_the_msg, source_car_traces = 0, []
    for pos in broadcasters:
        for car in grid[pos]:
            if car['when'] == 0:
                # could be optimized
                source_car_traces.append(car['trace'])
            # may need to change if we want the image after move but before propagate
        num_of_cars_has_the_msg += len(grid[pos])

    report = {
        "config": {
            "NUM_OF_ROWS": config.NUM_OF_ROWS,
            "NUM_OF_COLS": config.NUM_OF_COLS,
            "NUM_OF_CARS": config.NUM_OF_CARS,
            "NUM_OF_MOVES": config.NUM_OF_MOVES,
            "ALLOW_STANDING": config.ALLOW_STANDING,
            "FIRST_ROW_INDEX": config.FIRST_ROW_INDEX,
            "FIRST_COL_INDEX": config.FIRST_COL_INDEX,
            "FIRST_CAR_INDEX": config.FIRST_CAR_INDEX
        },
        "stats": {
            "num of cars has the message": num_of_cars_has_the_msg,
            "source_car(s)_trace(s)": source_car_traces
        },
        "raw_last_round": grid

    }

    print(report["stats"])
    return report


if __name__ == '__main__':
    g, b = init_the_grid()
    print(print_grid(g, b, 4, True))
    report_grid(g, b)
    pass
