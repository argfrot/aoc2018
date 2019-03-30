import datetime
import re
from collections import defaultdict, namedtuple

def get_data(parser=str):
    with open('input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

def collapse_adjacent(c1, c2):
    if c1.isupper() and c2.isupper():
        return False
    elif c1.islower() and c2.islower():
        return False
    elif c1.upper() == c2.upper():
        return True
    else:
        return False

def _collapse_line(line):
    last_char = None
    for c in line:
        if last_char is None:
            last_char = c
        elif collapse_adjacent(last_char, c):
            last_char = None
        else:
            yield last_char
            last_char = c
    if last_char is not None:
        yield last_char

def collapse_line(line):
    return ''.join(list(_collapse_line(line)))

def collapse(line):
    iteration = 0
    new_line = collapse_line(line)
    while(line != new_line):
        iteration += 1
        line = new_line
        new_line = collapse_line(line)
    #print(f'{iteration}')
    return new_line

values = get_data()[0].strip()
#result = collapse('BBBBbAaammmmmBMMMMmmmmbMMMMMAACBBbbcaBaaazzzZZZAAABbbBbbGGggbb')
#result = collapse('dabAcCaCBAcCcaDA')
result = collapse(values)
print(f'result A => {len(result)}')

unit_types = sorted(list(set([c.upper() for c in values])))
for unit_type in unit_types:
    result = collapse(''.join(filter(lambda x: x not in (unit_type, unit_type.lower()), values)))
    print(f'result B {unit_type} => {len(result)}')
