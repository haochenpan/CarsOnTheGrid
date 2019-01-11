from collections import defaultdict
from random import randint
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
        if config.HAS_SINGLE_SOURCE:
            while r == config.FIRST_ROW_INDEX and c == config.FIRST_COL_INDEX:
                r = randint(config.FIRST_ROW_INDEX, config.LAST_ROW_INDEX)
                c = randint(config.FIRST_COL_INDEX, config.LAST_COL_INDEX)

        car = init_a_car(i, (r, c), source_pos)
        grid[(r, c)].append(car)

    return grid, has_source


def report_grid(grid: dict, broadcaster: set, mode: int = 0, trace: bool = False):
    """

    :param grid:
    :param broadcaster:
    :param mode: 0 == all blocks with cars
                 1 == blocks with at least one broadcaster (or source), show every car
                 2 == blocks with at least one broadcaster (or source), but only show broadcaster(s) and source(s)
                 3 == blocks with at least one source, show every car
                 4 == blocks with at least one source, but only show source(s)
    :param trace:
    :return:
    """
    # print('\n\n')
    def has_any_broadcaster(cars: list):
        for car in cars:
            if car['when'] >= 0:
                return True
        return False

    def has_any_source(cars: list):
        for car in cars:
            if car['when'] == 0:
                return True
        return False

    def report_idx_and_pos(idx: int, pos: tuple):
        print(f'{idx: 5d}: ({pos[0]: 3d}, {pos[1]: 3d})', end='   ')

    def report_a_car_wo_trace(car: dict):
        print(f' id:{car["id"]: 3d}, when:{car["when"]: 3d}', end='   ')

    def report_all_cars(idx: int, pos: tuple, cars: list):
        if trace:
            print(f'{idx: 5d}: ({pos[0]: 3d}, {pos[1]: 3d})   {cars}')
        else:
            report_idx_and_pos(idx, pos)
            for car in cars:
                report_a_car_wo_trace(car)
            print()

    def report_all_broadcaster_only(idx: int, pos: tuple, cars: list):
        # could be optimized
        if has_any_broadcaster(cars):
            if trace:
                report_idx_and_pos(idx, pos)
                for car in cars:
                    if car['when'] >= 0:
                        print(car, end='    ')
            else:
                report_idx_and_pos(idx, pos)
                for car in cars:
                    if car['when'] >= 0:
                        report_a_car_wo_trace(car)
            print()

    def report_all_sources_only(idx: int, pos: tuple, cars: list):
        # could be optimized
        if has_any_source(cars):
            if trace:
                report_idx_and_pos(idx, pos)
                for car in cars:
                    if car['when'] == 0:
                        print(car, end='    ')
            else:
                report_idx_and_pos(idx, pos)
                for car in cars:
                    if car['when'] == 0:
                        report_a_car_wo_trace(car)
            print()

    def report_all_cars_if_has_any_broadcaster(idx: int, pos: tuple, cars: list):
        if has_any_broadcaster(cars):
            report_all_cars(idx, pos, cars)

    def report_all_cars_if_has_any_source(idx: int, pos: tuple, cars: list):
        if has_any_source(cars):
            report_all_cars(idx, pos, cars)

    if mode == 0:
        for idx, (pos, cars) in enumerate(grid.items()):
            report_all_cars(idx, pos, cars)

    # A receiver cannot become a source, so we need to use the full grid to report
    elif config.CONST_NUM_OF_SOURCE:
        if mode == 1:
            for idx, (pos, cars) in enumerate(grid.items()):
                report_all_cars_if_has_any_broadcaster(idx, pos, cars)
        elif mode == 2:
            for idx, (pos, cars) in enumerate(grid.items()):
                report_all_broadcaster_only(idx, pos, cars)
        elif mode == 3:
            for idx, (pos, cars) in enumerate(grid.items()):
                report_all_cars_if_has_any_source(idx, pos, cars)
        elif mode == 4:
            for idx, (pos, cars) in enumerate(grid.items()):
                report_all_sources_only(idx, pos, cars)

    # A receiver can become a broadcaster, so we use the set sources for faster searching
    else:
        if mode in {1, 2}:
            for idx, pos in enumerate(broadcaster):
                # all cars in the set are broadcasters
                report_all_cars(idx, pos, grid[pos])
        elif mode == 3:
            for idx, pos in enumerate(broadcaster):
                report_all_cars_if_has_any_source(idx, pos, grid[pos])
        elif mode == 4:
            for idx, pos in enumerate(broadcaster):
                report_all_sources_only(idx, pos, grid[pos])
    print(f'    <--report mode:{mode}\n')


def get_report(grid: dict, broadcasters: set):
    num_of_cars_has_the_msg, source_car_traces = 0, []
    for broadcaster in broadcasters:
        for car in grid[broadcaster]:
            if car['when'] == 0:
                source_car_traces.append(car['trace'])
        if not config.CONST_NUM_OF_SOURCE:
            num_of_cars_has_the_msg += len(grid[broadcaster])

    # if a car can only become a receiver, not a source (broadcaster), the set sources may not contain its position
    if config.CONST_NUM_OF_SOURCE:
        for cars in grid.values():
            for car in cars:
                if car['when'] >= 0:
                    num_of_cars_has_the_msg += 1

    report = {
        "config": {
            "NUM_OF_CARS": config.NUM_OF_CARS,
            "NUM_OF_MOVES": config.NUM_OF_MOVES,
            "NUM_OF_ROWS": config.NUM_OF_ROWS,
            "NUM_OF_COLS": config.NUM_OF_COLS,
            "FIRST_ROW_INDEX": config.FIRST_ROW_INDEX,
            "FIRST_COL_INDEX": config.FIRST_COL_INDEX,
            "NUM_OF_DIRS": config.NUM_OF_DIRS,
            "ALLOW_STANDING": config.ALLOW_STANDING,
            "HAS_SINGLE_SOURCE": config.HAS_SINGLE_SOURCE,
            "CONST_NUM_OF_SOURCE": config.CONST_NUM_OF_SOURCE,
            "BORDER_BEHAVIOR": config.BORDER_BEHAVIOR,
        },
        "stats": {
            "num of source cars": len(source_car_traces),
            "num of cars has the message": num_of_cars_has_the_msg,
            "source_car(s)_trace(s)": source_car_traces
        },
        "raw_last_round": grid

    }

    print(report["stats"])
    return report


if __name__ == '__main__':
    # TODO(Haochen): formal assertion tests
    # car_count = 0
    # g, h = init_the_grid()
    # for k, cars in g.items():
    #     car_count += len(cars)
    # assert car_count == config.NUM_OF_CARS

    pass
