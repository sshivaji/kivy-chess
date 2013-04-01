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


#ifndef AGCHESS_EDITABLEPOSITION_H
#define AGCHESS_EDITABLEPOSITION_H

#include "Position.h"
#include "StandardPosition.h"

namespace AGChess {

class EditablePosition : public Position {
        
public:
    void setBoard(const Board& b) { board_ = b;}
    void setCastlingRights(CastlingRights rights) { castle_rights_ = rights;}
    void set_castling_right(Color, CastlingSide, bool);
    void setEpSquare(Square ep) { ep_square_ = ep;}
    void setSideToMove(Color color);
    void setHalfmoveClock(unsigned short halfmove) {halfmove_clock_ = halfmove;}
    
    void reset();
    void clear(Square s);
    void set(Square s, ColoredPiece p);

    
    EditablePosition& operator=(const Position& rhs);
    
    // Ply and move-counter
    void setPly(unsigned short new_ply);
    void set_move_number(unsigned short new_move_number);

};    
    
}

#endif