import datetime
import operator
import re
from collections import defaultdict, namedtuple
import heapq
from functools import lru_cache, partial
import numpy as np
import time

def hundreds_digit(n):
    n //= 100
    return n % 10

def power_level(cell_column, cell_row, serial_number):
    rack_id = cell_column + 10
    power_level = rack_id * cell_row
    power_level += serial_number
    power_level *= rack_id
    power_level = hundreds_digit(power_level)
    return power_level - 5

def build_power_grid(serial_number, width=300):
    def np_pl(row, col):
        return power_level(col+1, row+1, serial_number=serial_number)
    return np.fromfunction(np_pl, (width,width))

def fuel_cell_at(grid, column, row, cell_size):
    if cell_size == 1:
        return grid[row-1, column-1]
    else:
        return grid[row-1:row-1+cell_size,column-1:column-1+cell_size].sum()

def fuel_cell_at_recurse(grid):
    @lru_cache(maxsize=None)
    def fuel_cell_at_memo(column, row, cell_size):
        if cell_size == 1:
            return grid[row-1, column-1]
        else:
            total = fuel_cell_at_memo(column, row, cell_size-1)
            total += grid[row-1:row-1+cell_size, column-1+cell_size-1].sum()
            total += grid[row-1+cell_size-1, column-1:column-1+cell_size-1].sum()
            return total
    return fuel_cell_at_memo

def find_best_fuel_cell(grid, cell_size):
    max_pl = 0
    max_pl_at = None

    for row in range(1, 301-cell_size):
        for column in range(1, 301-cell_size):
            pl = fuel_cell_at(grid, column, row, cell_size)
            if pl > max_pl:
                max_pl = pl
                max_pl_at = (column, row)
    
    return (max_pl, max_pl_at)

def find_best_fuel_cell_any_size(grid):
    max_pl = None
    max_size = None

    for cell_size in range(1,300):
        t1 = time.time()
        pl = find_best_fuel_cell(grid, cell_size)
        t2 = time.time()
        diff = t2 - t1
        print(f'{cell_size}: {diff}')
        if max_pl is None or pl > max_pl:
            max_pl = pl
            max_size = cell_size

    return (max_pl, max_size)


def find_best_fuel_cell_recurse(fc_func, cell_size):
    max_pl = 0
    max_pl_at = None

    for row in range(1, 301-cell_size):
        for column in range(1, 301-cell_size):
            pl = fc_func(column, row, cell_size)
            if pl > max_pl:
                max_pl = pl
                max_pl_at = (column, row)
    
    return (max_pl, max_pl_at)

def find_best_fuel_cell_any_size_recurse(grid):
    fc_func = fuel_cell_at_recurse(grid)
    max_pl = None
    max_size = None

    for cell_size in range(1,300):
        t1 = time.time()
        pl = find_best_fuel_cell_recurse(fc_func, cell_size)
        t2 = time.time()
        diff = t2 - t1
        print(f'{cell_size}: {diff}')
        if max_pl is None or pl > max_pl:
            max_pl = pl
            max_size = cell_size

    return (max_pl, max_size)

def run():
    grid = build_power_grid(18)
    cell = fuel_cell_at(grid,33,45,3).sum()
    print(f'{cell}')
    grid = build_power_grid(42)
    print(f'{find_best_fuel_cell(grid, 3)}')
    grid = build_power_grid(9445)
    print(f'{find_best_fuel_cell(grid, 3)}')
    print(f'{find_best_fuel_cell_any_size_recurse(grid)}')

if __name__ == "__main__":
    run()
