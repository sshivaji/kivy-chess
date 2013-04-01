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

#include "EditablePosition.h"

namespace AGChess {

    /* The following three methods are linked to eachother by the fact that
     * the ply count has to do with whose move it is, and the move number
     * is based on the ply count.  */
    
    inline void EditablePosition::setSideToMove(Color color) {
#warning validate_color(color);
        side_to_move_ = color;
    }
    
    void EditablePosition::setPly(unsigned short new_ply) {
        ply_ = new_ply;
    }
    
    void EditablePosition::set_move_number(unsigned short new_move_number) {
        unsigned char offset = (side_to_move_ == White ? 1 : 0);
        setPly(new_move_number * 2 - offset);  // The ply is twice the move number
        // Subtract 1 if side_to_move is White,
        // Otherwise, ply is just twice the move number
    }
    
    
    void EditablePosition::set_castling_right(Color color, CastlingSide side, bool flag) {
        Position::set_castling_right(color, side, flag);
    }
    
    void EditablePosition::reset() {
        for (int i = 0; i < 63; i++) {
            set(Square(i), NoColoredPiece);
        }
        setCastlingRights(NoCastling);
        setHalfmoveClock(0);
        set_move_number(0);
        setSideToMove(White);
        setEpSquare(InvalidSquare);
    }
    
    void EditablePosition::clear(Square s) {
        board_.clear(s); 
    }
    
    void EditablePosition::set(Square s, ColoredPiece p) {
        board_.set(s, p);
    }

    EditablePosition& EditablePosition::operator=(const Position& rhs) {
        setBoard(rhs.board());
        setCastlingRights(rhs.castlingRights());
        setEpSquare(rhs.epSquare());
        setSideToMove(rhs.sideToMove());
        setHalfmoveClock(rhs.halfmoveClock());
        setPly(rhs.ply());
        
        return *this;
    }
}