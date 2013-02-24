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

from piece import Piece
from square import Square

class MoveError(ValueError):
    """Thrown when a move in invalid."""

class Move(object):
    """Represents a move.

    :param source:
        The source square.
    :param target:
        The target square.
    :param promotion:
        Optional. If given this indicates which piece a pawn has been
        promoted to: %s.

    >>> import chess
    >>> e4 = chess.Move(chess.Square("e2"), chess.Square("e4"))
    >>> e4 == chess.Move.from_uci("e2e4")
    True
    """ % ', '.join(list(Piece.promote_to))

    _x88_moves = {}

    def __init__(self, source, target, promotion=''):

        promotion and Piece.promote_to.index(promotion)

        if source == target:
            raise ValueError(
                "Source and target cannot be the same: %s, %s." %(source, target))

        if promotion and promotion not in Piece.promote_to:
            raise ValueError(
                "Invalid promotion piece: %s.", repr(promotion))

        if promotion and not target.is_backrank():
            raise ValueError(
                "Promotion move even though target is not a backrank square.")

        self._source_x88 = source.x88
        self._target_x88 = target.x88
        self._promotion = promotion or ''

    @property
    def uci(self):
        """The UCI move string like `"a1a2"` or `"b7b8q"`."""
        return str(self)
    
    @property
    def source(self):
        """The source square."""
        return Square.from_x88(self._source_x88)

    @property
    def target(self):
        """The target square."""
        return Square.from_x88(self._target_x88)

    @property
    def promotion(self):
        """The promotion type as `''` or one of %s.""" % Piece.promote_to
        return self._promotion
    
    def __str__(self):
        return str(self.source) + str(self.target) + self._promotion
    
    def __repr__(self):
        return "Move.from_uci(%s)" % repr(self.uci)

    def __eq(self, other):
        if other is None:
            return False
        return self._source_x88 == other._source_x88 \
            and self._target_x88 == other._target_x88 \
            and self._promotion == other._promotion 

    def __eq__(self, other):
        return self.__eq(other)

    def __ne__(self, other):
        return not self.__eq(other)
    
    def __hash__(self):
        # should be a perfect hash if our square number is under 128
        p = Piece.promote_to.index(self._promotion) + 1 if self._promotion else 0
        return self._source_x88 * 137 + self._target_x88 + p


    @classmethod
    def from_uci(cls, uci):
        """Creates a move object from an UCI move string.

        :param move: An UCI move string like "a1a2" or "b7b8q".
        """
        if len(uci) not in [4,5]:
            raise ValueError(uci)

        source = Square(uci[:2])
        target = Square(uci[2:4])
        promotion = uci[4:]

        return cls(source, target, promotion)

    @classmethod
    def from_x88(cls, source, target, promotion=''):
        if not cls._x88_moves:
            raise ValueError
        # try to use the cache
        if not promotion:
            return cls._x88_moves[(source, target)]
        return Move(Square.from_x88(source), Square.from_x88(target), promotion)

    @classmethod
    def get_all(cls):
        '''Yield all moves combinations that do not have promotion.'''
        #FIXME add in promotion
        
        for source in Square.get_all():
            for target in Square.get_all():
                if source != target:
                    move = cls(Square.from_x88(source.x88), Square.from_x88(target.x88))
                    yield(move)


for move in Move.get_all():
    Move._x88_moves[(move.source.x88, move.target.x88)] = move

