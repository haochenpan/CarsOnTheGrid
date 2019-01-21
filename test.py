from collections import defaultdict
import unittest
import config
import helplib


def base_config_assertions():
    assert config.NUM_OF_ROWS >= 1
    assert config.NUM_OF_COLS >= 1
    assert config.NUM_OF_MOVES >= 2
    assert config.NUM_OF_CARS >= 2, "need at least 2 cars, one is the source and one is not"
    assert config.NUM_OF_ROWS * config.NUM_OF_COLS >= 2, "need at least 2 blocks to store the source and other cars"


class SimulationTestCase(unittest.TestCase):
    def setUp(self):
        base_config_assertions()
        self.grid, self.source_pos = helplib.init_grid()

    def test_init_grid(self):
        self.assertEqual(len(self.grid[self.source_pos]), 1, "ensure the single source car")
        cars_count = 0
        for cars in self.grid.values():
            cars_count += len(cars)
        self.assertEqual(cars_count, config.NUM_OF_CARS)

    def test_rand_position_generation(self):
        config.ALLOW_STANDING = True
        directions = defaultdict(lambda: 0)
        for i in range(100000):
            curr_pos = helplib.get_rand_pos()
            next_pos = helplib.get_new_dir_and_pos(curr_pos)
            directions[next_pos[0]] += 1
        self.assertEqual(len(directions), 5)
        print(dict(directions))

        config.ALLOW_STANDING = False
        directions = defaultdict(lambda: 0)
        for i in range(100000):
            curr_pos = helplib.get_rand_pos()
            next_pos = helplib.get_new_dir_and_pos(curr_pos)
            directions[next_pos[0]] += 1
        self.assertEqual(len(directions), 4)
        print(dict(directions))

    def test_rand_position_at_corners(self):
        config.ALLOW_STANDING = True
        left_upper_corner_set = set()
        for i in range(50):
            left_upper_corner = helplib.get_new_dir_and_pos((config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX))
            left_upper_corner_set.add(left_upper_corner)
        self.assertEqual(left_upper_corner_set, {('↓', (config.FIRST_ROW_INDEX + 1, config.FIRST_COL_INDEX)),
                                                 ('•', (config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX)),
                                                 ('→', (config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX + 1))})
        left_lower_corner_set = set()
        for i in range(50):
            left_lower_corner = helplib.get_new_dir_and_pos((config.LAST_ROW_INDEX, config.FIRST_COL_INDEX))
            left_lower_corner_set.add(left_lower_corner)
        self.assertEqual(left_lower_corner_set, {('↑', (config.LAST_ROW_INDEX - 1, config.FIRST_COL_INDEX)),
                                                 ('•', (config.LAST_ROW_INDEX, config.FIRST_COL_INDEX)),
                                                 ('→', (config.LAST_ROW_INDEX, config.FIRST_COL_INDEX + 1))})
        right_upper_corner_set = set()
        for i in range(50):
            right_upper_corner = helplib.get_new_dir_and_pos((config.FIRST_ROW_INDEX, config.LAST_COL_INDEX))
            right_upper_corner_set.add(right_upper_corner)
        self.assertEqual(right_upper_corner_set, {('←', (config.FIRST_ROW_INDEX, config.LAST_COL_INDEX - 1)),
                                                  ('•', (config.FIRST_ROW_INDEX, config.LAST_COL_INDEX)),
                                                  ('↓', (config.FIRST_ROW_INDEX + 1, config.LAST_COL_INDEX))})
        right_lower_corner_set = set()
        for i in range(50):
            right_lower_corner = helplib.get_new_dir_and_pos((config.LAST_ROW_INDEX, config.LAST_COL_INDEX))
            right_lower_corner_set.add(right_lower_corner)
        self.assertEqual(right_lower_corner_set, {('↑', (config.LAST_ROW_INDEX - 1, config.LAST_COL_INDEX)),
                                                  ('•', (config.LAST_ROW_INDEX, config.LAST_COL_INDEX)),
                                                  ('←', (config.LAST_ROW_INDEX, config.LAST_COL_INDEX - 1))})

        config.ALLOW_STANDING = False
        left_upper_corner_set = set()
        for i in range(50):
            left_upper_corner = helplib.get_new_dir_and_pos((config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX))
            left_upper_corner_set.add(left_upper_corner)
        self.assertEqual(left_upper_corner_set, {('↓', (config.FIRST_ROW_INDEX + 1, config.FIRST_COL_INDEX)),
                                                 ('→', (config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX + 1))})
        left_lower_corner_set = set()
        for i in range(50):
            left_lower_corner = helplib.get_new_dir_and_pos((config.LAST_ROW_INDEX, config.FIRST_COL_INDEX))
            left_lower_corner_set.add(left_lower_corner)
        self.assertEqual(left_lower_corner_set, {('↑', (config.LAST_ROW_INDEX - 1, config.FIRST_COL_INDEX)),
                                                 ('→', (config.LAST_ROW_INDEX, config.FIRST_COL_INDEX + 1))})
        right_upper_corner_set = set()
        for i in range(50):
            right_upper_corner = helplib.get_new_dir_and_pos((config.FIRST_ROW_INDEX, config.LAST_COL_INDEX))
            right_upper_corner_set.add(right_upper_corner)
        self.assertEqual(right_upper_corner_set, {('←', (config.FIRST_ROW_INDEX, config.LAST_COL_INDEX - 1)),
                                                  ('↓', (config.FIRST_ROW_INDEX + 1, config.LAST_COL_INDEX))})
        right_lower_corner_set = set()
        for i in range(50):
            right_lower_corner = helplib.get_new_dir_and_pos((config.LAST_ROW_INDEX, config.LAST_COL_INDEX))
            right_lower_corner_set.add(right_lower_corner)
        self.assertEqual(right_lower_corner_set, {('↑', (config.LAST_ROW_INDEX - 1, config.LAST_COL_INDEX)),
                                                  ('←', (config.LAST_ROW_INDEX, config.LAST_COL_INDEX - 1))})


if __name__ == '__main__':
    unittest.main()
