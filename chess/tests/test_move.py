import unittest

import sys; sys.path.extend(['../', './'])
from square import Square
from move import Move
from chess import MoveError

def gen_moves():
    for source in Square.get_all():
        for target in Square.get_all():
            if target != source:
                yield(Move(source, target))
        

class TestMove(unittest.TestCase):
    def test___eq__(self):
        source = Square('a1')
        target = Square('a2')
        promotion = 'q'
        move1 = Move(source, target)
        move2 = Move(source, target)
        self.assertEqual(True, move1.__eq__(move2))

    def test___hash__(self):
        d = {}
        for idx, move in enumerate(gen_moves()):
            d[hash(move)] = None
        self.assertEqual(idx + 1, len(d))

    def test___init__(self):
        with self.assertRaises(ValueError):
            Move(Square('a1'), Square('a1'))

        with self.assertRaises(ValueError):
            m = Move.from_uci('a1a2q')

        for move in gen_moves():
            pass

    def test___ne__(self):
        source = Square('a1')
        target = Square('a2')
        promotion = 'q'
        move1 = Move(source, target)
        move2 = Move(source, target)
        self.assertEqual(False, move1.__ne__(move2))

    def test___repr__(self):
        m = gen_moves().next()
        self.assertEqual("Move.from_uci('a1b1')", repr(m))

    def test___str__(self):
        m = gen_moves().next()
        self.assertEqual('a1b1', str(m))

    def test_from_uci(self):
        m = Move.from_uci('a1a2')
        self.assertEqual('a1a2', str(m))

    def test_from_x88(self):
        m = Move.from_x88(0, 1)
        self.assertEqual('a1b1', str(m))

    def test_promotion(self):
        m = Move.from_uci('a1a2')
        self.assertEqual('', m.promotion)

        m = Move.from_uci('a1a8q')
        self.assertEqual('q', m.promotion)

    def test_source(self):
        m = Move.from_uci('a1a2')
        self.assertEqual(Square('a1'), m.source)

    def test_target(self):
        m = Move.from_uci('a1a2')
        self.assertEqual(Square('a2'), m.target)

    def test_uci(self):
        m = Move.from_uci('a1a2')
        self.assertEqual('a1a2', m.uci)

    def test_equality(self):
        """Tests the custom equality behaviour of the move class."""
        a = Move(Square("a1"), Square("a2"))
        b = Move(Square("a1"), Square("a2"))
        c = Move(Square("h7"), Square("h8"), "b")
        d = Move(Square("h7"), Square("h8"))

        self.assertEqual(a, b)
        self.assertEqual(b, a)

        self.assertNotEqual(a, c)
        self.assertNotEqual(c, d)
        self.assertNotEqual(b, d)

    def test_uci_parsing(self):
        """Tests the UCI move parsing."""
        self.assertEqual(Move.from_uci('b5c7').uci, 'b5c7')
        self.assertEqual(Move.from_uci('e7e8q').uci, 'e7e8q')

if __name__ == '__main__':
    unittest.main()
