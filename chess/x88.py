# -*- coding: utf-8 -*-
#
# This file is part of the python-chess library.
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

import piece

class X88(object):
    """Static class that encapsulates operations need for a little-endian 0x88 chess board.

    `http://chessprogramming.wikispaces.com/0x88`_
    """

    X88 = 0x88
    ATTACKER_DIFF = 119

    ATTACKS = [
            20, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 20, 0,
            0, 20, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 20, 0, 0,
            0, 0, 20, 0, 0, 0, 0, 24, 0, 0, 0, 0, 20, 0, 0, 0,
            0, 0, 0, 20, 0, 0, 0, 24, 0, 0, 0, 20, 0, 0, 0, 0,
            0, 0, 0, 0, 20, 0, 0, 24, 0, 0, 20, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 20, 2, 24, 2, 20, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 2, 53, 56, 53, 2, 0, 0, 0, 0, 0, 0,
            24, 24, 24, 24, 24, 24, 56, 0, 56, 24, 24, 24, 24, 24, 24, 0,
            0, 0, 0, 0, 0, 2, 53, 56, 53, 2, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 20, 2, 24, 2, 20, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 20, 0, 0, 24, 0, 0, 20, 0, 0, 0, 0, 0,
            0, 0, 0, 20, 0, 0, 0, 24, 0, 0, 0, 20, 0, 0, 0, 0,
            0, 0, 20, 0, 0, 0, 0, 24, 0, 0, 0, 0, 20, 0, 0, 0,
            0, 20, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 20, 0, 0,
            20, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 20
    ]

    RAYS = [
            17, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 15, 0,
            0, 17, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 15, 0, 0,
            0, 0, 17, 0, 0, 0, 0, 16, 0, 0, 0, 0, 15, 0, 0, 0,
            0, 0, 0, 17, 0, 0, 0, 16, 0, 0, 0, 15, 0, 0, 0, 0,
            0, 0, 0, 0, 17, 0, 0, 16, 0, 0, 15, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 17, 0, 16, 0, 15, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 17, 16, 15, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1, 0,
            0, 0, 0, 0, 0, 0, -15, -16, -17, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, -15, 0, -16, 0, -17, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, -15, 0, 0, -16, 0, 0, -17, 0, 0, 0, 0, 0,
            0, 0, 0, -15, 0, 0, 0, -16, 0, 0, 0, -17, 0, 0, 0, 0,
            0, 0, -15, 0, 0, 0, 0, -16, 0, 0, 0, 0, -17, 0, 0, 0,
            0, -15, 0, 0, 0, 0, 0, -16, 0, 0, 0, 0, 0, -17, 0, 0,
            -15, 0, 0, 0, 0, 0, 0, -16, 0, 0, 0, 0, 0, 0, -17
    ]

    SHIFTS = {
        piece.PAWN:   0,
        piece.KNIGHT: 1,
        piece.BISHOP: 2,
        piece.ROOK:   3,
        piece.QUEEN:  4,
        piece.KING:   5
    }

    # 1-for, 2-for, cap-right, cap-left
    PAWN_OFFSETS = { 
            piece.WHITE: [ 16,  32,  17,  15], 
            piece.BLACK: [-16, -32, -17, -15]
    }

    PIECE_OFFSETS = {
            piece.KNIGHT: [-18, -33, -31, -14, 18, 33, 31, 14],
            piece.BISHOP: [-17, -15, 17, 15],
            piece.ROOK:   [-16, 1, 16, -1],
            piece.QUEEN:  [-17, -16, -15, 1, 17, 16, 15, -1],
            piece.KING:   [-17, -16, -15, 1, 17, 16, 15, -1]
    }
    
    @staticmethod
    def from_x_and_y(x, y):
        """Return 0x88 number from a x and y coordinates in first quadrant geometry.

        `http://en.wikipedia.org/wiki/Quadrant_%28plane_geometry%29`_
        """
        return 16 * y + x

    #FIXME
    @staticmethod
    def from_index(idx):
        return
    
    @staticmethod
    def to_x(x88):
        """Return x coordinate in first quadrant geometry from 0x88 number.

        `http://en.wikipedia.org/wiki/Quadrant_%28plane_geometry%29`_
        """
        return x88 & 7

    @staticmethod
    def to_y(x88):
        """Return y coordinate in first quadrant geometry from 0x88 number.

        `http://en.wikipedia.org/wiki/Quadrant_%28plane_geometry%29`_
        """
        return x88 >> 4
    
    @staticmethod
    def to_index(x88):
        """Return an integer from 0 to 63 given a 0x88 number."""
        return x88 + (x88 & ~7)
    
    #FIXME: this should be renamed as backrank implies the own players backrank
    @classmethod
    def is_backrank(cls, x88, color):
        """Returns whether or not a square is on the opponent's back rank."""
        return color == piece.BLACK and cls.to_y(x88) == 0 \
            or color == piece.WHITE and cls.to_y(x88) == 7

    @classmethod
    def is_secondrank(cls, offset, color):
        """Returns whether or not a square is on the player's second rank."""
        return color == piece.BLACK and cls.to_y(offset) == 6 \
            or color == piece.WHITE and cls.to_y(offset) == 1
            
