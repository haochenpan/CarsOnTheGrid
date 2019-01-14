from collections import defaultdict
from defaultlist import defaultlist
import pickle
import pprint
import run_main
import config
ped = 0.2
num = 4  # 9 elems per row / col


def get_plotting_pos(bkt, pos):
    """
    Transform a grid position (3, 4) to a plotting position (3.4, 4.2) based on the number of items in that block
    :param bkt:
    :param pos:
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
    plotting_pos_tbl = defaultlist(lambda: [])
    plotting_pos_bkt = defaultlist(lambda: defaultdict(lambda: 0))
    for round_ctr in range(config.NUM_OF_MOVES + 1):
        for pos, cars in grid.items():
            for car in cars:
                if round_ctr >= len(car['trace']):
                    return plotting_pos_tbl
                grid_pos = car['trace'][round_ctr][1]
                plot_pos = get_plotting_pos(plotting_pos_bkt[round_ctr], grid_pos)
                plotting_pos_tbl[round_ctr].append(plot_pos)
    return plotting_pos_tbl


# with open('g.pickle', 'rb') as handle:
#     g, b = pickle.load(handle)
# g, b = proto.run()
# pp = pprint.PrettyPrinter(indent=2)
# t = get_plotting_pos_tbl(g)
# pp.pprint(t)
# print(len(t))
# bucket = defaultdict(lambda: 0)
# print(get_plotting_pos(bucket, (2, 1)))
# print(get_plotting_pos(bucket, (2, 1)))
