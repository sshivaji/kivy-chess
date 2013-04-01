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

#include "Board.h"
#include "AGChess_Exception.h"

namespace AGChess {

#pragma mark Board Editing Methods
    
    Board::Board(StartPosition p) {
        if (p == EmptyStartPosition) {
            set_empty_position();
        } else {
            set_standard_position();
        }
    }
    
    void Board::clear(Square sq) {
        ColoredPiece p = at(sq);
        if (!p.isPiece()) return; // Break early if the Square is unoccupied
        
        Bitboard& b = piece_bitboard(p);
        Bitboard sqbb = squareBB(sq); 
        b &= ~sqbb;
        pieceForSquare_[char(sq)] = NoColoredPiece;
    }
    
    void Board::set(Square sq, ColoredPiece p) {
#warning validateColoredPieceType(p);
        //validateColoredPieceType(p);
        clear(sq);
        if (!p.isPiece()) return; // Break early if the piece
        
        Bitboard& b = piece_bitboard(p);
        Bitboard sqbb = squareBB(sq);
        b |= sqbb;
        pieceForSquare_[char(sq)] = p;
    }
    
    void Board::move(Square from, Square to) {
        ColoredPiece p = at(from);  // Validates from square
        if (!p.isPiece()) throw AGChess_Exception("basic_board::move Cannot move from an empty square"); 
        clear(to);
        set(to, p);
        clear(from);
    }
    
    /* Returns the ColoredPieceType at sq, and does bounds checking */
    ColoredPiece Board::at(Square sq) const { 
#warning validateSquare(sq); 
        return pieceForSquare_[sq];
    }
    
    /* Compares element by element with rhs.  Returns true if all
     * elements are equal */
    bool Board::operator==(const Board& rhs) const {
        
        /* // Debug
        std::cout << "White Pawns: " << (pawnsBB_[0]   == rhs.pawnsBB_[0]) << std::endl;
        std::cout << "Black Pawns: " << (pawnsBB_[1]   == rhs.pawnsBB_[1]) << std::endl;
        std::cout << "White Kings: " << (kingsBB_[0]   == rhs.kingsBB_[0]) << std::endl;
        std::cout << "Black Kings: " << (kingsBB_[1]   == rhs.kingsBB_[1]) << std::endl;
        std::cout << "White Rooks: " << (rooksBB_[0]   == rhs.rooksBB_[0]) << std::endl;
        std::cout << "Black Rooks: " << (rooksBB_[1]   == rhs.rooksBB_[1]) << std::endl;
        std::cout << "White Queens: " << (queensBB_[0]  == rhs.queensBB_[0]) << std::endl;
        std::cout << "Black Queens: " << (queensBB_[1]  == rhs.queensBB_[1]) << std::endl;
        std::cout << "White Knights: " << (knightsBB_[0] == rhs.knightsBB_[0]) << std::endl;
        std::cout << "Black Knights: " << (knightsBB_[1] == rhs.knightsBB_[1]) << std::endl;
        std::cout << "White Bishops: " << (bishopsBB_[0] == rhs.bishopsBB_[0]) << std::endl;
        std::cout << "Black Bishops: " << (bishopsBB_[1] == rhs.bishopsBB_[1]) << std::endl;
        */
         
        return (pawnsBB_[0]   == rhs.pawnsBB_[0] &&
                pawnsBB_[1]   == rhs.pawnsBB_[1] &&
                kingsBB_[0]   == rhs.kingsBB_[0] &&
                kingsBB_[1]   == rhs.kingsBB_[1] &&
                rooksBB_[0]   == rhs.rooksBB_[0] &&
                rooksBB_[1]   == rhs.rooksBB_[1] &&
                queensBB_[0]  == rhs.queensBB_[0] &&
                queensBB_[1]  == rhs.queensBB_[1] &&
                knightsBB_[0] == rhs.knightsBB_[0] &&
                knightsBB_[1] == rhs.knightsBB_[1] &&
                bishopsBB_[0] == rhs.bishopsBB_[0] &&
                bishopsBB_[1] == rhs.bishopsBB_[1]
                );
    }
    
#pragma mark -
    
    Bitboard Board::occupied() const {
        return occupied(White) | occupied(Black);
    }
    
    Bitboard Board::occupied(Color c) const {
        unsigned char i = c.color_index();
        return pawnsBB_[i] | kingsBB_[i] | rooksBB_[i] |
        queensBB_[i] | knightsBB_[i] | bishopsBB_[i];
    }

    Bitboard Board::empty() const {
        return ~occupied();
    }
    
    Bitboard& Board::piece_bitboard(Square sq) {
#warning  validateSquare(sq); 
        
        ColoredPiece p = at(sq);
        if (!p.isValid()) throw AGChess_Exception("basic_board::piece_bitboard No bitboard "
                                        "for empty squares");
        return piece_bitboard(p);
    }
    
    
    Bitboard& Board::piece_bitboard(ColoredPiece p) {
        /* Throws an exception if p is invalid or if piece is NoPiece */
        
        unsigned char c = p.color().color_index();
        
        Piece piece = p.piece();
        
        if      (piece == Rook)   {return rooksBB_[c];   }
        else if (piece == Knight) {return knightsBB_[c]; }
        else if (piece == Bishop) {return bishopsBB_[c]; }
        else if (piece == Queen)  {return queensBB_[c];  }
        else if (piece == King)   {return kingsBB_[c];   }
        else if (piece == Pawn)   {return pawnsBB_[c];   }
        else {
            throw AGChess_Exception("basic_board::piece_bitboard No bitboard "
                                    "for empty squares");
        }
    }
    
