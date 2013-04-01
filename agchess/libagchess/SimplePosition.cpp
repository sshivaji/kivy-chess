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


#include "SimplePosition.h"
#include <cmath>

namespace AGChess {


    /*
    basic_position::basic_position() {
    
    };
     */
    
    
    void SimplePosition::make(basic_move& move) {
        if (requires_promotion()) throw AGChess_Exception("basic_position::move() Unpromoted pawn before move.");
        if (!is_valid(move)) throw AGChess_Exception("basic_position::move() Invalid basic_move");
        
        Square from = move.from();
        Square to   = move.to();
        
        /* Update move with pre-move information for un-make */
        /* THIS WILL HAVE TO CHANGE WHEN MOVE IS UPDATED WITH ACCESSORS AND MUTATORS */
        move.is_castle_ = isCastle(move);
        move.ply_ = ply_;
        move.halfmove_clock_ = halfmove_clock_;
        move.ep_square_ = epSquare();
        move.castling_ = castlingRights();
        
        // Save the moving piece for later
        ColoredPiece piece = at(from);
        Piece pieceT = piece.piece();
        
        /* If move is an en passant capture, update the unmake fields of move with information 
         * regarding the en passant capture */
        bool ep_capture = isEnPassantCapture(move);
        if (ep_capture) {
            move.is_capture_ = true;
            move.captured_square_ = ep_capture_square();
            move.captured_piece_ = at(move.captured_square_);
            ep_square_ = InvalidSquare;
            board_.clear(move.captured_square_); // Clear the captured square
        } 
        
        /* If move is castle, move the king and rook */
        else if (isCastle(move)) {
            move.is_castle_ = true;
            /* Would normally move the king here, but it will be
             * taken care of as a normal move later */
                 if (to == g1) {board_.move(h1, f1);} 
            else if (to == c1) {board_.move(a1, d1);}
            else if (to == g8) {board_.move(h8, f8);}
            else if (to == c8) {board_.move(a8, d8);}
        }
        
        /* Is the move a capture? */
        if (!ep_capture) {
            move.captured_piece_ = at(to); // Already taken care of if the move is an ep capture
            move.captured_square_ = to;
            if (move.captured_piece_) move.is_capture_ = true;
        }
        
        /* Move the piece */
        board_.move(from, to);
        
        /* Adjust castling rights if a King or rook is moved */
        if (pieceT == King) {
            set_castling_right(sideToMove(), Kingside, false);
            set_castling_right(sideToMove(), Queenside, false);
        } else if (pieceT == Rook) {
                 if ((from == h1) && (piece == WR)) set_castling_right(White, Kingside, false);
            else if ((from == a1) && (piece == WR)) set_castling_right(White, Queenside, false);
            else if ((from == h8) && (piece == BR)) set_castling_right(Black, Kingside, false);
            else if ((from == a8) && (piece == BR)) set_castling_right(Black, Queenside, false);
        }
        
        /* Adjust ep square and do promotions for pawns */
        if (pieceT == Pawn) {
            /* TODO WORK HERE */
        }
        
        
        check_requires_promotion();
    }
    
    void SimplePosition::unmake(const basic_move& move) {
        
    }    
    
    /* Promotes pawn if the Position requires a promotion.  Does nothing
     * if it doesn't require promotion */
    void SimplePosition::promote(Piece p) {
        
    }
    
#pragma mark -
#pragma mark Move Methods
    
    /* Doesn't check any chess rules... Validates a move in the following steps
     * 1. Verify source and destination squares are in a valid range
     * 2. Verify source and destination squares are different
     * 3. Verify that there is a piece on the source square
     * 4. Verify that the piece is of the correct color to move
     */
    bool SimplePosition::is_valid(const basic_move& move) const {
        if (move.isValid() == false) return false;
        
        ColoredPiece p = at(move.from());
        if (!p.isPiece()) return false;
        if (p.color() != sideToMove()) return false;
            
        return true;
    }
    
