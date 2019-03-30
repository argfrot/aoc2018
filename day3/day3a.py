import re
from collections import defaultdict, namedtuple

def get_data(parser=str):
    with open('input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

# #1 @ 1,3: 4x4
LINE_REGEXP = re.compile(r'#(?P<entry_id>\d*) @ (?P<col>\d*),(?P<row>\d*): (?P<width>\d*)x(?P<height>\d*)')

def parse_line(line):
    m = LINE_REGEXP.match(line)
    return m.groupdict()

class Grid(object):

    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(list))
        self.non_overlapping_rectangles = set()
    
    def add_rectangle(self, entry_id, col, row, width, height):
        self.non_overlapping_rectangles.add(entry_id)
        for i in range(row, row+height):
            for j in range(col, col+width):
                if self.data[i][j]:
                    for eid in self.data[i][j]:
                        self.non_overlapping_rectangles.discard(eid)
                    self.non_overlapping_rectangles.discard(entry_id)
                self.data[i][j].append(entry_id)
    
    def count_overlap(self):
        count = 0

        for row in self.data.values():
            for col in row.values():
                if len(col) > 1:
                    count += 1

        return count

    def get_non_overlapping(self):
        return self.non_overlapping_rectangles

def build_grid(rectangles):
    grid = Grid()
    for rectangle in rectangles:
        rectangle = {k: int(v) for (k,v) in rectangle.items()}
        grid.add_rectangle(**rectangle)
    return grid

values = get_data(parser=parse_line)
grid = build_grid(values)
print(grid.count_overlap())
print(grid.get_non_overlapping())
