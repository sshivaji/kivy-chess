import unittest

import sys; sys.path.extend(['../', './'])
from position import Position
from move import Move
from notation import SanNotation
from piece import WHITE, BLACK
from fen import Fen

class TestPosition(unittest.TestCase):
    
    def setUp(self):
        self.pos = Position()
        self.pos_dup = Position()
        self.pos_other = Position()
        self.pos_other.make_move(Move.from_uci('e2e4'))

    def test___delitem__(self):
        del self.pos['a1']
        self.assertIs(None, self.pos['a1'])

    def test___eq__(self):
        self.assertEqual(True, self.pos == self.pos_dup)
        self.assertEqual(False, self.pos == self.pos_other)

    def test___getitem__(self):
        self.assertEqual(True, self.pos['e1'] == 'K')

    def test___hash__(self):
        self.assertEqual(True, hash(self.pos) == hash(self.pos_dup))
        self.assertEqual(False, hash(self.pos) != hash(self.pos_other))

    def test___ne__(self):
        self.assertEqual(False, self.pos != self.pos_dup)
        self.assertEqual(True, self.pos != self.pos_other)

    def test___repr__(self):
        self.assertEqual("Position('%s')" % Fen(), repr(self.pos))

    def test___setitem__(self):
        self.pos['a1'] = 'K'
        self.assertEqual('K', self.pos['a1'])

    def test___str__(self):
        self.assertEqual(str(Fen()), str(self.pos))
        self.assertEqual(False, str(self.pos) == str(self.pos_other))

    def test_copy(self):
        copy = self.pos.copy()
        self.assertEqual(copy, self.pos)

    def test_is_check(self):
        self.assertEqual(False, self.pos.is_check())

    def test_is_checkmate(self):
        self.assertEqual(False, self.pos.is_checkmate())

    def test_is_game_over(self):
        self.assertEqual(False, self.pos.is_game_over())

    def test_is_insufficient_material(self):
        self.assertEqual(False, self.pos.is_insufficient_material())

    def test_is_king_attacked(self):
        self.assertEqual(False, self.pos.is_king_attacked(WHITE))

    def test_is_stalemate(self):
        self.assertEqual(False, self.pos.is_stalemate())


if __name__ == '__main__':
    unittest.main()
