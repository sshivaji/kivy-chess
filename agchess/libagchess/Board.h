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

#ifndef AGCHESS_BASIC_BOARD_H
#define AGCHESS_BASIC_BOARD_H

#include "Square.h"
#include "ColoredPiece.h"
#include "Bitboard.h"
#include "StartPos.h"

namespace AGChess {
    
    /*!
     * @class Board
     * @abstract An object that contains information about the arrangement of
     * pieces on a chess board.
     * @discussion A basic_board object encapsulates data about the arrangement
     * of pieces on the chess board.  It contains no information about other 
     * aspects of a position, such as castling rights, or en passant.  One way of
     * thinking about a basic_board object is the information that an onlooker
     * might get by glancing at a chess board mid-game: it isn't necessarily clear 
     * whose move it is or if castling is legal.  A basic_board does not require
     * the arrangement of pieces be a legal arrangement.
     */
    class Board {
    public:
        Board(StartPosition = EmptyStartPosition);
        
        void clear(Square sq);
        void set(Square square, ColoredPiece piece);
        void move(Square from, Square to);
        ColoredPiece at(Square square) const;
        
        /* Bitboard methods */
        Bitboard occupied() const;
        Bitboard occupied(Color color) const;
        Bitboard empty() const;
        
        const Bitboard& bitboard(ColoredPiece piece) const;
        const Bitboard& bitboard(Square) const;
        Bitboard bitboard(Piece) const;
        
        bool operator==(const Board& rhs) const;
        
    private:
        
        Bitboard& piece_bitboard(ColoredPiece piece);
        Bitboard& piece_bitboard(Square);
        
        void set_standard_position();
        void set_empty_position();
        
        // State Bitboards	
        Bitboard pawnsBB_[2];	
        Bitboard knightsBB_[2];
        Bitboard bishopsBB_[2];
        Bitboard rooksBB_[2];
        Bitboard queensBB_[2];
        Bitboard kingsBB_[2];
        
        // Array for easy identification of a Square's occupancy
        ColoredPiece pieceForSquare_[64];
    };
    
    std::ostream& operator<<(std::ostream& out, const Board& board);
};



#endif