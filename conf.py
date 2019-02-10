"""
    Program descriptions, configurations and validations

    Definitions and terminologies:
        Source:         The first car that holds the message, its id = FIRST_CAR_INDEX.
        Broadcaster:    If a car holds the message, it is a broadcaster, thus the source is the first broadcaster.
        Receiver:       = Broadcaster.
        Round:          A snapshot of cars in the grid. Cars are initiated at the 0th round, 
                        NUM_OF_MOVES moves and propagates are performed in a simulation,
                        and NUM_OF_MOVES-th round is the last round.

    Program Structure:
        conf.py:      Program descriptions, configurations and validations
        gui.py:         User control Gui / Snapshot Generation
        help.py:        The home of helper functions
        main.py:        Generates a simulation
        simulation.py:  Continuous simulation with threading, database connectivity
        stats_gui.py:   Generates a scatter plot from the results of simulations
        test.py:        Unit tests (not complete)

    Developer plans, not in particular order:
        TODO(Haochen): Analyze blind run data, quantify measurements. Why broadcast fast/slow?
        Reorganize the code, move this part and other memos to readme file
        Add more unit tests
        User defined source position and route, will that accelerate message broadcasting?
        Movement Model for all cars, how that will affect message broadcasting? Any new efficient strategies?

"""

"""
    Common Configs - Grid and cars
"""
NUM_OF_ROWS = 20
NUM_OF_COLS = 20

NUM_OF_CARS = 1000
NUM_OF_MOVES = 80  # number of moves and propagates

# car movement:
# [True|False] = [Can|Cannot] stay in the same block in two consecutive rounds
ALLOW_STANDING = True


"""
    Common Configs - Preferences
"""
FIRST_ROW_INDEX = 0  # often 0 or 1
FIRST_COL_INDEX = 0
FIRST_CAR_INDEX = 0


"""
    GUI Configs
"""
PADDING = 0.1  # 0.1/0.2
COUNT_PER_ROW_COL = 9  # 9/4 cars per row/col
FRAMES = 30


"""
    (No need to modify) Frequently used variables and shorthand notations
"""
LAST_ROW_INDEX = NUM_OF_ROWS + FIRST_ROW_INDEX - 1
LAST_COL_INDEX = NUM_OF_COLS + FIRST_COL_INDEX - 1
NOR = NUM_OF_ROWS
NOC = NUM_OF_COLS
FRI = FIRST_ROW_INDEX
FCI = FIRST_COL_INDEX
LRI = LAST_ROW_INDEX
LCI = LAST_COL_INDEX

"""
    Variable that keeps track the current position of the source card
    Not used Yet.
"""
SOURCE_CURRENT_ROW = 0
SOURCE_CURRENT_COL = 0

"""
    Variable needed for restricting the source car it the middle
"""
# True: The source car should only be restricted in the middle area;
# False: Other Cases
RESTRICTING_MIDDLE = True

# Middle Row
MR = NUM_OF_ROWS / 2
# Middle Column
MC = NUM_OF_COLS / 2
# Middle_Pos:
MID_POS = (MR, MC)

# Length of the Restricting rows
RESTRICTING_MIDDLE_ROW_LEN = 3
# Length of the Restricting cols
RESTRICTING_MIDDLE_COL_LEN = 3

# Restricting the border of the sour car
RESTRICTING_MIDDLE_TOP_BORDER = int(MR - ((RESTRICTING_MIDDLE_ROW_LEN + 1) / 2))
RESTRICTING_MIDDLE_BOTTOM_BORDER = int(MR + (RESTRICTING_MIDDLE_ROW_LEN / 2))
RESTRICTING_MIDDLE_LEFT_BORDER = int(MC - ((RESTRICTING_MIDDLE_COL_LEN + 1) / 2))
RESTRICTING_MIDDLE_RIGHT_BORDER = int(MC + (RESTRICTING_MIDDLE_COL_LEN / 2))