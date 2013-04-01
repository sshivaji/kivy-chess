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

#ifndef AGCHESS_COLORED_PIECE_T_H
#define AGCHESS_COLORED_PIECE_T_H

#include "Color.h"
#include "Piece.h"

namespace AGChess {
    
    class ColoredPiece {
    public:
        enum AGColoredPieceType {
            NoColoredPiece = 0, 
            WP = 1, WN = 2,  WB = 3,  WR = 4,  WQ = 5,  WK = 6,
            BP = 9, BN = 10, BB = 11, BR = 12, BQ = 13, BK = 14,
        };
        
        ColoredPiece();
        ColoredPiece(Color::AGChessColorT color, Piece::AGChessPieceT piece);
        ColoredPiece(Color color, Piece piece);
        ColoredPiece(char piece);
        //ColoredPiece(AGColoredPieceType piece);

        bool isValid() const;
        bool isPiece() const;
        bool isSlider() const;
        Color color() const;
        Piece  piece() const;
        
        operator char() const;
        
        bool operator==(const ColoredPiece& rhs) const;
        bool operator!=(const ColoredPiece& rhs) const;
        
        bool operator==(const Color& rhs) const;
        bool operator!=(const Color& rhs) const;
        
        bool operator==(const Piece& rhs) const;
        bool operator!=(const Piece& rhs) const;
        
    protected:
        unsigned char coloredPiece_;
    };

    const ColoredPiece WP = ColoredPiece('P');
    const ColoredPiece WN = ColoredPiece('N');
    const ColoredPiece WB = ColoredPiece('B');
    const ColoredPiece WR = ColoredPiece('R');
    const ColoredPiece WQ = ColoredPiece('Q');
    const ColoredPiece WK = ColoredPiece('K');
    const ColoredPiece BP = ColoredPiece('p');
    const ColoredPiece BN = ColoredPiece('n');
    const ColoredPiece BB = ColoredPiece('b');
    const ColoredPiece BR = ColoredPiece('r');
    const ColoredPiece BQ = ColoredPiece('q');
    const ColoredPiece BK = ColoredPiece('k');
    const ColoredPiece NoColoredPiece = ColoredPiece();
    
    
    /*
    const ColoredPiece WP = ColoredPiece(ColoredPiece::WP);
    const ColoredPiece WN = ColoredPiece(ColoredPiece::WN);
    const ColoredPiece WB = ColoredPiece(ColoredPiece::WB);
    const ColoredPiece WR = ColoredPiece(ColoredPiece::WR);
    const ColoredPiece WQ = ColoredPiece(ColoredPiece::WQ);
    const ColoredPiece WK = ColoredPiece(ColoredPiece::WK);
    const ColoredPiece BP = ColoredPiece(ColoredPiece::BP);
    const ColoredPiece BN = ColoredPiece(ColoredPiece::BN);
    const ColoredPiece BB = ColoredPiece(ColoredPiece::BB);
    const ColoredPiece BR = ColoredPiece(ColoredPiece::BR);
    const ColoredPiece BQ = ColoredPiece(ColoredPiece::BQ);
    const ColoredPiece BK = ColoredPiece(ColoredPiece::BK);
    const ColoredPiece NoColoredPiece = ColoredPiece(ColoredPiece::NoColoredPiece);
     */
}

#endif