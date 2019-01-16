from collections import defaultdict
from defaultlist import defaultlist
from random import randint, choice
import numpy as np
import config

"""
    Simulation Helper Library
"""
dir_tbl = {
    0: "•",
    1: "↑",
    2: "→",
    3: "↓",
    4: "←",
}


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


def get_new_dir_and_pos(curr_pos: tuple) -> tuple:
    """
    Base on the current position (x, y), generate a new random direction (could be ↑) and a position (x, y+1)
    :param curr_pos: The current position coordinate (i.e. (x, y)) of the car
    :return: The direction and position coordinate (i.e. (d, (x, y)))
    """
    directions = {1, 2, 3, 4}
    if config.ALLOW_STANDING:
        directions.add(0)

    # removes directions that a border block does not have
    if curr_pos[0] == config.FIRST_ROW_INDEX:
        directions.difference_update({1})
    if curr_pos[0] == config.LAST_ROW_INDEX:
        directions.difference_update({3})
    if curr_pos[1] == config.FIRST_COL_INDEX:
        directions.difference_update({4})
    if curr_pos[1] == config.LAST_COL_INDEX:
        directions.difference_update({2})

    # choose a random direction
    assert len(directions) > 0
    new_dir = choice(tuple(directions))
    # print(new_dir)

    # convert to the new direction to an position coordinate
    if new_dir == 1:
        return dir_tbl[new_dir], (curr_pos[0] - 1, curr_pos[1])
    if new_dir == 2:
        return dir_tbl[new_dir], (curr_pos[0], curr_pos[1] + 1)
    if new_dir == 3:
        return dir_tbl[new_dir], (curr_pos[0] + 1, curr_pos[1])
    if new_dir == 4:
        return dir_tbl[new_dir], (curr_pos[0], curr_pos[1] - 1)
    return dir_tbl[new_dir], curr_pos


"""
    GUI Helper Library
"""


def get_plotting_pos(pos: tuple, bkt: dict) -> tuple:
    """
    Transform a grid position (3, 4) to a plotting position (3.4, 4.2) based on the number of items in that block
    :param pos:
    :param bkt:
    :return:
    """
    num_in_the_block = bkt[pos]
    # row_idx starts from 0
    row_idx = num_in_the_block % config.COUNT_PER_ROW_COL
    col_idx = num_in_the_block // config.COUNT_PER_ROW_COL
    # print(pos)
    # print(row_idx, col_idx)
    row_pos = pos[0] + config.PADDING + config.PADDING * row_idx
    col_pos = pos[1] + config.PADDING + config.PADDING * col_idx
    bkt[pos] += 1
    # print(row_pos, col_pos)
    return row_pos, col_pos


def get_plotting_pos_tbl(grid):
    """
    Get all (NUM_OF_MOVES + 1) sets of plotting positions
    :param grid:
    :return:
    """
    plotting_pos_tbl = defaultlist(lambda: [])
    plotting_pos_bkt = defaultlist(lambda: defaultdict(lambda: 0))
    for pos, cars in grid.items():
        for car in cars:
            assert len(car['trace']) == config.NUM_OF_MOVES + 1, "sanity check, we want to use the final grid"
            # iterate car['trace']
            for round_idx in range(config.NUM_OF_MOVES + 1):
                grid_pos = car['trace'][round_idx][1]
                plot_pos = get_plotting_pos(grid_pos, plotting_pos_bkt[round_idx])
                plotting_pos_tbl[round_idx].append(plot_pos)

    assert len(plotting_pos_bkt) == config.NUM_OF_MOVES + 1, "make sure we have len(init and every move) rounds"
    assert len(plotting_pos_tbl) == config.NUM_OF_MOVES + 1, "make sure we have len(init and every move) rounds"
    assert len(plotting_pos_tbl[0]) == config.NUM_OF_CARS, "for every round, we have NUM_OF_CARS plotting positions"
    return plotting_pos_tbl


