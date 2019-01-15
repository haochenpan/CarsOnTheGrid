from collections import defaultdict
from defaultlist import defaultlist
import pickle
import pprint
import run_main
import numpy as np
import config

ped = 0.2
num = 4  # 9 elems per row / col
frames = 30


def get_plotting_pos(pos: tuple, bkt: dict) -> tuple:
    """
    Transform a grid position (3, 4) to a plotting position (3.4, 4.2) based on the number of items in that block
    :param pos:
    :param bkt:
    :return:
    """
    num_in_the_block = bkt[pos]
    # row_idx starts from 0
    row_idx = num_in_the_block % num
    col_idx = num_in_the_block // num
    # print(pos)
    # print(row_idx, col_idx)
    row_pos = pos[0] + ped + ped * row_idx
    col_pos = pos[1] + ped + ped * col_idx
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
    ls_x = np.linspace(pos1[0], pos2[0], num=frames, dtype=np.float16)  # no need such precision, and optimize mem usage
    ls_y = np.linspace(pos1[1], pos2[1], num=frames, dtype=np.float16)
    ls = np.column_stack((ls_x, ls_y))
    return ls


def get_ls_tbl(plotting_pos_tbl: list):
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
    return ls_tbl


def get_stack_tbl(ls_tbl: list):
    stack_tbl = []
    for each in ls_tbl:
        stack_tbl.append(np.stack(each, axis=1))
    return stack_tbl


if __name__ == '__main__':
    # with open('g.pickle', 'rb') as handle:
    #     g, b = pickle.load(handle)
    g, b = run_main.run()
    t = get_plotting_pos_tbl(g)
    pp = pprint.PrettyPrinter(indent=2)
    print(t[0][5], t[1][5])
    print(get_ls_tbl(t)[0][5])
