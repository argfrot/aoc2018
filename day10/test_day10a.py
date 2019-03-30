import unittest
from day10.day10a import Point, Position, Velocity, Grid

class TestPoint(unittest.TestCase):
    
    def test_move_point(self):
        p1 = Point(Position(2,3), Velocity(-1,1))
        p1.move()
        self.assertEqual(p1.position, Position(1,4))


class TestGrid(unittest.TestCase):

    def test_add_point(self):
        p1 = Point(Position(2,3), Velocity(100, -100))
        p2 = Point(Position(1,5), Velocity(100, -100))
        grid = Grid()
        grid.add_point(p1)
        grid.add_point(p2)
        self.assertEqual(grid.min_col, 1)
        self.assertEqual(grid.max_col, 2)
        self.assertEqual(grid.min_row, 3)
        self.assertEqual(grid.max_row, 5)

    def test_move_points(self):
        p1 = Point(Position(2,3), Velocity(1, 5))
        p2 = Point(Position(1,5), Velocity(5, -5))
        grid = Grid()
        grid.add_point(p1)
        grid.add_point(p2)
        grid.move()
        self.assertEqual(p1.position, Position(3, 8))
        self.assertEqual(p2.position, Position(6, 0))
        self.assertEqual(grid.min_col, 3)
        self.assertEqual(grid.max_col, 6)
        self.assertEqual(grid.min_row, 0)
        self.assertEqual(grid.max_row, 8)


if __name__ == '__main__':
    unittest.main()
