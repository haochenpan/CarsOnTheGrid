"""
    Program configurations and validations
"""
"""
    Definitions and terminologies (Version 01/11/2019, according to the email discussion):
    Source: The first car holds the message, generate at the run time, has id = FIRST_CAR_INDEX.
    Broadcaster: If a car holds the message, it is a broadcaster. The source is the first broadcaster.
    Receiver: same as broadcaster.
    Round: A snapshot of cars in the grid. Cars are initiated in the 0th round, NUM_OF_MOVES-th round is the last round.
"""
"""Grid and cars"""
NUM_OF_ROWS = 20
NUM_OF_COLS = 20

NUM_OF_CARS = 1000
NUM_OF_MOVES = 10

# car movement:
# [True|False] = [Can|Cannot] stay in the same block in two consecutive rounds
ALLOW_STANDING = True

"""Preferences"""
FIRST_ROW_INDEX = 0  # 0 or 1
FIRST_COL_INDEX = 0
FIRST_CAR_INDEX = 0


# [4|8] = [4|8] directions available, 4 = {↑, ↓, ←, →} and 8 = {↑, ↓, ←, →, ↖, ↗, ↙, ↘}
# NUM_OF_DIRS = 4

# [True|False] = [Cannot|Can] have multiple sources in the first grid
# HAS_SINGLE_SOURCE = False

# [True|False] = Cars in the same block with source(s)
# [Cannot become a source, just a receiver | Can let others receive the message and become a source]
# CONST_NUM_OF_SOURCE = False

# ["restricted"|"not-restricted"]
# "restricted": if at border, won't generate the option to move toward the border again
# "not-restricted":
# BORDER_BEHAVIOR = "restricted"

LAST_ROW_INDEX = NUM_OF_ROWS + FIRST_ROW_INDEX - 1
LAST_COL_INDEX = NUM_OF_COLS + FIRST_COL_INDEX - 1
GREEN = [0.48 * 2, 1.0 * 2, 0.4 * 2, 1.0 * 2]
RED = [1.0 * 2, 0.3 * 2, 0.3 * 2, 1.0 * 2]
YELLOW = [0.94 * 2, 1.0 * 2, 0.5 * 2, 1.0 * 2]
BLUE = [0.5 * 2, 1.0 * 2, 1.0 * 2, 1.0 * 2]

assert NUM_OF_CARS >= 2, "need at least 2 cars, one is the source and one is not"
assert NUM_OF_ROWS * NUM_OF_COLS >= 2, "need at least 2 blocks to store the source and other cars"