    /* const piece_bitboard function for use by other objects (basic_position) */
    const Bitboard& Board::bitboard(Square sq) const {
        ColoredPiece p = at(sq);
        if (!p.isPiece()) throw AGChess_Exception("basic_board::piece_bitboard No bitboard "
                                        "for empty squares");
        
        return bitboard(p);
    }
    
    
    /* const piece_bitboard function for use by other objects (basic_position) */
    const Bitboard& Board::bitboard(ColoredPiece p) const {
        
        unsigned char c = p.color().color_index();
        
        Piece piece = p.piece();
        
        if      (piece == Rook)   {return rooksBB_[c];   }
        else if (piece == Knight) {return knightsBB_[c]; }
        else if (piece == Bishop) {return bishopsBB_[c]; }
        else if (piece == Queen)  {return queensBB_[c];  }
        else if (piece == King)   {return kingsBB_[c];   }
        else if (piece == Pawn)   {return pawnsBB_[c];   }
        else {
            throw AGChess_Exception("basic_board::piece_bitboard No bitboard "
                                    "for empty squares");
        }    
    }
    
    Bitboard Board::bitboard(Piece p) const {
        return bitboard(ColoredPiece(White, p)) | bitboard(ColoredPiece(Black, p));
    }
    
#pragma mark -
#pragma mark Position Setups
    
    void Board::set_standard_position() {
        pawnsBB_[0]   = 0x000000000000ff00ULL;
        pawnsBB_[1]   = 0x00ff000000000000ULL;
        rooksBB_[0]   = 0x0000000000000081ULL;
        rooksBB_[1]   = 0x8100000000000000ULL;
        kingsBB_[0]   = 0x0000000000000010ULL;
        kingsBB_[1]   = 0x1000000000000000ULL;
        queensBB_[0]  = 0x0000000000000008ULL;
        queensBB_[1]  = 0x0800000000000000ULL;
        knightsBB_[0] = 0x0000000000000042ULL;
        knightsBB_[1] = 0x4200000000000000ULL;
        bishopsBB_[0] = 0x0000000000000024ULL;
        bishopsBB_[1] = 0x2400000000000000ULL;
        
        pieceForSquare_[a1] = WR;
        pieceForSquare_[b1] = WN;
        pieceForSquare_[c1] = WB;
        pieceForSquare_[d1] = WQ;
        pieceForSquare_[e1] = WK;
        pieceForSquare_[f1] = WB;
        pieceForSquare_[g1] = WN;
        pieceForSquare_[h1] = WR;

        pieceForSquare_[a2] = WP;
        pieceForSquare_[b2] = WP;
        pieceForSquare_[c2] = WP;
        pieceForSquare_[d2] = WP;
        pieceForSquare_[e2] = WP;
        pieceForSquare_[f2] = WP;
        pieceForSquare_[g2] = WP;
        pieceForSquare_[h2] = WP;
        
        pieceForSquare_[a8] = BR;
        pieceForSquare_[b8] = BN;
        pieceForSquare_[c8] = BB;
        pieceForSquare_[d8] = BQ;
        pieceForSquare_[e8] = BK;
        pieceForSquare_[f8] = BB;
        pieceForSquare_[g8] = BN;
        pieceForSquare_[h8] = BR;

        pieceForSquare_[a7] = BP;
        pieceForSquare_[b7] = BP;
        pieceForSquare_[c7] = BP;
        pieceForSquare_[d7] = BP;
        pieceForSquare_[e7] = BP;
        pieceForSquare_[f7] = BP;
        pieceForSquare_[g7] = BP;
        pieceForSquare_[h7] = BP;
        
        for (int i = a3; i < a7; i++) {
            pieceForSquare_[i] = NoColoredPiece;
        }
    }
    
    void Board::set_empty_position() {
        /* Initialize to empty board */
        for (int i = 0; i < 2; i++) {
            pawnsBB_[i]   = 0;	
            rooksBB_[i]   = 0;
            kingsBB_[i]   = 0;
            queensBB_[i]  = 0;
            knightsBB_[i] = 0;
            bishopsBB_[i] = 0;
        }
        
        /* Clear the piece array */
        for (int i = 0; i < 64; i++) {
            pieceForSquare_[i] = NoColoredPiece;
        }
    }
    
#pragma mark -
#pragma mark Output stream
    std::ostream& operator<<(std::ostream& out, const Board& board) {
        out << std::endl;
        /* Loop over each rank and file and print the piece, starting with the 
         * 8th rank */
        for (int r = 7; r >= 0 ; r--) {
            for (int f = 0; f < 8; f++) {
                out << char(board.at(Square(r, f))) << " ";
            } 
            out << std::endl;
        }
        out << std::endl;
    
        return out;
    }    
}