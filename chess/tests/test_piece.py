import unittest

import sys; sys.path.extend(['../', './'])
import piece
from piece import Piece

class TestPiece(unittest.TestCase):
    def test_color(self):
        self.assertEqual(piece.WHITE, Piece.color('P'))
        self.assertEqual(piece.BLACK, Piece.color('p'))

    def test_enum(self):
        self.assertEqual(piece.W_PAWN, Piece.enum('P'))

    def test_from_klass_and_color(self):
        self.assertEqual('P', Piece.from_klass_and_color(piece.PAWN, piece.WHITE))

    def test_is_klass_and_color(self):
        self.assertEqual(True, Piece.is_klass_and_color('P', piece.PAWN, piece.WHITE))

    def test_klass(self):
        self.assertEqual(piece.PAWN, Piece.klass('P'))

if __name__ == '__main__':
    unittest.main()
