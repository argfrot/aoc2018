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

class Node(object):

    def __init__(self, node_type):
        self.node_type = node_type
        self.dependents = {}
        self.requirements = {}

    def depends_upon(self, other):
        self.requirements[other.node_type] = other
        other.dependents[self.node_type] = self

    def can_begin(self):
        return not len(self.requirements)

    def trigger(self, requirement):
        try:
            self.requirements.pop(requirement.node_type)
        except KeyError:
            pass

    def complete(self):
        next_nodes = []
        for dependent in self.dependents.values():
            dependent.trigger(self)
            if dependent.can_begin():
                next_nodes.append(dependent)
        return next_nodes
    
#    def duration(self):
#        return 1 + (ord(self.node_type) - ord('A'))

    def duration(self):
        return 61 + (ord(self.node_type) - ord('A'))

    def __lt__(self, other):
        return self.node_type < other.node_type

    def __str__(self):
        return self.node_type

    def __repr__(self):
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
            if node.can_begin():
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

    def parallel_traverse(self, num_workers):
        done = []
        doing = []
        current_time = 0
        bfs_queue = list(self.iter_roots())
        heapq.heapify(bfs_queue)

        while(bfs_queue or doing):
            while(doing and doing[0][0] == current_time):
                _, completed = heapq.heappop(doing)
                done.append(completed.node_type)
                triggered = completed.complete()
                for node in triggered:
                    heapq.heappush(bfs_queue, node)
            while(bfs_queue and len(doing) < num_workers):
                next = heapq.heappop(bfs_queue)
                heapq.heappush(doing, (current_time + next.duration(), next))
            if doing:
                current_time = doing[0][0]
            print(f'{current_time} - {doing}')

        return ''.join(done)


values = get_data(parser=parse_line)
print(f'inputs => {len(values)}')

graph = Graph()
for dependency in values:
    graph.add_edge(dependency.first, dependency.then)

#traversal_order = graph.traverse()
#print(f'{traversal_order}')

traversal_order = graph.parallel_traverse(num_workers=5)
print(f'{traversal_order}')
