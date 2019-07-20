import unittest
from main import *


class NCarTest(unittest.TestCase):
    def test_init(self):
        c1 = Car(0, "1", True, (0, 0), [(1, 0), (2, 0), (3, 0)])
        self.assertEqual(c1.when, 0)
        self.assertEqual(c1.trace, [(0, 0)])
        self.assertEqual(c1.targets, [(0, 0), (1, 0), (2, 0), (3, 0)])
        self.assertEqual(c1.target_idx, 1)

        c1 = Car(0, "1", False, (1, 1))
        self.assertEqual(c1.when, -1)
        self.assertEqual(c1.trace, [(1, 1)])
        self.assertEqual(c1.targets, [(1, 1)])
        self.assertEqual(c1.target_idx, 1)

    def test_get_target(self):
        c1 = Car(0, "1", False, (1, 1))
        self.assertEqual(c1.when, -1)
        self.assertEqual(c1.trace, [(1, 1)])
        self.assertEqual(c1.targets, [(1, 1)])
        self.assertEqual(c1.target_idx, 1)
        c1._set_target()
        self.assertEqual(c1.target_idx, 1)
        self.assertEqual(len(c1.targets), 2)

        c1 = Car(0, "1", False, (1, 1), [(2, 2)])
        self.assertEqual(c1.when, -1)
        self.assertEqual(c1.trace, [(1, 1)])
        self.assertEqual(c1.targets, [(1, 1), (2, 2)])
        self.assertEqual(c1.target_idx, 1)
        self.assertEqual(c1.get_target(), (2, 2))
        self.assertEqual(c1.target_idx, 1)
        self.assertEqual(len(c1.targets), 2)

    def test_move(self):
        c1 = Car(0, "1", True, (0, 0), [(10, 0)])
        self.assertEqual(c1.when, 0)
        self.assertEqual(len(c1.trace), 1)
        for _ in range(9):
            c1.move()
            self.assertEqual(c1.target_idx, 1)
            self.assertEqual(len(c1.targets), 2)
        c1.move()
        self.assertEqual(c1.target_idx, 2)
        c1.get_target()
        self.assertEqual(len(c1.targets), 3)

        c1 = Car(0, "1", True, (3, 3), [(4, 2)])
        self.assertEqual(c1.when, 0)
        self.assertEqual(len(c1.trace), 1)
        c1.move()
        self.assertEqual(c1.target_idx, 1)
        self.assertEqual(len(c1.targets), 2)
        pos = c1.get_position()
        self.assertAlmostEqual(pos[0], 3.70710, 4)
        self.assertAlmostEqual(pos[1], 2.29289, 4)

        c1 = Car(0, "1", True, (3, 3), [(2, 4)])
        self.assertEqual(c1.when, 0)
        self.assertEqual(len(c1.trace), 1)
        c1.move()
        self.assertEqual(c1.target_idx, 1)
        self.assertEqual(len(c1.targets), 2)
        pos = c1.get_position()
        self.assertAlmostEqual(pos[0], 2.29289, 4)
        self.assertAlmostEqual(pos[1], 3.70710, 4)

        c1 = Car(0, "1", True, (3, 3), [(9, 2)])
        self.assertEqual(c1.when, 0)
        self.assertEqual(len(c1.trace), 1)

        c1.move()
        self.assertEqual(c1.target_idx, 1)
        self.assertEqual(len(c1.targets), 2)
        pos = c1.get_position()
        self.assertAlmostEqual(pos[0], 3.98639, 4)
        self.assertAlmostEqual(pos[1], 2.83560, 4)

        c1.move()
        self.assertEqual(c1.target_idx, 1)
        self.assertEqual(len(c1.targets), 2)
        pos = c1.get_position()
        self.assertAlmostEqual(pos[0], 4.97278, 4)
        self.assertAlmostEqual(pos[1], 2.67120, 4)

    def test_source(self):
        c1 = Car(0, "1", True, (0, 0), [(0, 0)])
        c1.move()
        self.assertEqual(c1.trace, [(0, 0), (0, 0)])
        self.assertEqual(c1.targets, [(0, 0), (0, 0)])
        self.assertEqual(c1.target_idx, 1)
        c1.move()
        self.assertEqual(c1.trace, [(0, 0), (0, 0), (0, 0)])
        self.assertEqual(c1.targets, [(0, 0), (0, 0)])
        self.assertEqual(c1.target_idx, 1)

        c1 = Car(0, "1", True, (0, 0), [(1, 0), (1, 0)])
        c1.move()
        self.assertEqual(c1.trace, [(0, 0), (1, 0)])
        self.assertEqual(c1.targets, [(0, 0), (1, 0), (1, 0)])
        self.assertEqual(c1.target_idx, 2)
        c1.move()
        self.assertEqual(c1.trace, [(0, 0), (1, 0), (1, 0)])
        self.assertEqual(c1.targets, [(0, 0), (1, 0), (1, 0)])
        self.assertEqual(c1.target_idx, 2)


if __name__ == '__main__':
    pass
