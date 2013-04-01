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

#ifndef AGCHESS_POSITION_H
#define AGCHESS_POSITION_H

#include "Board.h"
#include "AGChess_Common.h"
#include "Move.h"


namespace AGChess {
    
    /*!
     * @abstract Position is an abstract base class for a positional representation.
     * @discussion In general a Position has a basic_board for keeping track of the
     * location of pieces and keeps track of state-dependent variables:
     * castling rights, en-passant square, side to move, and halfmove clock.
     * A position knows the rules of chess such that it recognizes when a pawn move
     * creates an en-passant square, when moving a king/rook revokes a castling right, 
     * when moving a king two squares with a castling right results in castling,
     * how capturing or moving a pawn resets the halfmove clock, and that each move
     * results in switching the side to move.
     * 
     * If a pawn is moved to the last rank but isn't promoted immediately, the Position
     * goes into a waiting state - if the unpromoted pawn is not resolved before the
     * next move is made an exception will be thrown.
     */
    
    class Position {
        
    public:
        Position() : board_(StandardStartPosition) {
            ply_ = 1;
            castle_rights_ = CastlingRights(WOO|WOOO|BOO|BOOO);
        };
        
        // Accessors
        // Mutators are only allowed in an edit_position
        ColoredPiece at(Square s) const {return board_.at(s); }
        
        virtual const Board& board() const {return board_;} 
        virtual CastlingRights castlingRights() const {return castle_rights_;}
        virtual bool hasCastlingRight(Color, CastlingSide) const;
        virtual Square epSquare() const {return ep_square_;}
        virtual Color sideToMove() const {return side_to_move_;}
        virtual unsigned short halfmoveClock() const {return halfmove_clock_;}
        
        // Ply and move-counter
        unsigned short ply() const {return ply_;}
        unsigned short moveNumber() const {return (ply_ + 1) / 2;}
                
    protected:
        // Protected Functions
        void set_castling_right(Color, CastlingSide, bool);
        
        Board board_;
        
        /* Irreversible aspects of a position */
        CastlingRights castle_rights_;
        Square ep_square_;
        Color  side_to_move_;
        unsigned short halfmove_clock_;
        unsigned short ply_;
    };
    
    std::ostream& operator<<(std::ostream& out, const Position& position);
    bool operator==(const Position& lhs, const Position& rhs);
    bool operator!=(const Position& lhs, const Position& rhs);
}
#endif