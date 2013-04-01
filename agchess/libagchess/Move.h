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


#ifndef AGCHESS_MOVE_H
#define AGCHESS_MOVE_H

#include <string>
#include <vector>
#include "AGChess_Common.h"
#include "Square.h"

namespace AGChess {
    
    class basic_move {
        friend class SimplePosition;
        friend class StandardPosition;
        
    public:
        
        basic_move();
        basic_move(Square from, Square to, Piece promote_piece = None);
        
        Square from() const;
        void setFrom(Square s);
        
        Square to() const;
        void setTo(Square s);
        
        Piece promotionPiece() const {return promoted_piece_;}
        void setPromotionPiece(Piece p) {promoted_piece_ = p;}
        
        CastlingRights castlingRights() const {return castling_;}
        void setCastlingRights(CastlingRights castling) {castling_ = castling;}
        
        ColoredPiece capturedPiece() const {return captured_piece_;}
        void setCapturedPiece(ColoredPiece p) {captured_piece_ = p;}
        
        Square capturedSquare() const {return captured_square_;}
        void setCapturedSquare(Square s) {captured_square_ = s;}
        
        Square epSquare() const {return ep_square_;}
        void setEpSquare(Square s) {ep_square_ = s;}
        
        bool isPromotion() const {return is_promotion_;}
        void setIsPromotion(bool p) {is_promotion_ = p;}
        
        bool isCastle() const {return is_castle_;}
        void setIsCastle(bool castle) { is_castle_ = castle; }
        
        bool isCapture() const {return is_capture_;}
        void setIsCapture(bool capture) {is_capture_ = capture;}
        
        unsigned short halfmoveClock() const {return halfmove_clock_;}
        void setHalfmoveClock(unsigned short c) {halfmove_clock_ = c;}
        
        unsigned short ply() const {return ply_;}
        void setPly(unsigned short p) {ply_ = p;}
        
        Color sideToMove() const {return side_to_move_;}
        void setSideToMove(Color c) {side_to_move_ = c;}
        
        void reset();
        bool isValid() const;
        bool isNull() const;
        
        void debug() const;
        
    private:
        Square          from_;
        Square          to_;
        Piece           promoted_piece_;  // By default is None
        
        /* Captured piece information */
        ColoredPiece    captured_piece_;  // By default is NoColoredPiece
        Square          captured_square_; // Convenience for determining en passant captures
        
        /* State information for restoring the position */
        Square          ep_square_;               
        CastlingRights   castling_;
        unsigned short   halfmove_clock_;
        unsigned short   ply_;
        Color           side_to_move_;
        
        /* Special move flags */
        bool             is_castle_;
        bool             is_promotion_;
        bool             is_capture_;
    };
    
    class Move : public basic_move {
        
    public:
        Move();
        Move(const basic_move& move);
        const std::string& SAN() const {return SAN_;}
        const std::string& comment() const {return comment_;}
        const std::vector<unsigned char>& NAG() const {return NAG_;}
        
        void setSAN(const std::string& SAN) const {SAN_ = SAN;}
        void setComment(const std::string& comment) const {comment_ = comment;}
        
    private:
        mutable std::string      SAN_;                 // Standard Algebraic Notation string representation
        mutable std::string      comment_;             // Comment string
        mutable std::vector      <unsigned char> NAG_; // Vector of Numeric Annotation Glyphs, since we can have
                                              // multiple glyphs for a single move
    };
    
    std::ostream& operator<<(std::ostream& out, const basic_move& move);
    std::ostream& operator<<(std::ostream& out, const Move& move);
    
}
#endif