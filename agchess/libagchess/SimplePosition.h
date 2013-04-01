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


#ifndef AGCHESS_BASIC_POSITION_H
#define AGCHESS_BASIC_POSITION_H

#include "AGChess_Common.h"
#include "Position.h"
#include "Board.h"
#include "Move.h"

namespace AGChess {
        
   
    class SimplePosition : public Position {
        
    public:
        SimplePosition() : Position() {
            requires_promotion_ = false;
            setEpSquare(InvalidSquare);
            setSideToMove(White);
            castle_rights_ = CastlingRights(WOO | WOOO | BOO | BOOO);
        };
        
        /*!
         * @abstract Makes a move
         * @param a struct containing only the most basic elements necessary
         * to make and unmake a move
         * @discussion Moves according to move.from and move.to
         */
        virtual void make(basic_move& move);        
        virtual void unmake(const basic_move& move);
        
        virtual bool requires_promotion() {return requires_promotion_;}
        virtual void promote(Piece);
            
        virtual bool isCastle(const basic_move& move) const;
        virtual bool isEnPassantCapture(const basic_move& move) const;
    
        /* A valid move is one which specifies legal source and destination squares,
         * requiring that there is a piece on the source square and that it is 
         * of the correct color to move.  Note that this method does not require that
         * the color of the piece on the destination square is not the same as the piece 
         * that is moving. */
        virtual bool is_valid(const basic_move& move) const;
        
    protected:
        /* If interacting with a GUI, the promotion piece may not come at the
         * same time as the move.  We set the flag requires_promotion = true
         * if the position has a pawn on the first or eighth rank.  An exception
         * is thrown if another move is made before the promotion is resolved. */
        bool requires_promotion_;
        
        virtual bool isDoubleJump(const basic_move& move) const;
        Square ep_capture_square() const;
        
        /* Setters for instance variables */
        virtual void setBoard(const Board& b) { board_ = b;}
        virtual void setEpSquare(Square ep) { ep_square_ = ep;}
        virtual void setSideToMove(Color color) {side_to_move_ = color; };
        virtual void setHalfmoveClock(unsigned short halfmove) {halfmove_clock_ = halfmove;}
        virtual void setPly(unsigned short p) {ply_ = p;}
        virtual void setCastlingRights(CastlingRights right) {castle_rights_ = right;}
        
        /*! @abstract Checks after a move to see if the requires promotion flag
         *  needs to be set. */
        void check_requires_promotion();
        
        
        /* Include a method to assert the squares in a basic_move / Move */
        
    private:
        
    };
    
    std::ostream& operator<<(std::ostream& out, const SimplePosition& position);
};

#endif