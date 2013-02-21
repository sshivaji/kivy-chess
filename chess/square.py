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

from x88 import X88

class Square(object):
    """Represents a square on the chess board.

    :param name: The name of the square in algebraic notation.

    Square objects that represent the same square compare as equal.

    >>> import chess
    >>> chess.Square("e4") == chess.Square("e4")
    True
    """

    ranks = '12345678'
    files = 'abcdefgh'
    ep_files = ranks[2] + ranks[5]
    _x88_squares = {}

    def __init__(self, label):

        if len(label) != 2:
            raise ValueError(square)

        try:
            x = self.files.index(label[0])
            y = self.ranks.index(label[1])
        except ValueError:
            raise ValueError(label)

        self._x88 = X88.from_x_and_y(x, y)

    @property
    def x(self):
        """The x-coordinate, starting with 0 for the a-file."""
        return X88.to_x(self._x88)

    @property
    def y(self):
        """The y-coordinate, starting with 0 for the first rank."""
        return X88.to_y(self._x88)
    
    @property
    def rank(self):
        """The rank as a character in %s""" % self.ranks
        return self.ranks[X88.to_y(self._x88)]

    @property
    def file(self):
        """The file as a character in %s""" % self.files
        return self.files[X88.to_x(self._x88)]

    @property
    def name(self):
        """The algebraic name of the square."""
        return str(self)

    @property
    def x88(self):
        """The `0x88 <http://en.wikipedia.org/wiki/Board_representation_(chess)#0x88_method>`_
        index of the square."""
        return self._x88

    @property
    def index(self):
        """An integer between 0 and %s where 0 represents Square('a1').""" % (
            len(self.ranks) * len(self.files) - 1)
        return X88.to_index(self._x88)

    def is_dark(self):
        """:return: Whether it is a dark square."""
        return self._x88 % 2 == 0

    def is_light(self):
        """:return: Whether it is a light square."""
        return self._x88 % 2 == 1
    
    def is_backrank(self):
        """:return: Whether the square is on either sides backrank."""
        return self.y in [0,len(self.ranks)-1]

    def __str__(self):
        return self.files[self.x] + self.ranks[self.y]

    def __repr__(self):
        return "Square('%s')" % str(self)

    def __eq__(self, other):
        return self._x88 == other._x88

    def __ne__(self, other):
        return self._x88 != other._x88

    def __hash__(self):
        return self._x88

    @classmethod
    def from_x88(cls, x88):
        """Creates a square object from an `x88 <http://en.wikipedia.org/wiki/Board_representation_(chess)#0x88_method>`_
        index.

        :param x88:
            The x88 index as an integer from 0 to 127.
        """
        if not cls._x88_squares:
            raise ValueError
        return cls._x88_squares[x88]

    @classmethod
    def from_rank_and_file(cls, rank, file):
        """Creates a square object from rank and file.

        :param rank:
            An integer between 1 and 8.
        :param file:
            The rank as a letter between `"a"` and `"h"`.
        """
        return Square(str(file) + str(rank))

    @classmethod
    def from_x_and_y(cls, x, y):
        """Creates a square object from x and y coordinates.

        :param x:
            An integer between 0 and 7 where 0 is the a-file.
        :param y:
            An integer between 0 and 7 where 0 is the first rank.
        """
        return Square(Square.files[x] + Square.ranks[y])

    @classmethod
    def get_all(cls):
        for r in cls.ranks:
            for f in cls.files:
                yield cls(f + r)
    
for square in Square.get_all():
    Square._x88_squares[square.x88] = square

if __name__ == '__main__':
    print Square("e4") == Square("e4")
