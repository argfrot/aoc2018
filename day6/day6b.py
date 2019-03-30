import datetime
import operator
import re
from collections import defaultdict, namedtuple, deque

CHAR_MAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def get_data(parser=str):
    with open('day6/input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

Point = namedtuple('Point', ['column', 'row'])

def parse_line(line):
    return Point(*(int(coord.strip()) for coord in line.split(',')))


class Node(object):
    def __init__(self):
        self.colour = None
        self.distances = {} # distance from each point

    @property
    def closest(self):
        if self.colour:
            return (self.colour, 0)
        elif self.distances:
            in_order = sorted(self.distances.items(), key=operator.itemgetter(1))
            if len(in_order) == 1 or in_order[0][1] < in_order[1][1]:
                return in_order[0]
            else:
                return (None, None)
        else:
            return (None, None)

    @property
    def closest_colour(self):
        return self.closest[0]

    @property
    def total_distance(self):
        return sum(self.distances.values())
    
    def visit_by(self, colour, distance):
        if colour == self.colour:
            return False
        if colour not in self.distances:
            self.distances[colour] = distance
            return True
        elif distance < self.distances[colour]:
            self.distances[colour] = distance
            return True
        return False

    def __str__(self):
        return self.closest_colour


class Grid(object):

    def __init__(self):
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        self.grid = defaultdict(lambda: defaultdict(lambda: Node()))
    
    def iter_origin_points(self):
        for row in range(self.min_y, self.max_y+1):
            for column in range(self.min_x, self.max_x+1):
                point = Point(column, row)
                node = self.get_node_at_point(point)
                if node.colour is not None:
                    yield (point, node)

    def iter_border(self):
        for row in range(self.min_y, self.max_y+1):
            for column in range(self.min_x, self.max_x+1):
                if column in (self.min_x, self.max_x) or row in (self.min_y, self.max_y):
                    point = Point(column, row)
                    node = self.get_node_at_point(point)
                    yield (point, node)

    def iter_all_points(self):
        for row in range(self.min_y, self.max_y+1):
            for column in range(self.min_x, self.max_x+1):
                point = Point(column, row)
                node = self.get_node_at_point(point)
                yield (point, node)

    def add_point(self, point, point_type):
        self.grid[point.row][point.column].colour = point_type
        if self.min_x is None or point.column < self.min_x:
            self.min_x = point.column
        if self.min_y is None or point.row < self.min_y:
            self.min_y = point.row
        if self.max_x is None or point.column > self.max_x:
            self.max_x = point.column
        if self.max_y is None or point.row > self.max_y:
            self.max_y = point.row

    def get_node_at_point(self, point):
        return self.grid[point.row][point.column]

    def is_point_occupied(self, point):
        return point.column in self.grid[point.row]
        
    def get_bounds(self):
        return (self.min_x, self.min_y), (self.max_x, self.max_y)

    def _get_neighbours(self, point):
        def clip(row, column):
            return (row < self.min_y or row > self.max_y or
                column < self.min_x or column > self.max_x)

        neighbours = []
        x, y = point.column, point.row
        for column,row in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if not clip(row,column):
                neighbours.append(Point(column,row))

        return neighbours
    
    def grow_area(self):
        bfs_queue = deque((node.colour, 0, point) for (point, node) in self.iter_origin_points())
        while(bfs_queue):
            colour, distance, point = bfs_queue.popleft()
            for neighbour in self._get_neighbours(point):
                if self.get_node_at_point(neighbour).visit_by(colour, distance+1):
                    bfs_queue.append((colour, distance+1, neighbour))

    def border_colours(self):
        return set(node.closest_colour for (point, node) in self.iter_border())
    
    def get_finite_areas(self):
        frequency = defaultdict(int)
        border = self.border_colours()
        for (_, node) in self.iter_all_points():
            colour = node.closest_colour
            if colour not in border:
                frequency[colour] += 1
        return frequency

    def get_internal_area(self, max_distance=10000):
        internal_count = 0
        for (_, node) in self.iter_all_points():
            if node.total_distance < max_distance:
                internal_count += 1
        return internal_count

    def __str__(self):
        def _iter_nodes():
            for row in range(self.min_y, self.max_y+1):
                for column in range(self.min_x, self.max_x+1):
                    point = Point(column, row)
                    node = self.get_node_at_point(point)
                    yield node.closest_colour if node.closest_colour else '.'
                yield '\n'
        return ''.join(_iter_nodes())

    def distance_str(self, max_distance=32):
        def _iter_nodes():
            for row in range(self.min_y, self.max_y+1):
                for column in range(self.min_x, self.max_x+1):
                    point = Point(column, row)
                    node = self.get_node_at_point(point)
                    yield node.colour if node.colour else '#' if node.total_distance < max_distance else '.'
                yield '\n'
        return ''.join(_iter_nodes())


values = get_data(parser=parse_line)
print(f'result A => {len(values)}')

grid = Grid()
for i, point in enumerate(values):
    grid.add_point(point, CHAR_MAP[i])
print(f'{grid.get_bounds()}')

print(f'{grid}')

grid.grow_area()

print(f'\n==================\n{grid}')

finite_areas = grid.get_finite_areas()
biggest_area = max(finite_areas.values())
print(f'{biggest_area}')

# print(f'{finite_areas}')
# print(f'{grid.border_colours()}')

# print(f'{grid.distance_str()}')

# node = grid.get_node_at_point(Point(column=4, row=3))
# print(f'{node.distances} - {node.total_distance}')

print(f'{grid.get_internal_area(max_distance=10000)}')
