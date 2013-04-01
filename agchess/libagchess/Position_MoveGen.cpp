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


#include "Position_MoveGen.h"
#include "Bitboard_MoveGen.h"

namespace AGChess {

    Bitboard coloredPiecePseduoLegalMovesTo(Square square, ColoredPiece piece, const StandardPosition& position) {
        Bitboard b = EmptyBB;
        
        if (!piece.isPiece()) return b;  // Empty Bitboard for NoColoredPiece
        
        if (piece.piece() != Pawn) {
            if (piece.isSlider()) {
                b = sliding_attacks(position.board().occupied(), piece.piece(), square);
            } else {
                // piece is a Knight or King
                b = pieceMoves(piece.piece(), square);
            }
            b &= position.board().bitboard(piece); 

        } else {  // piece.piece() == Pawn
            Color c = piece.color();
            ColoredPiece p = position.at(square);
            Bitboard sq = squareBB(square);
            
            if (c == White) {
                const Bitboard& wpawns = position.board().bitboard(WP);

                // Is the square unoccupied?
                if (!p.isPiece()) {
                    if ((square == position.epSquare()) && (position.epSquare().rank() == 5)) {
                        b = w_pawn_attacks_to(wpawns, square);  // square is the en passant square, calculate attacks
                    } else {
                        // Square is not en passant square, so calculate pushes
                        b = w_pawns_able_to_push(wpawns, position.board().empty()) |
                        w_pawns_able_to_double_push(wpawns, position.board().empty());
                        b &= (soutOne(sq) | soutX(sq, 2));
                    }
                } 
                // Is the square occupied by an enemy piece?
                else if (p.color() == Black) {
                    b = w_pawn_attacks_to(wpawns, square);  // square is occupied by an enemy piece, calculate attacks
                }
                // else square is occupied by friendly piece
                /* Return empty bitboard since pawns can't move onto a square occupied by a friendly */
            } else { // c == Black
                const Bitboard& bpawns = position.board().bitboard(BP);
                
                // Is the square unoccupied?
                if (p == NoColoredPiece) {
                    if ((square == position.epSquare()) && (position.epSquare().rank() == 2)) {
                        b = b_pawn_attacks_to(bpawns, square);  // square is the en passant square, calculate attacks
                    } else {
                        // Square is not en passant square, so calculate pushes
                        b = b_pawns_able_to_push(bpawns, position.board().empty()) |
                        b_pawns_able_to_double_push(bpawns, position.board().empty());
                        b &= (nortOne(sq) | nortX(sq, 2));
                    }
                } 
                // Is the square occupied by an enemy piece?
                else if (p.color() == White) {
                    b = b_pawn_attacks_to(bpawns, square);  // square is occupied by an enemy piece, calculate attacks
                }
                // else square is occupied by friendly piece
                /* Return empty bitboard since pawns can't move onto a square occupied by a friendly */
            }
        }
 
        return b;
    }
}