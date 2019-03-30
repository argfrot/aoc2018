import datetime
import operator
import re
from collections import defaultdict, namedtuple
import heapq

def get_data(parser=str):
    with open('day13/input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

Position = namedtuple('Position', ['column', 'row'])

class Direction(object):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def next_direction(direction):
        return (direction+1)%4

    @staticmethod
    def move(position, direction):
        if direction == Direction.NORTH:
            return Position(position.column, position.row-1)
        elif direction == Direction.EAST:
            return Position(position.column+1, position.row)
        elif direction == Direction.SOUTH:
            return Position(position.column, position.row+1)
        elif direction == Direction.WEST:
            return Position(position.column-1, position.row)

    @staticmethod        
    def opposite(direction):
        return (direction+2)%4
    
    @staticmethod
    def to_str(direction):
        heading_map = {
            Direction.NORTH : '^',
            Direction.EAST : '>',
            Direction.SOUTH : 'v',
            Direction.WEST : '<',
        }
        return heading_map[direction]

    @staticmethod
    def from_str(direction):
        heading_map = {
            '^' : Direction.NORTH,
            '>' : Direction.EAST,
            'v' : Direction.SOUTH,
            '<' : Direction.WEST,
        }
        return heading_map[direction]


class RelativeDirection(object):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1

    @staticmethod
    def turn(heading, relative_direction):
        return (heading + relative_direction)%4
    
    @staticmethod
    def next(relative_direction):
        return ((relative_direction+2)%3)-1


class Node(object):
    def __init__(self, position):
        self.position = position
        self.outgoing_edges = {}

    def possible_edges(self):
        return self.outgoing_edges.keys()
    
    def set_neighbour(self, direction, neighbour):
        self.outgoing_edges[direction] = neighbour

    @property
    def north(self):
        return self.outgoing_edges.get(Direction.NORTH)

    @property
    def east(self):
        return self.outgoing_edges.get(Direction.EAST)

    @property
    def south(self):
        return self.outgoing_edges.get(Direction.SOUTH)

    @property
    def west(self):
        return self.outgoing_edges.get(Direction.WEST)
    
    def __str__(self):
        edge_lookup = {
            (Direction.NORTH, Direction.WEST) : '/',
            (Direction.EAST, Direction.SOUTH) : '/',
            (Direction.EAST, Direction.WEST) : '-',
            (Direction.NORTH, Direction.EAST) : '\\',
            (Direction.SOUTH, Direction.WEST) : '\\',
            (Direction.NORTH, Direction.SOUTH) : '|',
            (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST) : '+',
        }
        return edge_lookup[tuple(sorted(self.outgoing_edges.keys()))]

class Cart(object):
    def __init__(self, node, heading):
        self.node = node
        self.heading = heading
        self.next_turn = RelativeDirection.LEFT

    def _next_node(self):
        if self.heading == Direction.NORTH:
            return self.node.north
        elif self.heading == Direction.EAST:
            return self.node.east
        elif self.heading == Direction.SOUTH:
            return self.node.south
        elif self.heading == Direction.WEST:
            return self.node.west

    def move(self):
        self.node = self._next_node()
        if len(list(self.node.possible_edges())) > 2:
            # when at a cross-roads, turn according to the next turn state
            self.heading = RelativeDirection.turn(self.heading, self.next_turn)
            self.next_turn = RelativeDirection.next(self.next_turn)
        else:
            # turn to face the way out of this node
            for direction in self.node.possible_edges():
                if direction != Direction.opposite(self.heading):
                    self.heading = direction
                    break
    
    def position(self):
        return self.node.position
    
    def __str__(self):
        return Direction.to_str(self.heading)

class Grid(object):
    def __init__(self):
        self.nodes = {}
        self.carts = []
        self._reset_limits()
    
    def add_node(self, position, node, link_edges):
        self.nodes[position] = node
        for direction in link_edges:
            next_position = Direction.move(position, direction)
            other_node = self.nodes.get(next_position)
            if not other_node:
                other_node = Node(next_position)
                self.nodes[next_position] = other_node
            node.set_neighbour(direction, other_node)
            other_node.set_neighbour(Direction.opposite(direction), node)
        self._update_limits(position)

    def add_cart(self, cart):
        self.carts.append(cart)

    def get_node(self, position):
        return self.nodes.get(position)

    def _reset_limits(self):
        self.min_row = None
        self.max_row = None
        self.min_col = None
        self.max_col = None

    def _update_limits(self, position):
        self.min_row = min(self.min_row, position.row) if self.min_row is not None else position.row
        self.max_row = max(self.max_row, position.row) if self.max_row is not None else position.row
        self.min_col = min(self.min_col, position.column) if self.min_col is not None else position.column
        self.max_col = max(self.max_col, position.column) if self.max_col is not None else position.column

    def move(self, remove_cart_on_collision=False):
        positions = {cart.position(): cart for cart in self.carts}
        carts = sorted(self.carts, key=lambda c: (c.position().row, c.position().column))
        for cart in carts:
            try:
                positions.pop(cart.position())
            except KeyError:
                continue
            cart.move()
            position = cart.position()
            if position in positions:
                if not remove_cart_on_collision:
                    raise Exception(f'Collision at {position}!')
                else:
                    self.carts.remove(cart)
                    self.carts.remove(positions[position])
                    positions.pop(position)
            else:
                positions[position] = cart
    
    def __str__(self):
        cart_map = {cart.position(): cart for cart in self.carts}

        def _iter_nodes():
            for row in range(self.min_row, self.max_row+1):
                yield "%3d " % row
                for column in range(self.min_col, self.max_col+1):
                    position = Position(column, row)
                    if position in cart_map:
                        yield str(cart_map[position])
                    else:
                        node = self.get_node(position)
                        yield str(node) if node else ' '
                yield '\n'
        return ''.join(_iter_nodes())

def build_grid(data):
    edge_lookup = {
        '/' : set(),
        '-' : {Direction.WEST, Direction.EAST},
        '\\' : set(),
        '|' : {Direction.NORTH, Direction.SOUTH},
        '+' : {Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST},
        '>' : {Direction.WEST, Direction.EAST},
        '<' : {Direction.WEST, Direction.EAST},
        '^' : {Direction.NORTH, Direction.SOUTH},
        'v' : {Direction.NORTH, Direction.SOUTH},
    }
    grid = Grid()
    for row, line in enumerate(data):
        for column, character in enumerate(line):
            position = Position(column, row)
            link_edges = edge_lookup.get(character)
            if link_edges is not None:
                node = grid.get_node(position) or Node(position)
                grid.add_node(position, node, link_edges)
                if character in "<>^v":
                    grid.add_cart(Cart(node, Direction.from_str(character)))
    return grid

def run():
    values = get_data()
    grid = build_grid(values)
    print(f'{str(grid)}')
    print(f'{list(c.position() for c in grid.carts)}')

    step = 1
    while True:
        print(f'{step}')
        grid.move(remove_cart_on_collision=True)
        step += 1
        if len(grid.carts) <= 1:
            print(f'{list(c.position() for c in grid.carts)}')
            break

    print(f'{str(grid)}')

if __name__ == "__main__":
    run()
