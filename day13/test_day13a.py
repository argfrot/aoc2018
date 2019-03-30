import unittest
from day13.day13a import Direction, RelativeDirection, Node, Position, Grid, Cart

class TestDirection(unittest.TestCase):
    
    def test_opposite(self):
        self.assertEqual(Direction.opposite(Direction.NORTH), Direction.SOUTH)
        self.assertEqual(Direction.opposite(Direction.SOUTH), Direction.NORTH)
        self.assertEqual(Direction.opposite(Direction.EAST), Direction.WEST)
        self.assertEqual(Direction.opposite(Direction.WEST), Direction.EAST)

    def test_move(self):
        position = Position(column=5, row=10)
        self.assertEqual(Direction.move(position, Direction.NORTH), Position(5,9))
        self.assertEqual(Direction.move(position, Direction.SOUTH), Position(5,11))
        self.assertEqual(Direction.move(position, Direction.EAST), Position(6,10))
        self.assertEqual(Direction.move(position, Direction.WEST), Position(4,10))

class TestRelativeDirection(unittest.TestCase):

    def test_turn_west(self):
        self.assertEqual(RelativeDirection.turn(Direction.NORTH, RelativeDirection.LEFT), Direction.WEST)
        self.assertEqual(RelativeDirection.turn(Direction.SOUTH, RelativeDirection.RIGHT), Direction.WEST)
        self.assertEqual(RelativeDirection.turn(Direction.WEST, RelativeDirection.STRAIGHT), Direction.WEST)

    def test_turn_east(self):
        self.assertEqual(RelativeDirection.turn(Direction.SOUTH, RelativeDirection.LEFT), Direction.EAST)
        self.assertEqual(RelativeDirection.turn(Direction.NORTH, RelativeDirection.RIGHT), Direction.EAST)
        self.assertEqual(RelativeDirection.turn(Direction.EAST, RelativeDirection.STRAIGHT), Direction.EAST)

    def test_turn_north(self):
        self.assertEqual(RelativeDirection.turn(Direction.EAST, RelativeDirection.LEFT), Direction.NORTH)
        self.assertEqual(RelativeDirection.turn(Direction.WEST, RelativeDirection.RIGHT), Direction.NORTH)
        self.assertEqual(RelativeDirection.turn(Direction.NORTH, RelativeDirection.STRAIGHT), Direction.NORTH)

    def test_turn_south(self):
        self.assertEqual(RelativeDirection.turn(Direction.WEST, RelativeDirection.LEFT), Direction.SOUTH)
        self.assertEqual(RelativeDirection.turn(Direction.EAST, RelativeDirection.RIGHT), Direction.SOUTH)
        self.assertEqual(RelativeDirection.turn(Direction.SOUTH, RelativeDirection.STRAIGHT), Direction.SOUTH)

    def test_next_turn(self):
        self.assertEqual(RelativeDirection.next(RelativeDirection.LEFT), RelativeDirection.STRAIGHT)
        self.assertEqual(RelativeDirection.next(RelativeDirection.STRAIGHT), RelativeDirection.RIGHT)
        self.assertEqual(RelativeDirection.next(RelativeDirection.RIGHT), RelativeDirection.LEFT)
        
class TestGrid(unittest.TestCase):

    def test_add_point(self):
        p1 = Position(2,3)
        p2 = Position(1,5)
        grid = Grid()
        grid.add_node(p1, Node(p1), link_edges=[])
        grid.add_node(p2, Node(p2), link_edges=[])
        self.assertEqual(grid.min_col, 1)
        self.assertEqual(grid.max_col, 2)
        self.assertEqual(grid.min_row, 3)
        self.assertEqual(grid.max_row, 5)

    def test_link_points(self):
        p1 = Position(0,0)
        p2 = Position(1,0)
        grid = Grid()
        n1 = Node(p1)
        n2 = Node(p2)
        grid.add_node(p1, n1, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p2, n2, link_edges=[Direction.EAST, Direction.WEST])
        self.assertEqual(n1.east, n2)
        self.assertEqual(n2.west, n1)

    def test_collision_detection(self):
        p1 = Position(0,0)
        p2 = Position(1,0)
        p3 = Position(2,0)
        p4 = Position(3,0)
        grid = Grid()
        n1 = Node(p1)
        n2 = Node(p2)
        n3 = Node(p3)
        n4 = Node(p4)
        grid.add_node(p1, n1, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p2, n2, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p3, n3, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p4, n4, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_cart(Cart(n2, Direction.EAST))
        grid.add_cart(Cart(n3, Direction.WEST))
        with self.assertRaises(Exception):
            grid.move()

    def test_collision_detection_removal(self):
        p1 = Position(0,0)
        p2 = Position(1,0)
        p3 = Position(2,0)
        p4 = Position(3,0)
        grid = Grid()
        n1 = Node(p1)
        n2 = Node(p2)
        n3 = Node(p3)
        n4 = Node(p4)
        grid.add_node(p1, n1, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p2, n2, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p3, n3, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p4, n4, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_cart(Cart(n2, Direction.EAST))
        grid.add_cart(Cart(n3, Direction.WEST))
        grid.move(remove_cart_on_collision=True)
        self.assertEqual(len(grid.carts), 0)

    def test_collision_detection_removal_again(self):
        p1 = Position(0,0)
        p2 = Position(1,0)
        p3 = Position(2,0)
        p4 = Position(3,0)
        grid = Grid()
        n1 = Node(p1)
        n2 = Node(p2)
        n3 = Node(p3)
        n4 = Node(p4)
        grid.add_node(p1, n1, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p2, n2, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p3, n3, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_node(p4, n4, link_edges=[Direction.EAST, Direction.WEST])
        grid.add_cart(Cart(n2, Direction.EAST))
        grid.add_cart(Cart(n3, Direction.EAST))
        grid.add_cart(Cart(n4, Direction.WEST))
        grid.move(remove_cart_on_collision=True)
        self.assertEqual(len(grid.carts), 1)

if __name__ == '__main__':
    unittest.main()
