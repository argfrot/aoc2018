import datetime
import operator
import re
from collections import defaultdict, namedtuple
import heapq

def get_data(parser=str):
    with open('day7/input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

Dependency = namedtuple('Dependency', ['first', 'then'])

#Step Y must be finished before step L can begin.
def parse_line(line):
    words = line.split()
    return Dependency(first=words[1], then=words[7])

# A -> Z
# G -> Z
# A -> G

# A-D-|
#     +-Z
#   G-|

#A.immediate_children -= G.all_descendants
#A.immediate_children += G

#   |-D-|
# A-+   +-Z
#   |-G-|

# A - G - Z

# A -> G
# B -> G

# A -|
#    +- G
# B -|

class Node(object):

    def __init__(self, node_type):
        self.node_type = node_type
        self.dependents = {}
        self.requirements = {}

    def depends_upon(self, other):
        self.requirements[other.node_type] = other
        other.dependents[self.node_type] = self

    def can_complete(self):
        return not self.requirements

    def trigger(self, requirement):
        try:
            self.requirements.pop(requirement.node_type)
        except KeyError:
            pass

    def complete(self):
        next_nodes = []
        for dependent in self.dependents.values():
            dependent.trigger(self)
            if dependent.can_complete():
                next_nodes.append(dependent)
        return next_nodes

    def __lt__(self, other):
        return self.node_type < other.node_type

    def __str__(self):
        return self.node_type


class Graph(object):

    def __init__(self):
        self.nodes = {}

    def add_node(self, node_type):
        node = self.nodes.get(node_type)
        if node is None:
            node = Node(node_type)
            self.nodes[node_type] = node
        return node

    def add_edge(self, first, then):
        n1 = self.add_node(first)
        n2 = self.add_node(then)
        n2.depends_upon(n1)
    
    def iter_roots(self):
        for node in self.nodes.values():
            if node.can_complete():
                yield node

    def traverse(self):
        traversal_order = []
        bfs_queue = list(self.iter_roots())
        heapq.heapify(bfs_queue)
        while(bfs_queue):
            next = heapq.heappop(bfs_queue)
            traversal_order.append(next.node_type)
            triggered = next.complete()
            for node in triggered:
                heapq.heappush(bfs_queue, node)
        return ''.join(traversal_order)


values = get_data(parser=parse_line)
print(f'inputs => {len(values)}')

graph = Graph()
for dependency in values:
    graph.add_edge(dependency.first, dependency.then)

traversal_order = graph.traverse()
print(f'{traversal_order}')
