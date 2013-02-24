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

import re

from piece import Piece, PAWN, KING, WHITE
from move import Move, MoveError
from square import Square


class AbstractNotation(object):

    def __init__(self, position, move):

        resulting_position = position.copy().make_move(move)
        captured = position._pieces[move.target._x88]
        piece = position._pieces[move.source._x88]
        ocolor = Piece.opposite_color(position.fen._to_move)

        # Pawn moves.
        enpassant = False
        if Piece.klass(piece) == PAWN:
            # En-passant.
            if move.target.file != move.source.file and not captured:
                enpassant = True
                captured = Piece.from_klass_and_color(PAWN, ocolor)

        # Castling.
        # TODO: Support Chess960.
        # TODO: Validate the castling move.
        if Piece.klass(piece) == KING:
            self.is_king_side_castle = move.target.x - move.source.x == 2
            self.is_queen_side_castle = move.target.x - move.source.x == -2
        else:
            self.is_king_side_castle = self.is_queen_side_castle = False

        # Checks.
        self.is_check = resulting_position.is_check()
        self.is_checkmate = resulting_position.is_checkmate()

        self.move = move
        self.piece = piece
        self.captured = captured
        self.is_enpassant = enpassant

        self._set_text(position)

    @property
    def text(self):
        return self._text

    def __str__(self):
        return self._text

    def __eq__(self, other):
        return self._text == other._text

    def __ne__(self, other):
        return self._text != other._text

    def __hash__(self):
        return hash(self._text)

    def _set_text(self, position):
        raise NotImplementedError()

    @classmethod
    def to_move(cls, position, notation):
        raise NotImplementedError()


class SanNotation(AbstractNotation):

    #FIXME remove hard coded symbols
    san_regex = re.compile('^([NBKRQ])?([a-h])?([1-8])?x?([a-h][1-8])(=[NBRQ])?(\+|#)?$')

    def _set_text(self, position):

        move = self.move

        piece_klass = Piece.klass(self.piece)

        # Generate the SAN.
        san = ""
        if self.is_king_side_castle:
            san += "O-O"
        elif self.is_queen_side_castle:
            san += "O-O-O"
        else:
            if piece_klass != PAWN:
                san += Piece.from_klass_and_color(piece_klass, WHITE)

            if position:
                san += self._get_disambiguator(move, position)

            if self.captured:
                if piece_klass == PAWN:
                    san += move.source.file
                san += "x"
            san += move.target.name

            if move.promotion:
                san += "="
                san += move.promotion.upper()

        if self.is_checkmate:
            san += "#"
        elif self.is_check:
            san += "+"

        if self.is_enpassant:
            san += " (e.p.)"

        self._text = san

    #FIXME legal moves could be passed into game_move
    def _get_disambiguator(self, move, position):

        same_rank = False
        same_file = False
        piece = position[move.source]

        for m in position.get_legal_moves():
            ambig_piece = position[m.source]
            if (piece == ambig_piece and move.source != m.source and
                move.target == m.target):
                if move.source.rank == m.source.rank:
                    same_rank = True

                if move.source.file == m.source.file:
                    same_file = True

                if same_rank and same_file:
                    break

        if same_rank and same_file:
            return move.source.name
        elif same_file:
            return str(move.source.rank)
        elif same_rank:
            return move.source.file
        else:
            return ""

    @classmethod
    def to_move(cls, position, san):
        
        san = str(san)

        # Castling moves.
        if san == "O-O" or san == "O-O-O":
            # TODO: Support Chess960, check the castling moves are valid.
            rank = 1 if position.fen.turn == "w" else 8
            if san == "O-O":
                return Move(
                    source=Square.from_rank_and_file(rank, 'e'),
                    target=Square.from_rank_and_file(rank, 'g'))
            else:
                return Move(
                    source=Square.from_rank_and_file(rank, 'e'),
                    target=Square.from_rank_and_file(rank, 'c'))
        # Regular moves.
        else:
            matches = cls.san_regex.match(san)
            if not matches:
                raise ValueError("Invalid SAN: %s." % repr(san))

            if matches.group(1):
                klass = Piece.klass(matches.group(1).lower())
            else:
                klass = PAWN
            piece = Piece.from_klass_and_color(klass, position.fen._to_move)
            target = Square(matches.group(4))

            source = None
            for m in position.get_legal_moves():
                if position._pieces[m.source._x88] != piece or m.target != target:
                    continue

                if matches.group(2) and matches.group(2) != m.source.file:
                    continue
                if matches.group(3) and matches.group(3) != str(m.source.rank):
                    continue

                # Move matches. Assert it is not ambiguous.
                if source:
                    raise MoveError(
                        "Move is ambiguous: %s matches %s and %s."
                            % san, source, m)
                source = m.source

            if not source:
                raise MoveError("No legal move matches %s." % san)

            return Move(source, target, matches.group(5) or None)

if __name__ == '__main__':

    from position import Position
    from move import Move 

    p = Position()
    m = Move.from_uci('b1c3')
    san = SanNotation(p, m)
    print san
    print SanNotation.to_move(p, san)
    

