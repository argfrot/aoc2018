import datetime
import operator
import re
from collections import defaultdict, namedtuple
import heapq
from functools import lru_cache
import time

def hundreds_digit(n):
    n //= 100
    return n % 10

@lru_cache(maxsize=None)
def power_level(cell_column, cell_row, serial_number):
    #print(f'{cell_column},{cell_row}')
    rack_id = cell_column + 10
    power_level = rack_id * cell_row
    power_level += serial_number
    power_level *= rack_id
    power_level = hundreds_digit(power_level)
    return power_level - 5

@lru_cache(maxsize=None)
def fuel_cell_at(column, row, cell_size, serial_number):
    if cell_size == 1:
        return power_level(column, row, serial_number)
    else:
        total = fuel_cell_at(column, row, cell_size-1, serial_number)
        for j in range(cell_size):
            total += power_level(column+cell_size-1, row+j, serial_number)
        for i in range(cell_size-1):
            total += power_level(column+i, row+cell_size-1, serial_number)
        return total

def fuel_cell_at_slow(column, row, cell_size, serial_number):
        total = 0
        for j in range(cell_size):
            for i in range(cell_size):
                total += power_level(column+i, row+j, serial_number)
        return total

def find_best_fuel_cell(serial_number, cell_size):
    max_pl = 0
    max_pl_at = None

    for row in range(1, 301-cell_size):
        for column in range(1, 301-cell_size):
            pl = fuel_cell_at(column, row, cell_size, serial_number)
            if pl > max_pl:
                max_pl = pl
                max_pl_at = (column, row)
    
    return (max_pl, max_pl_at)

def find_best_fuel_cell_any_size(serial_number):
    max_pl = None
    max_size = None

    for cell_size in range(1,300):
        t1 = time.time()
        pl = find_best_fuel_cell(serial_number, cell_size)
        t2 = time.time()
        diff = t2 - t1
        print(f'{cell_size}: {diff}')
        if max_pl is None or pl > max_pl:
            max_pl = pl
            max_size = cell_size

    return (max_pl, max_size)

def run():
    print(f'{find_best_fuel_cell_any_size(18)}')
    print(f'{find_best_fuel_cell_any_size(9445)}')

if __name__ == "__main__":
    run()
