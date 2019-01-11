from random import choice
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


def get_new_dir_and_pos(curr_pos: tuple) -> tuple:
    """
    Generate a new random direction and the corresponding position base on the current position
    :param curr_pos: The current position coordinate (i.e. (x, y)) of the car
    :return: The direction and position coordinate (i.e. (d, (x, y)))
    """
    if config.BORDER_BEHAVIOR == "restricted":
        return get_new_dir_and_pos_res(curr_pos)
    else:
        raise Exception


def get_new_dir_and_pos_res(curr_pos: tuple) -> tuple:
    if config.NUM_OF_DIRS == 8:
        directions = {1, 2, 3, 4, 5, 6, 7, 8}  # all possible directions
    else:
        directions = {1, 3, 5, 7}

    if config.ALLOW_STANDING:
        directions.add(0)

    # removes directions that a border block does not have
    if curr_pos[0] == config.FIRST_ROW_INDEX:
        directions.difference_update({8, 1, 2})
    if curr_pos[0] == config.LAST_ROW_INDEX:
        directions.difference_update({6, 5, 4})
    if curr_pos[1] == config.FIRST_COL_INDEX:
        directions.difference_update({8, 7, 6})
    if curr_pos[1] == config.LAST_COL_INDEX:
        directions.difference_update({2, 3, 4})

    # choose a random direction
    assert len(directions) > 0
    new_dir = choice(tuple(directions))

    # convert the new direction to an position coordinate
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


if __name__ == '__main__':

    # TODO(Haochen): formal assertion tests
    new_dir_and_pos_set = set()
    for i in range(50):
        new_dir_and_pos = get_new_dir_and_pos((0, 5))
        new_dir_and_pos_set.add(new_dir_and_pos)
    print(new_dir_and_pos_set)
