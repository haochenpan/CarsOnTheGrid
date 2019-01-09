from random import randint, choice
import config

direction_dict = {
    0: "•",
    1: "↑",
    2: "↗",
    3: "→",
    4: "↘",
    5: "↓",
    6: "↙",
    7: "←",
    8: "↖",
}


def get_new_pos(curr_pos: tuple) -> tuple:
    if config.BORDER_BEHAVIOR == "restricted":
        return gen_new_pos_res(curr_pos)
    else:
        raise Exception


def gen_new_pos_res(curr_pos: tuple) -> tuple:
    if config.MOVE_DIR_COUNT == 8:
        # generate a new direction
        directions = {1, 2, 3, 4, 5, 6, 7, 8}  # all possible directions
    else:
        directions = {1, 3, 5, 7}
    # removes directions that a border block does not have
    if curr_pos[0] == config.FIRST_ROW_INDEX:
        directions.difference_update({8, 1, 2})
    if curr_pos[0] == config.LAST_ROW_INDEX:
        directions.difference_update({6, 5, 4})
    if curr_pos[1] == config.FIRST_COL_INDEX:
        directions.difference_update({8, 7, 6})
    if curr_pos[1] == config.LAST_COL_INDEX:
        directions.difference_update({2, 3, 4})
    if config.ALLOW_STANDING:
        directions.add(0)
    new_dir = choice(tuple(directions))  # int, 0 - 8

    # if curr_pos == (FIRST_ROW_INDEX, FIRST_COL_INDEX) and ALLOW_STANDING:
    #     assert directions == {0, 3, 4, 5}
    # elif curr_pos == (FIRST_ROW_INDEX, LAST_COL_INDEX) and ALLOW_STANDING:
    #     assert directions == {0, 5, 6, 7}
    # elif curr_pos == (LAST_ROW_INDEX, FIRST_COL_INDEX) and ALLOW_STANDING:
    #     assert directions == {0, 1, 2, 3}
    # elif curr_pos == (LAST_ROW_INDEX, LAST_COL_INDEX) and ALLOW_STANDING:
    #     assert directions == {0, 1, 7, 8}

    # convert the new direction to an position (coordinate)
    new_row, new_col = curr_pos[0], curr_pos[1]
    if new_dir in {8, 1, 2}:
        new_row -= 1
    elif new_dir in {6, 5, 4}:
        new_row += 1
    if new_dir in {8, 7, 6}:
        new_col -= 1
    elif new_dir in {2, 3, 4}:
        new_col += 1
    return direction_dict[new_dir], (new_row, new_col)
