"""
    Program descriptions, configurations and validations
"""

"""
    Definitions and terminologies (Version 01/11/2019, according to the email discussion):
        Source:         The first car holds the message, generate at the run time,
                        has id = FIRST_CAR_INDEX.
        Broadcaster:    If a car holds the message, it is a broadcaster.
                        The source is the first broadcaster.
        Receiver:       The same as broadcaster.
        Round:          A snapshot of cars in the grid. Cars are initiated in the 0th round,
                        and NUM_OF_MOVES-th round is the last round.
"""

"""
    Common Configs - Grid and cars
"""
NUM_OF_ROWS = 10
NUM_OF_COLS = 10

NUM_OF_CARS = 500
NUM_OF_MOVES = 10

# car movement:
# [True|False] = [Can|Cannot] stay in the same block in two consecutive rounds
ALLOW_STANDING = True

"""
    Common Configs - Preferences
"""
FIRST_ROW_INDEX = 0  # 0 or 1
FIRST_COL_INDEX = 0
FIRST_CAR_INDEX = 0

"""
    GUI Configs
"""
PADDING = 0.1  # 0.1/0.2
COUNT_PER_ROW_COL = 9  # 9/4 elems per row / col
FRAMES = 30

"""
    (Do not modify) Frequently Used Variables and Validations
"""

LAST_ROW_INDEX = NUM_OF_ROWS + FIRST_ROW_INDEX - 1
LAST_COL_INDEX = NUM_OF_COLS + FIRST_COL_INDEX - 1

