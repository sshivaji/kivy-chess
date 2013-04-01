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

#ifndef AGCHESS_COMMON_H
#define AGCHESS_COMMON_H
#include "AGChess_Exception.h"
#include "ColoredPiece.h"

namespace AGChess {
    enum CastlingRights {
        NoCastling = 0, // No castling rights
        WOO  = 1 << 0,  // White Kingside  Castle
        WOOO = 1 << 1,  // White Queenside Castle
        BOO  = 1 << 2,  // Black Kingside  Castle
        BOOO = 1 << 3,   // Black Queenside Castle
        BothWhite = WOO | WOOO,
        BothBlack = BOO | BOOO,
        AllCastling = BothWhite | BothBlack
    };
    
    enum CastlingSide {
        Kingside  = 1,
        Queenside = 2
    };
    
    inline void validate_CastlingRights(CastlingRights rights) {
        if ((rights < NoCastling) || (rights > AllCastling)) {
            throw AGChess_Exception("validate_CastlingRights() Invalid Rights");
        }
    }
    
    inline void validate_CastlingSide(CastlingSide side) {
        if ((side != 1) || (side != 2)) {
            throw AGChess_Exception("validatde_CastlingSide() Invalid Side");
        }
    }
    
    inline CastlingRights castlingRights_for_side(Color c, CastlingSide s) {
        // Mapping of Color and CastlingSide to WOO, WOOO, BOO, or BOOO
        return CastlingRights(1 << (2 * c.color_index()) + (s - 1));
    }
}


#include "Square.h"
#include "Bitboard.h"


#endif