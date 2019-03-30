
def get_data(parser=str):
    with open('day12/input.txt', 'r') as f:
        values = list(filter(None, [parser(line) for line in f.readlines()]))
    return values

class Automata(object):
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.rules = {}
        self.left_index = 0
    
    def add_rule(self, state, result):
        self.rules[state] = result
    
    def _pad(self):
        self.left_index -= 4
        self.current_state = (False, False, False, False) + self.current_state + (False, False, False, False)

    def _unpad(self, state):
        first = state.index(True)
        last = tuple(reversed(state)).index(True)
        self.current_state = tuple(state[first:len(state)-last])
        self.left_index += (first+2)

    def run(self):
        self._pad()
        next_state = []
        index = 0
        while(index < len(self.current_state)):
            group = self.current_state[index:index+5]
            next_state.append(self.rules.get(group, False))
            index += 1
        self._unpad(next_state)

    def value(self):
        index = self.left_index
        total = 0
        for plant in self.current_state:
            if plant:
                total += index
            index += 1
        return total

    def __str__(self):
        return str(self.left_index) + ' ' + ''.join('#' if x else '.' for x in self.current_state)


# position=< 9,  1> velocity=< 0,  2>
def parse_line(line):
    words = line.split()
    if line.startswith('initial state'):
        return parse_state(words[2])
    elif len(words):
        return (parse_state(words[0]), parse_state(words[2])[0])

def parse_state(state):
    state_map = {'.': False, '#': True}
    return tuple(map(lambda x: state_map[x], state))

def run():
    values = get_data(parser=parse_line)
    print(f'{values}')
    ca = Automata(values[0])
    print(f'{ca}')
    for rule, result in values[1:]:
        ca.add_rule(rule, result)
    for generation in range(120):
        if generation%10000==0:
            print(f'{generation} - {ca.left_index} - {ca}')
        ca.run()
    ca.left_index = 50000000000 - 75

    print(f'{ca.value()}')

    # solution is 4350000000957
    # pattern repeats from about 110 generations, the left index being 75 less
    # than the generation,nbut just shifts along each time


if __name__ == "__main__":
    run()
