import unittest

import sys; sys.path.extend(['../', './'])
from fen import Fen, FenError
from square import Square

class TestFen(unittest.TestCase):
    def test___eq__(self):
        self.assertEqual(True, Fen().__eq__(Fen()))

    def test___getitem__(self):
        fen = Fen()
        self.assertEqual('R', fen.__getitem__(Square('a1')))

    def test___hash__(self):
        hash(Fen())

    def test___init__(self):

        Fen()
        Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1')
        Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - e3 0 1')

        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP w KQkq - 0')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/71/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        with self.assertRaises(FenError):
            Fen('Znbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/ppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR Z KQkq - 0 1')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w ZQkq - 0 1')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - e4 0 1')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - Z 1')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0')
        with self.assertRaises(FenError):
            Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 Z')

    def test___ne__(self):
        self.assertEqual(False, Fen().__ne__(Fen()))

    def test___repr__(self):
        # fen = Fen(fen)
        self.assertEqual('Fen(\'' + Fen.start + '\')', Fen().__repr__())

    def test___setitem__(self):
        f, s = Fen(), Square('a1')
        f[s] = 'K'
        self.assertEqual('K', f[s])

    def test___str__(self):
        self.assertEqual(Fen.start, Fen().__str__())

    def test_castle_rights(self):
        self.assertEqual('KQkq', Fen().castle_rights)

    def test_ep_square(self):
        self.assertEqual('-', Fen().ep_square)

    def test_fifty_move(self):
        self.assertEqual(0, Fen().fifty_move)

    def test_fullmove(self):
        self.assertEqual(1, Fen().full_move)

    def test_text(self):
        self.assertEqual(Fen.start, Fen().text)

    def test_turn(self):
        self.assertEqual('w', Fen().turn)

if __name__ == '__main__':
    unittest.main()
