import unittest
from day11.day11a import power_level, find_best_fuel_cell, fuel_cell_at, fuel_cell_at_slow

class TestPowerLevel(unittest.TestCase):
    
    def test_power_level_1(self):
        self.assertEqual(power_level(3,5,8), 4)

    def test_power_level_2(self):
        self.assertEqual(power_level(122,79,57), -5)

    def test_power_level_3(self):
        self.assertEqual(power_level(217,196,39), 0)

    def test_power_level_4(self):
        self.assertEqual(power_level(101,153,71), 4)
    
    def test_find_best_fuel_cell(self):
        self.assertEqual(find_best_fuel_cell(18,3), (29, (33,45)))

    def test_fuel_cell_at(self):
        cell_size = 2
        for j in range(1, 301-cell_size):
            for i in range(1, 301-cell_size):
                self.assertEqual(fuel_cell_at(i,j,cell_size,18), fuel_cell_at_slow(i,j,cell_size,18), f'{i} {j}')

    def test_fuel_cell_at_simple(self):
        self.assertEqual(fuel_cell_at(3,1,2,18), -1)

    def test_fuel_cell_at_slow(self):
        self.assertEqual(fuel_cell_at_slow(3,1,2,18), -1)

if __name__ == '__main__':
    unittest.main()