def get_ls(pos1, pos2):
    """
    Gets an 2D array of positions for the animation,
    and each entry of the 2D array is an 1D array that represents a coordinate [x, y],
    The first entry is [pos1_x, pos1_y];
    The second entry is [pos1_x + delta_x, pos1_y + delta_y],
    where delta_x = (pos2_x - pos1_x)/config.FRAMES, deltas could be a negative float;
    So on so forth... and the last entry is [pos2_x, pos2_y]
    :param pos1:
    :param pos2:
    :return:
    """
    ls_x = np.linspace(pos1[0], pos2[0], num=config.FRAMES,
                       dtype=np.float16)  # no need such precision, and optimize mem usage
    ls_y = np.linspace(pos1[1], pos2[1], num=config.FRAMES, dtype=np.float16)
    ls = np.column_stack((ls_x, ls_y))
    return ls


def get_ls_tbl(plotting_pos_tbl: list):
    """
    Gets an 4D array that includes every position needed
    for every dot(car) on the grid during every the animation.
    Outermost dimension has config.NUM_OF_MOVES elements,
    each element represents all positions used by all cars in a round

    The next dimension has config.NUM_OF_CARS elements,
    each element represents all positions used for a car in a round

    The inner two dimensions are merely output of get_ls() function call.

    :param plotting_pos_tbl: A valid output of get_plotting_pos_tbl() function call
    :return:
    """
    ls_tbl = defaultlist(lambda: defaultlist(lambda: []))
    assert len(plotting_pos_tbl) == config.NUM_OF_MOVES + 1, "make sure we have len(init and every move) rounds"
    for round_idx in range(config.NUM_OF_MOVES):  # only need NUM_OF_MOVES of transitions
        assert len(plotting_pos_tbl[round_idx]) == config.NUM_OF_CARS, \
            "for every round, we have NUM_OF_CARS plotting positions"
        for car_idx in range(len(plotting_pos_tbl[round_idx])):
            curr_car_pos = plotting_pos_tbl[round_idx][car_idx]
            next_car_pos = plotting_pos_tbl[round_idx + 1][car_idx]
            ls = get_ls(curr_car_pos, next_car_pos)
            ls_tbl[round_idx].append(ls)

    assert len(ls_tbl) == config.NUM_OF_MOVES, "each elem of the list is for a move's animation"
    assert len(ls_tbl[0]) == config.NUM_OF_CARS, "need to move that many of cars in each animation"

    """
        the above function call gives a 4D array that each entry of the inner 3D array
        represents a car's all point-in-time positions, but we need to "stack" them in
        a way that each entry represents all cars' positions at a point-in-time
    """

    stack_tbl = []
    for each in ls_tbl:
        stack_tbl.append(np.stack(each, axis=1))
    return stack_tbl


def get_colors(car: dict):
    when = car['when']
    if when == -1:
        return ['b' for i in range(config.NUM_OF_MOVES + 1)]
    elif when == 0:
        return ['r' for i in range(config.NUM_OF_MOVES + 1)]
    else:
        colors = ['b' for i in range(when)]
        colors.extend(['y' for i in range(config.NUM_OF_MOVES + 1 - when)])
        return colors


def get_color_tbl(grid: dict):
    color_tbl = []
    for p, cs in grid.items():
        for c in cs:
            color_tbl.append(get_colors(c))
    color_tbl = np.stack(color_tbl, axis=1)
    assert len(color_tbl) == config.NUM_OF_MOVES + 1, ""
    assert len(color_tbl[0]) == config.NUM_OF_CARS, ""
    return color_tbl


def get_source_pos(pos: tuple, bkt: dict) -> tuple:
    num_in_the_block = bkt[pos]
    row_pos = pos[0] + config.PADDING + config.PADDING * num_in_the_block
    col_pos = pos[1] + config.PADDING + config.PADDING * num_in_the_block
    bkt[pos] += 1
    return row_pos, col_pos


def get_source_pos_tbl(grid: dict):
    source_pos_tbl = []
    source_pos_bkt = defaultdict(lambda: 0)
    for pos, cars in grid.items():
        for car in cars:
            if car['when'] == 0:
                for round_idx in range(config.NUM_OF_MOVES + 1):
                    grid_pos = car['trace'][round_idx][1]
                    plot_pos = get_source_pos(grid_pos, source_pos_bkt)
                    source_pos_tbl.append(plot_pos)
                source_pos_tbl = np.stack(source_pos_tbl, axis=1)
                return source_pos_tbl
    assert False, "sanity check"


if __name__ == '__main__':
    pass
