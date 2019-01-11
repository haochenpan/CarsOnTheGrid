NUM_OF_CARS = 1000
NUM_OF_MOVES = 10

NUM_OF_ROWS = 20
NUM_OF_COLS = 20

FIRST_ROW_INDEX = 0  # 0 or 1
FIRST_COL_INDEX = 0

# [4|8] = [4|8] directions available, 4 = {↑, ↓, ←, →} and 8 = {↑, ↓, ←, →, ↖, ↗, ↙, ↘}
NUM_OF_DIRS = 8

# [True|False] = [Can|Cannot] stay in the same block in two consecutive rounds
ALLOW_STANDING = True

# [True|False] = [Cannot|Can] have multiple sources in the first grid
HAS_SINGLE_SOURCE = True

# [True|False] = Cars in the same block with source(s)
# [Cannot become a source, just a receiver | Can let others receive the message and become a source]
CONST_NUM_OF_SOURCE = False

# ["restricted"|"not-restricted"]
# "restricted": if at border, won't generate the option to move toward the border again
# "not-restricted":
BORDER_BEHAVIOR = "restricted"

LAST_ROW_INDEX = NUM_OF_ROWS + FIRST_ROW_INDEX - 1
LAST_COL_INDEX = NUM_OF_COLS + FIRST_COL_INDEX - 1
GREEN = [0.4745098039215686 * 2, 1.0 * 2, 0.396078431372549 * 2, 1.0 * 2]
RED = [1.0 * 2, 0.2980392156862745 * 2, 0.2980392156862745 * 2, 1.0 * 2]
YELLOW = [0.9372549019607843 * 2, 1.0 * 2, 0.4980392156862745 * 2, 1.0 * 2]
BLUE = [0.4980392156862745 * 2, 1.0 * 2, 1.0 * 2, 1.0 * 2]

assert NUM_OF_DIRS in {4, 8}
assert ALLOW_STANDING in {True, False}
assert HAS_SINGLE_SOURCE in {True, False}
if HAS_SINGLE_SOURCE:
    assert NUM_OF_ROWS * NUM_OF_COLS > 1
assert CONST_NUM_OF_SOURCE in {True, False}
