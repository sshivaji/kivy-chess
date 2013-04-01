/*
 libagchess, a chess library in C++.
 Copyright (C) 2010-2011 Austen Green.
 
 libagchess is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 libagchess is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with libagchess.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef AGCHESS_BASIC_BOARD_MOVEGEN_H
#define AGCHESS_BASIC_BOARD_MOVEGEN_H

#include "Board.h"

namespace AGChess {
  
    Bitboard sliding_attacks(const Board& board, Square square);
    Bitboard pawn_attacks(const Board& board, Color color);
    Bitboard pawn_pushes(const Board& board, Color color);
    Bitboard attacks(const Board& board, Square square);
    Bitboard attacks_to(const Board& board, Square square);
    
    bool squareAttackedByColor(const Board& board, Square square, Color color);
    
    Square kingSquare(const Board& board, Color color);
    int coloredPieceCount(const Board& board, ColoredPiece piece);
    int colorCount(const Board& board, Color ccolor);
    int pieceCount(const Board& board, Piece piece);
    
    Bitboard pseudo_legal_moves_from(const Board& board, Square s);
    
    /* Returns a bitboard with each piece of Color c that is pinned to it's 
     * own king */
    Bitboard absolute_pins(const Board& board, Color color);
};

#endif