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

import copy

from piece import Piece,  \
        COLORS, BLACK, WHITE, \
        PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
from x88 import X88
from square import Square
from move import Move, MoveError
from fen import Fen
from notation import SanNotation
from zobrist_hasher import ZobristHasher



class Position(object):

    """Represents a chess position.

    :param fen:
        Optional. The FEN of the position. Defaults to the standard
        chess start position.

    Squares can be accessed via their name, a square object and their
    x88 index:

    >>> import chess
    >>> pos = chess.Position()
    >>> pos["e4"] = Piece("Q")
    >>> pos[chess.Square("e4")]
    Piece('Q')
    >>> del pos["a8"]
    >>> pos[0] # 0 is the x88 index of a8.
    None

    """

    def __init__(self, fen=Fen.start):
        
        self.fen = Fen(fen)
        self._pieces = self.fen._pieces

    def copy(self):
        """Gets a copy of the position. The copy will not change when the
        original instance is changed.

        :return:
            An exact copy of the positon.
        """
        return copy.deepcopy(self)
    
    def get_pseudo_legal_moves(self, source=None):
        """:yield: Pseudo legal moves in the current position.
         
        :param source: The source square to limit moves or None for
            all possible moves.
        """

        tomove = self.fen._to_move

        for x88 in [ x88 for x88 in Square._x88_squares.keys() 
            if self._pieces[x88] 
            and Piece.color(self._pieces[x88]) == tomove
            and (source is None or x88 == source._x88)]:

            piece = self._pieces[x88]
            klass = Piece.klass(piece)

            # pawn moves
            if klass == PAWN:
                single, double, capleft, capright = X88.PAWN_OFFSETS[tomove]

                # Single square ahead. Do not capture.
                offset = x88 + single
                if not self._pieces[offset]:
                    # Promotion.
                    if X88.is_backrank(offset, tomove):
                        for promote_to in Piece.promote_to:
                            yield Move.from_x88(x88, offset, promote_to)
                    else:
                        yield Move.from_x88(x88, offset)

                    # Two squares ahead. Do not capture.
                    if X88.is_secondrank(x88, tomove):
                        offset = x88 + double
                        if not self._pieces[offset]:
                            yield Move.from_x88(x88, offset)

                # Pawn captures.
                for cap in [capleft, capright]:
                    offset = x88 + cap
                    if offset & X88.X88:
                        continue
                    target = self._pieces[offset]
                    if target and Piece.color(target) != tomove:
                       # Promotion.
                        if X88.is_backrank(offset, tomove):
                            for promote_to in Piece.promote_to:
                                yield Move.from_x88(x88, offset, promote_to)
                        else:
                            yield Move.from_x88(x88, offset)
                   # En-passant.
                    elif not target and offset == self.fen._ep:
                        yield Move.from_x88(target, self.fen._ep)
            
            #piece moves
            else:
                # for each a direction a piece moves in
                for offset in X88.PIECE_OFFSETS[Piece.klass(piece)]:

                    t_x88 = x88 + offset

                    # while we do not fall off the board
                    while not t_x88 & 0x88:
                        
                        # if there was not piece to attack then yield a quiet move
                        if not self._pieces[t_x88]:
                            yield Move.from_x88(x88, t_x88)
                            # do not break out

                        # else there is a piece there
                        else:
                            # if we can attack generate a move
                            if Piece.color(self._pieces[t_x88]) != tomove:
                                yield Move.from_x88(x88, t_x88)
                            # we hit something so break out
                            break

                        # Knight and king do not go multiple times in their direction.
                        if klass in [KNIGHT, KING]:
                            break

                        # travel down the board in the direction
                        t_x88 += offset


        # castling moves
        opponent = Piece.opposite_color(tomove)
        ok = True

        # get possible castling for the side to move
        for castle in [c for c in self.fen._castle_rights if Piece.color(c) == tomove]:

            (square, enum), _ = Piece.castle_squares[castle]
            king = Square(square)

            if Piece.klass(castle) == KING:
                direc = 1
            else:
                direc = -1

            # for offset in the squares the king will travel
            for offset in range(0, 3):
                s = Square.from_x88(king._x88 + (offset * direc))

                # if we are not the king square and we are occuppied
                if offset and self._pieces[s._x88]:
                    ok = False
                    break
                    
                # if we are trying to travel through check
                if self.is_attacked(opponent, s):
                    ok = False
                    break

            # kludge: we have to check occupancy for one more square on the queen side
            if direc == -1 and self._pieces[s._x88 - 1]:
                    ok = False
            if ok:
                yield Move(king, s)

    def is_attacked(self, color, square):
        """Checks whether a square is attacked.

        :param color:
            Check if this player is attacking.
        :param square:
            The square the player might be attacking.

        :return:
            A boolean indicating whether the given square is attacked
            by the player of the given color.
        """
        try:
            self.get_attackers(color, square).next()
            return True
        except StopIteration:
            return False

    def get_attackers(self, color, square):
        """Gets the attackers of a specific square.

        :param color:
            Filter attackers by this piece color.
        :param square:
            The square to check for.

        :yield:
            Source squares of the attack.
        """
        if not color in [BLACK, WHITE]:
            raise KeyError("Invalid color: %s." % repr(color))


        for x88, source in Square._x88_squares.iteritems():

            piece = self._pieces[x88]
            if not piece or Piece.color(piece) != color:
                continue

            difference = x88 - square._x88
            index = difference + X88.ATTACKER_DIFF
            klass = Piece.klass(piece)

            if X88.ATTACKS[index] & (1 << X88.SHIFTS[klass]):
                # Handle pawns.
                if klass == PAWN:
                    if difference > 0:
                        if Piece.color(piece) == WHITE:
                            yield source
                    else:
                        if Piece.color(piece) == BLACK:
                            yield source
                    continue

                # Handle knights and king.
                if klass in [KNIGHT, KING]:
                    yield source

                # Handle the others.
                offset = X88.RAYS[index]
                j = source._x88 + offset
                blocked = False
                while j != square._x88:
                    if self._pieces[j]:
                        blocked = True
                        break
                    j += offset
                if not blocked:
                    yield source
                

    def make_move(self, move, validate=True):
        """Makes a move.

        :param move:
            The move to make.
        :param validate:
            Defaults to `True`. Whether the move should be validated.

        :return:
            Making a move changes the position object. The same
            (changed) object is returned for chainability.

        :raise MoveError:
            If the validate parameter is `True` and the move is not
            legal in the position.
        """

        #if validate:
        if validate:
            if move not in self.get_legal_moves(source=move.source):
                raise MoveError(
                    "%s is not a legal move in the position %s." % (move, self.fen))

        piece = self._pieces[move._source_x88]
        capture = self._pieces[move._target_x88]
        target = move.target
        source = move.source

        # Move the piece.
        self._pieces[move._target_x88] = piece
        self._pieces[move._source_x88] = None

        # It is the next players turn.
        ocolor = Piece.opposite_color(self.fen._to_move)
        self.fen._to_move = ocolor

        # Pawn moves.
        self._ep = None
        if Piece.klass(piece) == PAWN:

            # En-passant.
            if target.x != source.x and not capture:
                offset = 16 if self.fen._to_move == WHITE else -16
                self._pieces[target.x88() + offset] = None
                capture = True

            # If big pawn move, set the en-passant file.
            if abs(target.y - source.y) == 2:
                if self.get_theoretical_ep_right(target.x):
                    self._ep = move.target

        # Promotion.
        if move.promotion:
            self._pieces[move.target._x88] = move.promotion

        # Potential castling.
        if Piece.klass(piece) == KING:
            steps = move.target.x - move.source.x
            if abs(steps) == 2:
                # Queen-side castling.
                if steps == -2:
                    rook_target = move.target.x88 + 1
                    rook_source = move.target.x88 - 2
                # King-side castling.
                else:
                    rook_target = move.target.x88 - 1
                    rook_source = move.target.x88 + 1
                self._pieces[rook_target] = self._pieces[rook_source]
                self._pieces[rook_source] = None

        # Update castling rights.
        for klass in self.fen._castle_rights:
            if not self.get_theoretical_castling_right(klass):
                self.fen._castle_rights.remove(klass)
                # XXX Castling rights can only be removed 
                #self.set_castling_right(klass, False)


        # Increment the 50 move half move counter.
        if Piece.klass(piece) == PAWN or capture:
            self.fen._fifty_move = 0
        else:
            self.fen._fifty_move += 1

        # Increment the move number.
        if self.fen._to_move == WHITE:
            self.fen._full_move += 1
        
        return self

    def get_legal_moves(self, source=None):
        """:yield: All legal moves in the current position."""

        for move in self.get_pseudo_legal_moves(source=source):
            potential_position = self.copy()
            potential_position.make_move(move, False)
            if not potential_position.is_king_attacked(self.fen._to_move):
                yield move

    def is_king_attacked(self, color):
        """:return: Whether the king of the given color is attacked.

        :param color: `"w"` or `"b"`.
        """
        square = self.get_king(color)
        if square:
            return self.is_attacked(Piece.opposite_color(color), square)
        # XXX No king?
        else:
            return False

    def get_king(self, color):
        """Gets the square of the king.

        :param color:
            `"w"` for the white players king. `"b"` for the black
            players king.

        :return:
            The first square with a matching king or `None` if that
            player has no king.
        """
        #if not color in ["w", "b"]:
        #   raise KeyError("Invalid color: %s." % repr(color))

        for square, piece in [(s, self._pieces[s._x88]) for s in Square.get_all() if self._pieces[s._x88]]:
            if Piece.is_klass_and_color(piece, KING, color):
                return square

    def get_theoretical_ep_right(self, x):
        """Checks if a player could have an ep-move in theory from
        looking just at the piece positions.

        :param file:
            The file to check as a letter between `"a"` and `"h"`.

        :return:
            A boolean indicating whether the player could theoretically
            have that en-passant move.

        """
        if x < 0 or x > 7:
            raise ValueError(x)

        '''
        3 states of en-passant
        p.  pP  ..
        ..  ..  .p
        .P  ..  ..
        '''

        # Check there is a pawn on the right rank for e.p.
        y = 3 if self.fen._to_move == WHITE else 4
        x88 = X88.from_x_and_y(x, y) 

        piece = self._pieces[x88]
        if not piece:
            return False

        # If the square is not an opposite colored pawn then its not possible.
        ocolor = Piece.opposite_color(self.fen._to_move)
        if not Piece.is_klass_and_color(piece, PAWN, ocolor):
            return False

        # If the square below the pawn is not empty then it not possible.
        y = 2 if self.turn == WHITE else 5
        x88 = X88.from_x_and_y(x, y) 
        if self[x88]:
            return False

        # If there is not pawn of opposite color on a neighboring file then its not possible.
        xs = [_x for _x in range(8) if _x>=0 and  _x<8 and abs(x-_x) == 1]
        for _x in xs:
            x88 = X88.from_x_and_y(_x, y) 
            piece = self._pieces[x88] 
            if Piece.is_klass_color(piece, PAWN, Piece.opposite_color(self.fen._to_move)):
                return True
        # Else its just not possible.
        return False

    def get_theoretical_castling_right(self, klass):
        """Checks if a player could have a castling right in theory from
        looking just at the piece positions.

        :param klass:
            The type of castling move to check. See
            `Position.get_castling_right(type)` for values.

        :return:
            A boolean indicating whether the player could theoretically
            have that castling right.
        """
        if klass not in Piece.castleclass:
            raise KeyError(klass)

        # TODO: Support Chess960.

        for square, enum in Piece.castle_squares[klass]:
            piece = self._pieces[Square(square)._x88]
            if not piece or Piece.enum(piece) != enum:
                return False
        return True

    def is_check(self):
        """:return: Whether the current player is in check."""
        return self.is_king_attacked(self.fen._to_move)

    def is_checkmate(self):
        """:return: Whether the current player has been checkmated."""
        if not self.is_check():
            return False
        else:
            try:
                self.get_legal_moves().next()
                return False
            except StopIteration:
                return True

    def is_stalemate(self):
        """:return: Whether the current player is in stalemate."""
        if self.is_check():
            return False
        else:
            try:
                self.get_legal_moves().next()
                return False
            except StopIteration:
                return True

    def get_piece_counts(self, colors=[WHITE, BLACK]):
        """Counts the pieces on the board.

        :param color:
            list of colors to check. Defualts to black and white

        :return:
            A dictionary of piece counts, keyed by lowercase piece type
            letters.
        """
        #if not color in ["w", "b", "wb", "bw"]:
        #   raise KeyError(
        #       "Expected color filter to be one of 'w', 'b', 'wb', 'bw', "
        #       "got: %s." % repr(color))

        counts = {
            PAWN:   0,
            BISHOP: 0,
            KNIGHT: 0,
            ROOK:   0,
            KING:   0,
            QUEEN:  0,
        }
        for piece in self._pieces:
            if piece and Piece.color(piece) in colors:
                counts[Piece.klass(piece)] += 1
        return counts

    def is_insufficient_material(self):
        """Checks if there is sufficient material to mate.

        Mating is impossible in:

        * A king versus king endgame.
        * A king with bishop versus king endgame.
        * A king with knight versus king endgame.
        * A king with bishop versus king with bishop endgame, where both
          bishops are on the same color. Same goes for additional
          bishops on the same color.

        Assumes that the position is valid and each player has exactly
        one king.

        :return:
            Whether there is insufficient material to mate.
        """
        piece_counts = self.get_piece_counts()

        # King versus king.
        if sum(piece_counts.values()) == 2:
            return True

        # King and knight or bishop versus king.
        elif sum(piece_counts.values()) == 3:
            if piece_counts["b"] == 1 or piece_counts["n"] == 1:
                return True

        # Each player with only king and any number of bishops, 
        # where all bishops are on the same color.
        elif sum(piece_counts.values()) == 2 + piece_counts[BISHOP]:
            white_has_bishop = self.get_piece_counts([WHITE])[BISHOP] != 0
            black_has_bishop = self.get_piece_counts([BLACK])[BISHOP] != 0
            if white_has_bishop and black_has_bishop:
                color = None
                for square in Square.get_all():
                    p = self._pieces[square._x88]
                    if p and Piece.klass(p) == BISHOP:
                        if color and color != square.is_light():
                            return False
                        color = square.is_light()
                return True
        return False

    def is_game_over(self):
        """Checks if the game is over.

        :return:
            Whether the game is over by the rules of chess,
            disregarding that players can agree on a draw, claim a draw
            or resign.
        """
        return (self.is_checkmate() or self.is_stalemate() or
                self.is_insufficient_material())

    def __str__(self):
        return str(self.fen)

    def __repr__(self):
        return "Position(%s)" % repr(str(self.fen))

    def __eq__(self, other):
        return self.fen == other.fen

    def __ne__(self, other):
        return self.fen != other.fen

    def __hash__(self):
        hasher = ZobristHasher(ZobristHasher.POLYGLOT_RANDOM_ARRAY)
        return hasher.hash_position(self)

    def __getitem__(self, square):
        return self.fen.__getitem__(square)

    def __setitem__(self, square, piece):
        self.fen.__setitem__(square, piece)

    def __delitem__(self, square):
        self.fen.__delitem__(square)

    #TODO
    def clear_board(self): pass
    def reset(self): pass

    # do we want this public?
    def toggle_turn(self): """Toggles whos turn it is."""


if __name__ == '__main__':
    from notation import SanNotation
    
    f = Position()
#    print 11, f['a1']
#    print 11, f[Square('a1')]
    m = Move.from_uci('b1c3')
    print SanNotation(f, m)
    f.make_move(m)
    print f

    f.make_move(Move.from_uci('c7c5'))
    print f

    print f["a7"]
#
#    for move in f.get_legal_moves():
#        move
#    print f.is_check()
#    print f.is_checkmate()
#    print f.is_stalemate()
#    print f.is_game_over()
#
#    print f.fen
#    print f.fen.turn
#    print f.fen.castle_rights
#    print f.fen.ep_square
#    print f.fen.fifty_move
#    print f.fen.full_move
#
#    print dir(f)
#
    

