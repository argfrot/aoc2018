from collections import defaultdict

def get_data():
    with open('input.txt', 'r') as f:
        values = [line for line in f.readlines()]
    return values

def get_frequency(word):
    freq = defaultdict(int)
    for c in word:
        freq[c] += 1
    return freq

def checksum(values):
    twos = 0
    threes = 0
    for line in values:
        f = get_frequency(line)
        if 2 in f.values():
            twos += 1
        if 3 in f.values():
            threes += 1
    return twos * threes

values = get_data()
result = checksum(values)
print(result)
