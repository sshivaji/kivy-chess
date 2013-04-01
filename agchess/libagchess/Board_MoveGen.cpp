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

#include "Board_MoveGen.h"
#include "Bitboard_MoveGen.h"

namespace AGChess {
    
    inline Bitboard sliding_attacks(const Board& board, Square s) {
        return sliding_attacks(board.occupied(), board.at(s), s);
    }
    
    Bitboard pawn_attacks(const Board& board, Color c) {
        return (c == White ? w_pawn_attacks(board.bitboard(WP)) : b_pawn_attacks(board.bitboard(BP)));
    }
    
    Bitboard pawn_pushes(const Board& board, Color c) {
        return (c == White ? w_pawn_push_targets(board.bitboard(WP), ~board.occupied()) : 
                             b_pawn_push_targets(board.bitboard(BP), ~board.occupied()));
    }
    
    Bitboard attacks(const Board& board, Square s) {
        ColoredPiece p = board.at(s);
        Piece pt = p.piece();
        Bitboard b = EmptyBB;
        
        if (pt.isSlider()) {b = sliding_attacks(board, s); }
        else if ((pt == Knight) || (pt == King)) {b == pieceMoves(pt, s);}
        else if (pt == Pawn) {b == pawn_attacks(board, p.color());}
        
        return b;
    }
    
    /* Returns the Bitboard of squares of pieces attacking square s */
    Bitboard attacks_to(const Board& board, Square s) {        
        Bitboard attacks = 0;
        Bitboard pawn_att = w_pawn_attacks_to(board.bitboard(WP), s) | b_pawn_attacks_to(board.bitboard(BP), s);
        Bitboard queens = board.bitboard(Queen);  // Since it's used twice we store instead of recalculating
        
        attacks |= pawn_att;
        attacks |= sliding_attacks(board.occupied(), Rook, s) & (queens | board.bitboard(Rook));
        attacks |= sliding_attacks(board.occupied(), Bishop, s) & (queens | board.bitboard(Bishop));
        attacks |= board.bitboard(Knight) & pieceMoves(Knight, s);
        attacks |= board.bitboard(King) & pieceMoves(King, s);
        
        return attacks;
        
    }
    
    bool squareAttackedByColor(const Board& board, Square s, Color c) {
        return attacks_to(board, s) & board.occupied(c);
    }
    
    /* Returns the Bitboard of squares that a piece on Square s can pseudo-legally move to */
    Bitboard pseudo_legal_moves_from(const Board& board, Square s) {
        ColoredPiece p = board.at(s);
        Bitboard b = EmptyBB;
        
        if (!p.isPiece()) return b;
        if (p.piece() == Pawn) {
            if (p.color() == White) {
                Bitboard pushes  = w_pawn_push_targets(squareBB(s), board.empty());
                Bitboard attacks = pawn_attacks_from_square(s, White) & board.occupied(Black);
                b = pushes | attacks;
            } else {
                Bitboard pushes  = b_pawn_push_targets(squareBB(s), board.empty());
                Bitboard attacks = pawn_attacks_from_square(s, Black) & board.occupied(White);
                b = pushes | attacks;
            }
        } else {
            return attacks(board, s);
        }

        return b;
    }
    
    Bitboard absolute_pins(const Board& board, Color c) {
        Square s = squareForBitboard(board.bitboard(ColoredPiece(c, King)));
        //unsigned char rank = rankOf(s);
        //unsigned char file = fileOf(s);
        
        Bitboard pins = EmptyBB;
        
        // Bitboards for for opposing pieces that can pin
        Bitboard rooks_and_queens   = board.bitboard(ColoredPiece(c.opposite(), Rook)) | 
                                      board.bitboard(ColoredPiece(c.opposite(), Queen));
        Bitboard bishops_and_queens = board.bitboard(ColoredPiece(c.opposite(), Bishop)) | 
                                      board.bitboard(ColoredPiece(c.opposite(), Queen));

        
        Bitboard straight_attacks = rooks_and_queens & pieceMoves(Rook, s);
        Bitboard diagonal_attacks = bishops_and_queens & pieceMoves(Bishop, s);
        
        if ((straight_attacks | diagonal_attacks) == 0) return EmptyBB;  // There are no pieces which can potentially pin
        
        Bitboard ray = EmptyBB;
        Bitboard sliders = EmptyBB;
        Bitboard blockers = EmptyBB;
        
        Direction diags[4] = {noEa, soEa, soWe, noWe};
        Direction lines[4] = {nort, sout, east, west};
        
        Bitboard occ    = board.occupied(c);       // Occupied squares
        Bitboard op_occ = board.occupied(c.opposite());  // Opponent's occupied squares

        /* Check for pinned pieces on each diagonal */
        for (unsigned char i = 0; i < 4; i++) {
            ray = generate_ray(s, diags[i]);
            sliders = sliding_attacks(op_occ, Bishop, s) & ray;
            if (sliders & diagonal_attacks) {
                blockers = sliders & occ;
                if (BBPopCount(blockers) == 1) pins |= blockers;
            }
        }
        
        /* Check for pinned pieces on each rank and file */
        for (unsigned char i = 0; i < 4; i++) {
            ray = generate_ray(s, lines[i]);
            sliders = sliding_attacks(op_occ, Rook, s);
            print_bitboard(sliders);
            if (sliders & straight_attacks) {
                blockers = sliders & occ;
                if (BBPopCount(blockers) == 1) pins |= blockers;
            }
        }
        
        return pins;
    }    
    
    Square kingSquare(const Board& board, Color c) {
        return squareForBitboard(board.bitboard(ColoredPiece(c, King)));
    }
    
    int coloredPieceCount(const Board& board, ColoredPiece p) {
        return BBPopCount(board.bitboard(p));
    }
    
    int colorCount(const Board& board, Color c) {
        return BBPopCount(board.occupied(c));
    }
    
    int pieceCount(const Board& board, Piece p) {
        return BBPopCount(board.bitboard(ColoredPiece(White, p)) | 
                          board.bitboard(ColoredPiece(Black, p)));
    }
};