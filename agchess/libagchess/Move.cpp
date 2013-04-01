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



#include "Move.h"

namespace AGChess {

    basic_move::basic_move() {
        from_ = Square(Square::InvalidSquare);
        to_   = Square(Square::InvalidSquare);
        promoted_piece_ = None;
        reset();
    }  
    
    basic_move::basic_move(Square f, Square t, Piece p) 
    {
        from_ = f;
        to_   = t;
        promoted_piece_ = p;
        reset();
    }
    
    void basic_move::reset() {
        ep_square_ = Square(Square::InvalidSquare);
        captured_piece_ = NoColoredPiece;
        captured_square_ = Square(Square::InvalidSquare);
        castling_ = NoCastling;
        halfmove_clock_ = 0;
        ply_ = 0;
        is_castle_ = false;
        is_promotion_ = false;
        is_capture_ = false;
        side_to_move_ = White;
    }
    
    void basic_move::debug() const {
        std::cout << *this;
        std::cout << "En passant Square: " << epSquare() << std::endl;
        std::cout << "Captured Piece: " << std::string(capturedPiece().piece()) << std::endl;
        std::cout << "Captured Square: " << capturedSquare() << std::endl;
        std::cout << "Castling: " << castlingRights() << std::endl;
        std::cout << "Is Castle: " << isCastle() << std::endl;
        std::cout << "Is Promotion: " << isPromotion() << std::endl;
        std::cout << "Is Capture: " << isCapture() << std::endl;
        std::cout << "Side to move: " << (sideToMove() == White ? "White": "Black") << std::endl;
        std::cout << std::endl;
    }
    
    // Square from accessor and mutator
    Square basic_move::from() const {return from_;}
    void basic_move::setFrom(Square s) {from_ = s;}
    
    // Square to accessor and mutator
    Square basic_move::to() const {return to_;}
    void basic_move::setTo(Square s) {to_ = s;}
    
    
    bool basic_move::isValid() const {
        
        if (!from().isValid() || !to().isValid()) return false;
        if (from() == to()) return false;
        
        return true;
    }
    
    bool basic_move::isNull() const {
        return ((from() == InvalidSquare) && (to() == InvalidSquare));
    }
    
    Move::Move() : basic_move() {
        
    };
    
    Move::Move(const basic_move& move) : basic_move(move) {
    }
        
    std::ostream& operator<<(std::ostream& out, const basic_move& move) {
        out << "From: " << move.from();
        out << " To: " << move.to() << std::endl;
        out << "Promotion piece: " << std::string(move.promotionPiece()) << std::endl;
        return out;
    }
    
    std::ostream& operator<<(std::ostream& out, const Move& move) {
        if (move.SAN() == "") {
            out << static_cast<basic_move> (move);
            return out;
        } 
        
        out << move.SAN();
        if (move.comment() != "") {
            out << " {" << move.comment() << "} ";
        }

        return out;
    }
};