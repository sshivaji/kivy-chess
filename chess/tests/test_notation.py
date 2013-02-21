import unittest

import sys; sys.path.extend(['../', './'])
from position import Position
from move import Move
from notation import SanNotation

#XXX Abstract - using SanNotation to test.
class TestAbstractNotation(unittest.TestCase):

    def setUp(self):
        p = Position()
        self.moves = p.get_legal_moves()
        m1 = Move.from_uci('e2e4')
        m2 = Move.from_uci('b1c3')
        self.san = SanNotation(p, m1)
        self.san_dup = SanNotation(p, m1)
        self.san_other = SanNotation(p, m2)
        self.position = p
        self.m1 = m1
        self.m2 = m2

    def test___eq__(self):
        self.assertEqual(True, self.san.__eq__(self.san_dup))
        self.assertEqual(False, self.san.__eq__(self.san_other))

    def test___hash__(self):
        self.assertEqual(True, hash(self.san) == hash(self.san_dup))
        self.assertEqual(False, hash(self.san) == hash(self.san_other))

    def test___init__(self):
        for move in self.moves:
            san = SanNotation(self.position, move)

    def test___ne__(self):
        self.assertEqual(False, self.san.__ne__(self.san_dup))
        self.assertEqual(True, self.san.__ne__(self.san_other))

    def test___str__(self):
        self.assertEqual('e4', str(self.san))
        self.assertEqual('Nc3', str(self.san_other))

    def test_text(self):
        self.assertEqual('e4', (self.san.text))
        self.assertEqual('Nc3', (self.san_other.text))


class TestSanNotation(TestAbstractNotation):

    def test_to_move(self):
        SanNotation.to_move(self.position, self.san) == self.m1

if __name__ == '__main__':
    unittest.main()
