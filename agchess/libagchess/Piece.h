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


#ifndef AGCHESS_PIECE_T_H
#define AGCHESS_PIECE_T_H

#include <string>
#include <ostream>

namespace AGChess {
    
    class Piece {
    public:
        enum AGChessPieceT {
            NoPiece = 0, PawnPiece = 1, KnightPiece = 2, BishopPiece = 3,
            RookPiece = 4, QueenPiece = 5, KingPiece = 6
        };
        
        Piece();
        //Piece(AGChessPieceT piece);
        Piece(char piece);
        
        bool operator==(const Piece& rhs) const;
        bool operator!=(const Piece& rhs) const;
        
        bool isSlider() const;
        bool isPiece() const;
        
        unsigned char enumValue() const;
        
        operator char() const;
        operator std::string() const;
        
    protected:
        unsigned char piece_;
    };
    
    std::ostream& operator<<(std::ostream& out, const Piece& piece);
    bool operator==(const Piece& lhs, char rhs);
    bool operator!=(const Piece& lhs, char rhs);
    
    const Piece None    = Piece();
    const Piece Pawn    = Piece('P');
    const Piece Knight  = Piece('N');
    const Piece Bishop  = Piece('B');
    const Piece Rook    = Piece('R');
    const Piece Queen   = Piece('Q');
    const Piece King    = Piece('K');
    
    /*
    const Piece None    = Piece(Piece::NoPiece);
    const Piece Pawn    = Piece(Piece::PawnPiece);
    const Piece Knight  = Piece(Piece::KnightPiece);
    const Piece Bishop  = Piece(Piece::BishopPiece);
    const Piece Rook    = Piece(Piece::RookPiece);
    const Piece Queen   = Piece(Piece::QueenPiece);
    const Piece King    = Piece(Piece::KingPiece);
     */
}

#endif