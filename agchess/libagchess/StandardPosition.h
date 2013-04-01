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


#ifndef AGCHESS_STANDARD_POSITION_H
#define AGCHESS_STANDARD_POSITION_H

#include "SimplePosition.h"

namespace AGChess {
    
    /* The Standard_Position class has a very minimal interface.  It is meant as
     * an interface to make and unmake (undo) moves.   */
    
    class StandardPosition : public SimplePosition {
    public:
        void make(basic_move& move);
        void unmake(const basic_move& move);
        void promote(Piece p);
        StandardPosition& copy(const Position& position);
        
    protected:
        
        Bitboard sliding_attacks(Piece p, Square s) const;
        Bitboard sliding_attacks(ColoredPiece p, Square s) const {return sliding_attacks(p.piece(), s);}
        
        bool isCastle(const basic_move& move) const;        
        bool isEnPassantCapture(const basic_move& move) const;        
        bool isPseudoLegal(basic_move& move);
        bool isDoubleJump(basic_move& move);
        bool isPromotion(basic_move& move);
        Bitboard pseudoLegalMoves(Square s) const;
        Bitboard pseudoLegalCastle(Color c) const;
        
        bool inCheck(Color c) const;
        
        /* make helper methods */
        void makeSaveState(basic_move& move);
        void makePawnMove(basic_move& move);
        void makeKingMove(basic_move& move);
        void makeRookMove(basic_move& move);
        void makeCastle(basic_move& move);
        
        /* unmake helper methods */
        void unmakeSaveState(const basic_move& move);
        void unmakeCastle(const basic_move& move);
        
        void makeNullMove(basic_move& move);
    };
    
    bool isLegalStandardPosition(const Position& position);
    bool inCheck(const Position& position, Color c);
}

#endif