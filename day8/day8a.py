import datetime
import operator
import re
from collections import defaultdict, namedtuple
import heapq

def get_data(parser=str):
    with open('day8/input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

#Record = namedtuple('Record', ['children', 'metadata'])

class Record(object):
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

#    @property   
#    def value(self):
#        return sum(self.metadata)

    @property
    def value(self):
        if not self.children:
            return sum(self.metadata)

        total = 0
        for index in self.metadata:
            try:
                total += self.children[index-1].value
            except IndexError:
                pass
        return total

def parse_line(line):
    return parse_record(line)

def parse_record(line):
    split = line.split(maxsplit=2)
    if len(split) == 3:
        n, m, rest = split
    else:
        n, m = split
        rest = None
    num_children = int(n)
    num_metadata = int(m)
    children = []
    metadata = []

    for _ in range(num_children):
        child, rest = parse_record(rest)
        children.append(child)

    for _ in range(num_metadata):
        split = rest.split(maxsplit=1)
        if len(split) == 2:
            md, rest = split
        else:
            md, rest = split[0], None
        metadata.append(int(md))

    return (Record(children, metadata), rest)

def sum_metadata(root):
    next = [root]
    total = 0
    while(next):
        current_node = next.pop()
        total += current_node.value
        next.extend(current_node.children)
    return total

values = get_data(parser=parse_line)
#print(f'inputs => {values}')

total = sum_metadata(values[0][0])
print(f'{total}')

print(f'{values[0][0].value}')
