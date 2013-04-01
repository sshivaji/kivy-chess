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


#include "Position.h"

namespace AGChess {
    /* Returns true if the color has the right to castle in the direction indicated
     * by side */
    bool Position::hasCastlingRight(Color c, CastlingSide side) const {
        return castlingRights() & castlingRights_for_side(c, side);
    }
    
    /* Sets an individual castling right for a Color and CastlingSide.  This is probably
     * not a very efficient implementation */
    void Position::set_castling_right(Color c, CastlingSide side, bool flag) {
        CastlingRights r = castlingRights_for_side(c, side);
        
        if (flag) { castle_rights_ = CastlingRights(castle_rights_ | r) ; } 
        else { castle_rights_ = CastlingRights(castle_rights_ & ~r); }
    }    
    
    std::ostream& operator<<(std::ostream& out, const Position& position) {
        out << "En passant square: " << position.epSquare() << std::endl;
        out << "Side to move: " << (position.sideToMove() == White ? "White" : "Black") << std::endl;
        out << position.board() << std::endl;
        return out;
    }
    
    bool operator==(const Position& lhs, const Position& rhs) {
        return (lhs.castlingRights() == rhs.castlingRights()) &&
        (lhs.epSquare()       == rhs.epSquare()) &&
        (lhs.sideToMove()     == rhs.sideToMove()) &&
        (lhs.board()          == rhs.board());
    }
    
    bool operator!=(const Position& lhs, const Position& rhs) {
        return !(lhs==rhs);
    }
}

