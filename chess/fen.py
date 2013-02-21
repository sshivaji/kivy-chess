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

from piece import Piece, COLORS
from square import Square


class FenError(ValueError):
    """Thrown when a FEN string is invalid."""

class Fen(object):
    '''Manipulates, validates, and parses FEN strings.

    :param fen:
        Optional. The FEN of the position. Defaults to the standard
        chess start position of Fen.start.

    Forsyth–Edwards Notation (FEN)
    `http://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation`_
    '''

    start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    row_sep = '/'
    null = '-'
    empty_square = '.'

    def __init__(self, fen=start):
        
        self._pieces = [None] * 128
        self._to_move = None
        self._castle_rights = None
        self._ep = None
        self._fifty_move = None
        self._full_move = None

        self.text = fen

    @property
    def text(self):
        """The FEN string representing the position."""
        # Board setup.
        empty = 0
        fen = ""
        for y in range(7, -1, -1):
            for x in range(0, 8):
                square = Square.from_x_and_y(x, y)
                p = self._pieces[square._x88]
                # Add pieces.
                if not p:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += p

            # Boarder of the board.
            if empty > 0:
                fen += str(empty)
            # if were not the first iteration
            if not (x == 7 and y == 0):
                fen += "/"
            empty = 0

        return ' '.join([
            fen, 
            self.turn, 
            self.castle_rights, 
            str(self.ep_square), 
            str(self.fifty_move), 
            str(self.full_move)])

    @text.setter
    def text(self, fen):

        try:
            pieces, to_move, castle_rights, ep, fifty_move, full_move = fen.split(' ')
        except ValueError:
            raise FenError('FEN "%s"does not consist of 6 parts.' % fen)

        #pieces
        rows = pieces.split(self.row_sep)

        if len(rows) != 8:
            raise FenError('pieces does not have 8 rows in "%s"' % pieces)

        i = 0
        for row in reversed(rows):

            field_sum = 0
            previous_was_number = False

            for char in row:

                # if we are digit expand empty squares
                if char.isdigit():
                    if previous_was_number:
                        raise FenError('Fen has consective numbers in "%s"' % pieces)
                    previous_was_number = True
                    field_sum += int(char)
                    i += int(char)

                # elif we are piece then add the piece to the board
                elif char in Piece.pieces:
                    field_sum += 1
                    previous_was_number = False
                    self._pieces[i] = char
                    i += 1

                # else booboo
                else:
                    raise FenError('Character "%s" not in known pieces in "%s' %(char, pieces))

            # if we do not have 8 items for a row then booboo
            if field_sum != 8:
                raise FenError('Incorrect piece count for row "%s" in "%s"' % (row, pieces))
            i += 8

        # who has the move
        try:
            self._to_move = COLORS[to_move]
        except KeyError:
            raise FenError("Unkown color %s for fen %s" %(repr(to_move), repr(fen)))

        #castle
        if castle_rights == self.null:
            self._castle_rights = []
        else:
            for char in castle_rights:
                if char not in Piece.castleclass:
                    raise FenError('Unknown castleclass "%s" in %s' % (char, fen))
            self._castle_rights = list(castle_rights)

        if ep == self.null:
            self._ep = None
        else:
            # if e.p. square is not on the right rank
            if ep[1] not in Square.ep_files:
                raise FenError('Impossible en passant file "%s" in "%s"' % (ep[1], fen))
            self._ep = Square(ep).x88

        if not full_move.isdigit() or int(full_move) < 1:
            raise FenError('Invalid full move %s in %s' % (full_move, repr(fen)))

        if not fifty_move.isdigit() or int(fifty_move) < 0:
            raise FenError('Invalid fifty rule half move %s in %s' % (fifty_move, repr(fen)))

        self._fifty_move = int(fifty_move)
        self._full_move = int(full_move)

    @property
    def turn(self):
        '''Whose turn it is to move as the key of piece.COLORS.'''
        for key, value in COLORS.iteritems():
            if value == self._to_move:
                return key
        raise ValueError(self._to_move)

    @property
    def castle_rights(self):
        '''The string of characters representing the available castling.
        
        The available characters are defined in piece.castle_rights.
        Note: A castle right is a precondition for castling but not the
        only condition.
        '''
        return ''.join(self._castle_rights)

    @property
    def ep_square(self):
        '''The possible en passant square if available.

        http://en.wikipedia.org/wiki/En_passant
        '''

        if not self._ep:
            return self.null
        return Square.from_x88(self._ep)

    @property
    def fifty_move(self):
        '''The half-clock for the fifty move rule.
        
        Set to zero when the last move was a capture or pawn move, otherwise
        it is incremented.

        Note: For the fifty move rule to be enabled a **each** player must 
        make 50 (half) moves. For a draw request to be granted the half-move
        clock must have reached 100 half moves.

        `http://en.wikipedia.org/wiki/Fifty-move_rule`_

         
        '''
        return self._fifty_move

    @property
    def full_move(self):
        '''The full move number from a FEN.'''
        return self._full_move

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Fen(%s)" % repr(self.text)

    def __eq__(self, other):
        return self.text == other.text

    def __ne__(self, other):
        return self.text != other.text

    def __hash__(self):
        return hash(self.text)

    #FIXME __iter__ should return 8th rank first
    def __iter__(self):
        for key in Square._x88_squares.keys():
            yield self._pieces[key]

    def __get_key(self, square):
        #XXX removing direct access by x88 -- too many ways to skin a cat.
        # If its not a square type object
        # then should be a string label.
        if not hasattr(square, 'x88'):
            try:
                square = Square(square)
            except (TypeError, ValueError):
                raise ValueError(square)
        return square.x88

    def __getitem__(self, square):
        x88 = self.__get_key(square)
        return self._pieces[x88]

    def __setitem__(self, square, piece):
        x88 = self.__get_key(square)
        # Make sure piece is valid
        check = Piece.enum(str(piece))
        self._pieces[x88] = str(piece)

    def __delitem__(self, square):
        #XXX does anyone ever use del to delete objects in a container?
        x88 = self.__get_key(square)
        self._pieces[x88] = None

if __name__ == '__main__':
    
    start = 'rnbqkbnr/ppppppp1/7p/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    f = Fen()


    '''
    print f['a1']
    print f[Square('a1')]
    #print f[0]
    #print f['z1']
    f['a1'] = 'P'
    print f['a1']
    del f['a1'] 
    print f['a1']
    #f['a1'] = 1
    print f
    print repr(f)
    print f.text
    print f.turn
    print f.castle_rights
    print f.ep_square
    print f.fifty_move
    print f.full_move
    print f.to_boardstring()
    '''

