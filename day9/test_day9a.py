import unittest
from day9.day9a import List, insert_after

class TestList(unittest.TestCase):
    
    def test_insert_after_value(self):
        l1 = List(1)
        insert_after(l1, 2)
        self.assertEqual(l1.next.value, 2)

    def test_insert_after_previous(self):
        l1 = List(1)
        insert_after(l1, 2)
        self.assertEqual(l1.next.previous, l1)

if __name__ == '__main__':
    unittest.main()
