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

#include "ColoredPiece.h"
#include "AGChess_Exception.h"
#include <iostream>

namespace AGChess {

    ColoredPiece::ColoredPiece() {
        coloredPiece_ = 0;
    }
    
    ColoredPiece::ColoredPiece(Color::AGChessColorT color_, Piece::AGChessPieceT piece)
    {
        coloredPiece_ = piece;
        
        switch (color_) {
            case Color::WhiteColor:
                // piece_ = piece_;
                break;
            case Color::BlackColor:
                coloredPiece_ = coloredPiece_ | 8; // Black is 8
                std::cout << "Initializing with black" << std::endl;
                break;
            default:
                coloredPiece_ = NoColoredPiece;
                break;
        }
    }
    
    ColoredPiece::ColoredPiece(char piece) {
        switch (piece) {
            case 'K':  coloredPiece_ = WK; break;
            case 'Q':  coloredPiece_ = WQ; break;
            case 'R':  coloredPiece_ = WR; break;
            case 'B':  coloredPiece_ = WB; break;
            case 'N':  coloredPiece_ = WN; break;
            case 'P':  coloredPiece_ = WP; break;
            case 'k':  coloredPiece_ = BK; break;
            case 'q':  coloredPiece_ = BQ; break;
            case 'r':  coloredPiece_ = BR; break;
            case 'b':  coloredPiece_ = BB; break;
            case 'n':  coloredPiece_ = BN; break;
            case 'p':  coloredPiece_ = BP; break;
            default:
                coloredPiece_ = 0;
                break;
        }
    }
    
    /*
    ColoredPiece::ColoredPiece(AGColoredPieceType piece) {
        if ((piece == 7) || (piece == 8) || (piece > 14)) {
            coloredPiece_ = 0;
        } else {
            coloredPiece_ = piece;
        }
    }*/
    
    ColoredPiece::ColoredPiece(Color color, Piece piece) {
        if (piece.isPiece() && color.isValid()) {
            coloredPiece_ = piece.enumValue();            
            if (color == Black) {coloredPiece_ = coloredPiece_ | 8;}

        } else {
            coloredPiece_ = 0;
        }

    }
    
    bool ColoredPiece::isValid() const {
        return isPiece();
    }
    
    bool ColoredPiece::isPiece() const {
        switch (coloredPiece_ & ~8) {
            case Piece::KingPiece:   // fall through
            case Piece::QueenPiece:  // fall through
            case Piece::PawnPiece:   // fall through
            case Piece::BishopPiece: // fall through
            case Piece::KnightPiece: // fall through
            case Piece::RookPiece:   return true;
            default:                 return false;
        }
    }
    
    bool ColoredPiece::isSlider() const {
        return piece().isSlider();
    }
    
    Color ColoredPiece::color() const {
        if (!isPiece()) {
            return Color(Color::NoColor);
        }
        
        if ((coloredPiece_ & 8) == 0) {
            return Color(Color::WhiteColor);
        } else {
            return Color(Color::BlackColor);
        }
    }
    
    Piece ColoredPiece::piece() const {
        return Piece(toupper(char(*this)));
    }
    
    ColoredPiece::operator char() const {
        if (!isPiece()) { return '-'; }
    
        char c;
        switch (coloredPiece_ & ~8) {
            case Piece::KingPiece:   c = 'K'; break;
            case Piece::QueenPiece:  c = 'Q'; break;
            case Piece::PawnPiece:   c = 'P'; break;
            case Piece::BishopPiece: c = 'B'; break;
            case Piece::KnightPiece: c = 'N'; break;
            case Piece::RookPiece:   c = 'R'; break;
            default: throw AGChess_Exception("ColoredPiece::char() unexpected case in switch");
        }
        
        c = (color() == Color::WhiteColor ? c : tolower(c));
        return c;
    }
    
#pragma mark -
#pragma mark Comparison operators
    
    bool ColoredPiece::operator==(const ColoredPiece& rhs) const {
        return coloredPiece_ == rhs.coloredPiece_;
    }
    
    bool ColoredPiece::operator!=(const ColoredPiece& rhs) const {
        return coloredPiece_ != rhs.coloredPiece_;
    }
    
    bool ColoredPiece::operator==(const Color& rhs) const {
        return color() == rhs;
    }
    
    bool ColoredPiece::operator!=(const Color& rhs) const {
        return color() != rhs;
    }
    
    bool ColoredPiece::operator==(const Piece& rhs) const {
        return piece() == rhs;
    }
    bool ColoredPiece::operator!=(const Piece& rhs) const {
        return piece() != rhs;
    }
}