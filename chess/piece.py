# -*- coding: utf-8 -*-
#
# This file is part of the python-chess library.
# Copyright (C) 2012 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
# Copyright (C) 2013 Nathaniel Carson https://github.com/nate1001/python-chess
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

BLACK, WHITE = range(2)
COLORS = {'w': WHITE, 'b': BLACK}

PIECECLASSES = \
	PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = range(6)

PIECES = \
	B_PAWN, B_KNIGHT, B_BISHOP, B_ROOK, B_QUEEN, B_KING, \
	W_PAWN, W_KNIGHT, W_BISHOP, W_ROOK, W_QUEEN, W_KING = range(12)


class Piece(object):
    """Static class for working with characters that represent a piece.

    >>> import chess
    >>> chess.Piece.color("Q") == chess.WHITE
    True
    >>> chess.Piece.klass("Q") == chess.QUEEN
    True
    """
    # XXX order is important for all strings. see enums at top
    piececlass = 'pnbrqk'
    promote_to = 'nbrq'
    pieces = 'pnbrqkPNBRQK'
    castleclass = 'KQkq'

    castle_squares = {
        'K': (('e1', W_KING), ('h1', W_ROOK)),
        'Q': (('e1', W_KING), ('a1', W_ROOK)),
        'k': (('e8', B_KING), ('h8', B_ROOK)),
        'q': (('e8', B_KING), ('a8', B_ROOK)),
    }

    @staticmethod
    def opposite_color(color):
        if color == WHITE:
            return BLACK
        elif color == BLACK:
            return WHITE
        raise ValueError(color)


    @classmethod
    def color(cls, piece):
        """Returns the color enemuration from chess.COLORS."""
        try:
            if cls.pieces.index(piece) < len(PIECECLASSES):
                return BLACK
            else:
                return WHITE
        except ValueError:
            raise ValueError(piece)

    @classmethod
    def klass(cls, piece):
        """Returns the type of piece without regards to color from chess.PIECECLASSES."""
        try:
            return cls.piececlass.index(piece.lower())
        except ValueError:
            raise ValueError(piece)
    
    @classmethod
    def enum(cls, piece):
        """Returns the type of piece with regards to color from chess.PIECES."""
        try:
            return cls.pieces.index(piece)
        except ValueError:
            raise ValueError(piece)
    
    @classmethod
    def is_klass_and_color(cls, piece, klass, color):
        """Returns True if piece is of a chess.PIECECLASSES and chess.COLOR."""
        return cls.color(piece) == color and cls.klass(piece) == klass

    @classmethod
    def from_klass_and_color(cls, klass, color):
        """Returns the piece from chess.PIECES."""
        offset = color * len(PIECECLASSES)
        try:
            return cls.pieces[klass + offset]
        except IndexError:
            raise ValueError((klass, color))

