import unittest

import sys; sys.path.extend(['../', './'])
from x88 import X88
import piece

class TestX88(unittest.TestCase):
    def test_from_index(self):
        self.assertEqual(X88.from_index(0), 0)

    def test_from_x_and_y(self):
        self.assertEqual(X88.from_x_and_y(0,0), 0)

    def test_is_backrank(self):
        self.assertEqual(X88.is_backrank(0, piece.BLACK), True)

    def test_is_secondrank(self):
        self.assertEqual(X88.is_secondrank(8, piece.WHITE), True)

    def test_to_index(self):
        self.assertEqual(X88.to_index(0), 0)

    def test_to_x(self):
        self.assertEqual(X88.to_x(0), 0)

    def test_to_y(self):
        self.assertEqual(X88.to_y(0), 0)

if __name__ == '__main__':
    unittest.main()
