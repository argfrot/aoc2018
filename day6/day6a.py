import datetime
import re
from collections import defaultdict, namedtuple

CHAR_MAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def get_data(parser=str):
    with open('day6/input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

def parse_line(line):
    return tuple(int(coord.strip()) for coord in line.split(','))

def get_bounds(all_points):
    xs, ys = list(zip(*all_points))
    return (min(xs), min(ys)), (max(xs), max(ys))

class Grid(object):

    def __init__(self):
        self.all_points = []
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        self.grid = []

    def add_point(self, point):
        self.all_points.append(point)
        if self.min_x is None or point[0] < self.min_x:
            self.min_x = point[0]
        if self.min_y is None or point[1] < self.min_y:
            self.min_y = point[1]
        if self.max_x is None or point[0] > self.max_x:
            self.max_x = point[0]
        if self.max_y is None or point[1] > self.max_y:
            self.max_y = point[1]
        
    def get_bounds(self):
        return (self.min_x, self.min_y), (self.max_x, self.max_y)
    
    def freeze_points(self):
        self.empty_points = set()
        for j in range(self.min_y, self.max_y+1):
            row = []
            self.grid.append(row)
            for i in range(self.min_x, self.max_x+1):
                try:
                    char = CHAR_MAP[self.all_points.index((i,j))]
                except:
                    char = ' '
                    self.empty_points.add((i-self.min_x,j-self.min_y))
                row.append(char)

    def _get_neighbours(self, point):
        def clip(a,b):
            return (a < 0 or a >= len(self.grid[0]) or
                b < 0 or b >= len(self.grid))

        neighbours = []
        x,y = point
        for n,m in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if not clip(n,m):
                neighbours.append((n,m)                                                                                                                                                                                                                                                                                                                                                            )

        return neighbours

    def _add_closest_point(self, parent_point, point):
        parent_type = self._get_colour_of(parent_point)
        assert parent_type != ' '
        self.empty_points.discard(point)
        self._set_colour_of(point, parent_type)
    
    def _set_closest_point_clash(self, point):
        self._set_colour_of(point, '.')

    def _get_adjusted_points(self):
        for point in self.all_points:
            yield point[0] - self.min_x, point[1] - self.min_y
    
    def _get_colour_of(self, point):
        return self.grid[point[1]][point[0]]

    def _set_colour_of(self, point, colour):
        self.grid[point[1]][point[0]] = colour

    def _is_empty(self, point):
        return point in self.empty_points

    def grow_area(self):
        bfs_queue = []
        next_layer = list(self._get_adjusted_points())
        while(next_layer):
            bfs_queue = next_layer
            next_layer = set()
            for current_point in bfs_queue:
                for neighbour in self._get_neighbours(current_point):
                    if self._is_empty(neighbour):
                        self._add_closest_point(current_point, neighbour)
                        next_layer.add(neighbour)
                    elif neighbour in next_layer and self._get_colour_of(neighbour) != self._get_colour_of(current_point):
                        self._set_closest_point_clash(neighbour)

    def border_colours(self):
        border_colours = set(self.grid[0]).union(
            set(self.grid[-1])).union(
            set([row[0] for row in self.grid])).union(
            set([row[-1] for row in self.grid]))
        return border_colours
    
    def get_finite_areas(self):
        frequency = defaultdict(int)
        border = self.border_colours()
        for row in self.grid:
            for colour in row:
                if colour not in border:
                    frequency[colour] += 1
        return frequency

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid])

values = get_data(parser=parse_line)
bounds = get_bounds(values)
print(f'result A => {len(values)}')
print(f'bounds => {bounds}')

grid = Grid()
for point in values:
    grid.add_point(point)
print(f'{grid.get_bounds()}')

grid.freeze_points()

print(f'{grid}')

grid.grow_area()

print(f'\n==================\n{grid}')

finite_areas = grid.get_finite_areas()
biggest_area = max(finite_areas.values())
print(f'{biggest_area}')