    /* Verifies that a move is a castling move in the following steps:
     * 
     * 1. Verify the moving piece is a King
     * 2. Verify that the source and destination squares are the right
     *    squares for the side trying to castle.
     * 3. Verify that the rook you're trying to castle with is on the
     *    correct square.
     * 4. Verify that the side trying to castle has the right to castle
     *    to the square indicated by the move.
     * 5. Verify that the destination square and the square in between 
     *    the king and destination square are unoccupied.
     */
    bool SimplePosition::isCastle(const basic_move& move) const {
        Square from = move.from();
        Square to   = move.to();
        ColoredPiece p = at(from);
        Color c = p.color();
        CastlingSide side;
        
        if (p.piece() != King) return false;
        
        if (c == White) {
            if ((from != e1) || ((to != g1) && (to != c1)))
                return false; // Invalid squares for castling

            /* Perhaps this is redundant because otherwise a castling right wouldn't exist if
             * a rook wasn't on it's proper square? */
            if ((to == g1) && (at(h1) != WR)) return false;
            else if ((to == c1) && (at(a1) != WR)) return false;
            
            side = (to == g1 ? Kingside : Queenside); // previous if statement guarantees to == g1 or c1
            
        } else if (c == Black) {
            if ((from != e8) || ((to != g8) && (to != c8)))
                return false; // Invalid squares for castling

            /* Perhaps this is redundant because otherwise a castling right wouldn't exist if
             * a rook wasn't on it's proper square? */
            if ((to == g8) && (at(h8) != BR)) return false;
            else if ((to == c8) && (at(a8) != BR)) return false;

            side = (to == g8 ? Kingside : Queenside); // previous if statement guarantees to == g8 or c8
        }
        
        if (!hasCastlingRight(c, side)) return false; // No castling right 
        
        /* Finally, check that the square in between and the destination square aren't occupied, 
         * as well as the square next to the rook if castling queenside */
        Square s;
        if (to == g1)      s = f1;
        else if (to == c1) s = d1;
        else if (to == g8) s = f8;
        else if (to == c8) s = d8;
        
        if ((to == c1) && at(b1)) return false;
        else if ((to == c8) && at(b8)) return false;
        
        /* at(Square) returns 0 if the square is unoccupied.
         * Checks that both the adjacent square and destination square
         * are unoccupied - returns true if both are unoccpuied */
        return !((at(s)) || (at(to))); 
    }
    
    /* Verifies that a move is an en passant capture in the following steps:
     *
     * 1. Verify that the the destination square is the en passant square
     * 2. Verify that the piece moving to the en passant square is a pawn
     * 3. Verify that the piece to be captured is an opposite colored pawn
     * 4. Verify that the source square is one diagonal square away from
     *    the en passant square
     */
    bool SimplePosition::isEnPassantCapture(const basic_move& move) const {
        Square from = move.from();
        Square to   = move.to();
        if (epSquare() != to) return false;
        
        ColoredPiece p = at(from);
        if (p.piece() != Pawn) return false;
        
        // The piece at the square behind the ep_square (from perspective of the side_to_move)
        ColoredPiece capture = at(ep_capture_square());
        if (capture != ColoredPiece(sideToMove().opposite(), Pawn)) return false;
     
        if ((abs(from.rank() - to.rank()) != 1) ||
            (abs(from.file() - to.file()) != 1))
            return false;
        
        return true; // All other conditions are met
    }
    
    Square SimplePosition::ep_capture_square() const {
        Square capture_sq = sideToMove() == White ? soutOne(epSquare()) : nortOne(epSquare());
        return capture_sq;
    }
    
    bool SimplePosition::isDoubleJump(const basic_move& move) const {
        Square from = move.from();
        Square to   = move.to();
        ColoredPiece p = at(from);
        if (p.piece() != Pawn) return false;
        
        unsigned char from_rank = (p.color() == White ? 1 : 6);
        unsigned char to_rank   = (p.color() == White ? 3 : 4);
        if ((from.rank() != from_rank) || (to == Square(to_rank, to.file()))) return false;
        
        return true;
    }
    
    /* This method should be called at the very end of a valid move, after the side_to_move
     * has been switched */
    void SimplePosition::check_requires_promotion() {
        // Pawn Bitboard
        Bitboard b = board_.bitboard(ColoredPiece(sideToMove().opposite(), Pawn));
        // Appropriate rank bitboard
        Bitboard r = RanksBB[ (sideToMove() == White ? 0 : 7)];
        
        requires_promotion_ = (b & r);
    }
    
#pragma mark -
    
    std::ostream& operator<<(std::ostream& out, const SimplePosition& position) {
        out << "En passant square: " << position.epSquare() << std::endl;
        out << "Side to move: " << (position.sideToMove() == White ? "White" : "Black") << std::endl;
        out << "Castling: ";
        if (position.castlingRights() == NoCastling) {out << "No Castling";}
        
        if (position.hasCastlingRight(White, Kingside)) out << "W";
        if (position.hasCastlingRight(White, Queenside)) out << "w";
        if (position.hasCastlingRight(Black, Kingside)) out << "B";
        if (position.hasCastlingRight(Black, Queenside)) out << "b";
        out << std::endl;
        
        out << position.board() << std::endl;
        return out;
    }
    
};