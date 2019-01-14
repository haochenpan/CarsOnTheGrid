from random import choice
import config

dir_tbl = {
    0: "•",
    1: "↑",
    2: "→",
    3: "↓",
    4: "←",
}


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


if __name__ == '__main__':

    new_dir_and_pos_set = set()
    pos_1 = (config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX)
    pos_2 = (config.FIRST_ROW_INDEX, config.LAST_COL_INDEX)
    pos_3 = (config.LAST_ROW_INDEX, config.FIRST_COL_INDEX)
    pos_4 = (config.LAST_ROW_INDEX, config.LAST_COL_INDEX)

    for i in range(50):
        new_dir_and_pos = get_new_dir_and_pos((3, 5))
        new_dir_and_pos_set.add(new_dir_and_pos)
    print(new_dir_and_pos_set)
    new_dir_and_pos_set.clear()

