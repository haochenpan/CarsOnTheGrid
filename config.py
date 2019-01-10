NUM_OF_CARS = 1000
MAX_MOVE = 10

NUM_OF_ROWS = 10
NUM_OF_COLS = 10
FIRST_ROW_INDEX = 1  # 0 or 1
FIRST_COL_INDEX = 1
LAST_ROW_INDEX = NUM_OF_ROWS + FIRST_ROW_INDEX - 1
LAST_COL_INDEX = NUM_OF_COLS + FIRST_COL_INDEX - 1

# [4|8] = [4|8] directions available, 4 = {↑, ↓, ←, →} and 8 = {↑, ↓, ←, →, ↖, ↗, ↙, ↘}
MOVE_DIR_COUNT = 8

# [True|False] = [Can|Cannot] stay in the same block in two consecutive rounds
ALLOW_STANDING = True

# [True|False] = [Cannot|Can] have multiple sources in the first grid
SINGLE_SOURCE_FIRST_GRID = True
assert SINGLE_SOURCE_FIRST_GRID in {True, False}
if SINGLE_SOURCE_FIRST_GRID:
    assert NUM_OF_ROWS * NUM_OF_COLS > 1

# [True|False] = Cars in the same block with source(s)
# [Cannot become a source, just a receiver | Can let others receive the message and become a source]
CONSTANT_SOURCE_THROUGHOUT = False

# ["restricted"|"not-restricted"]
# "restricted": if at border, won't generate the option to move toward the border again
# "not-restricted":
BORDER_BEHAVIOR = "restricted"

GREEN = [0.4745098039215686 * 2, 1.0 * 2, 0.396078431372549 * 2, 1.0 * 2]
RED = [1.0 * 2, 0.2980392156862745 * 2, 0.2980392156862745 * 2, 1.0 * 2]
YELLOW = [0.9372549019607843 * 2, 1.0 * 2, 0.4980392156862745 * 2, 1.0 * 2]
BLUE = [0.4980392156862745 * 2, 1.0 * 2, 1.0 * 2, 1.0 * 2]
