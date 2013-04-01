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


#ifndef AGCHESS_SAN_H
#define AGCHESS_SAN_H

#include "StandardPosition.h"
#include "Square.h"
#include <string>

/* Methods for converting a move in a position to Standard Algebraic Notation
 * and vice versa. */

namespace AGChess {

    /* Converts a move to a string with the move's standard algebraic notation representation. */
    std::string moveToSan(const basic_move& move, const StandardPosition& position);
    
    /* Converts a string of standard algebraic notation to a basic_move */
    basic_move SanToBasicMove(const std::string& SAN, const StandardPosition& position);
    
    Move SanToMove(const std::string& SAN, const StandardPosition& position);
    
    /* The following methods are meant to be used exclusively by moveToSan and SanToMove. */
    namespace SAN {
        void normalizeSanString(std::string& san);
        void findAndRemove(char c, std::string& s);
        Piece promotionPieceFromSan(const std::string& san);
        Piece movingPieceFromSan(const std::string& san);
        Square destinationFromSan(const std::string& san);
        Square disambiguateSourceFromSan(const std::string& san, 
                                         const StandardPosition& position, 
                                         Piece movingPiece, 
                                         Square destination);
    };
};

#endif