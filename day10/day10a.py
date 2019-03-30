import datetime
import operator
import re
from collections import defaultdict, namedtuple
import heapq

def get_data(parser=str):
    with open('day10/input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

Position = namedtuple('Position', ['column', 'row'])
Velocity = namedtuple('Velocity', ['delta_column', 'delta_row'])

class Point(object):
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
    
    def move(self):
        self.position = Position(*map(sum, zip(self.position, self.velocity)))
    
    def reverse(self):
        self.position = Position(*map(lambda x: x[0]-x[1], zip(self.position, self.velocity)))


class Grid(object):
    def __init__(self):
        self.points = []
        self._reset_limits()
    
    def add_point(self, point):
        self.points.append(point)
        self._update_limits(point)

    def _reset_limits(self):
        self.min_row = None
        self.max_row = None
        self.min_col = None
        self.max_col = None

    def _update_limits(self, point):
        self.min_row = min(self.min_row, point.position.row) if self.min_row is not None else point.position.row
        self.max_row = max(self.max_row, point.position.row) if self.max_row is not None else point.position.row
        self.min_col = min(self.min_col, point.position.column) if self.min_col is not None else point.position.column
        self.max_col = max(self.max_col, point.position.column) if self.max_col is not None else point.position.column

    def move(self):
        self._reset_limits()
        for point in self.points:
            point.move()
            self._update_limits(point)
    
    def reverse(self):
        self._reset_limits()
        for point in self.points:
            point.reverse()
            self._update_limits(point)

    def area(self):
        return (self.max_col+1 - self.min_col) * (self.max_row+1 - self.min_row)

    def __str__(self):
        positions = set(p.position for p in self.points)
        def _iter_nodes():
            for row in range(self.min_row, self.max_row+1):
                for column in range(self.min_col, self.max_col+1):
                    point = Position(column, row)
                    yield '#' if point in positions else '.'
                yield '\n'
        return ''.join(_iter_nodes())


# position=< 9,  1> velocity=< 0,  2>
def parse_line(line):
    words = re.split("[<>]+", line)
    position = Position(*map(lambda x: int(x.strip()), words[1].split(",")))
    velocity = Velocity(*map(lambda x: int(x.strip()), words[3].split(",")))
    return (position, velocity)

def run():
    values = get_data(parser=parse_line)
    grid = Grid()
    for point in values:
        grid.add_point(Point(*point))

    area = grid.area()
    for seconds in range(15000):
        print(f'{seconds} -- {grid.area()}')
        grid.move()
        if grid.area() >= area:
            grid.reverse()
            print(f'{str(grid)}')
            break
        area = grid.area()


if __name__ == "__main__":
    run()
