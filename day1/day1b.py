def get_data():
    with open('input.txt', 'r') as f:
        values = [int(line) for line in f.readlines()]
    return values

def find_repeating_frequency(values):
    already_seen = set()
    current_frequency = 0
    already_seen.add(current_frequency)
    while(True):
        for v in values:
            current_frequency += v
            if current_frequency in already_seen:
                return current_frequency
            already_seen.add(current_frequency)

values = get_data()
repeat = find_repeating_frequency(values)
print(repeat)
