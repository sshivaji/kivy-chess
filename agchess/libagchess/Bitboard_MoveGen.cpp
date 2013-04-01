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

#include "Bitboard_MoveGen.h"
#include "AGChess_Exception.h"

namespace AGChess {

    Bitboard sliding_attacks(const Bitboard& occupied, Piece p, Square s) {
        if (p == Rook) {
            return rank_attacks(occupied, s) | file_attacks(occupied, s);
        } else if (p == Bishop) {
            return diagonal_attacks(occupied, s) | antidiagonal_attacks(occupied, s);
        } else if (p == Queen) {
            return sliding_attacks(occupied, Rook, s) | sliding_attacks(occupied, Bishop, s);
        } else {
            throw AGChess_Exception("Bitboard_Movegen::sliding_attacks() Non-slider piece parameter");
        }        
    }  
    
#pragma mark -
#pragma mark Pawn Attacks
    
    Bitboard pawn_attacks_from_square(Square s, Color c) {
        if (c == White) {
            return w_pawn_attacks(squareBB(s));
        } else {
            return b_pawn_attacks(squareBB(s));
        }
    }
    
#pragma mark -    
#pragma mark Pawn Moves
    
    Bitboard w_pawn_attacks_to(const Bitboard& wpawns, Square s) {
        return (soEaOne(squareBB(s)) | soWeOne(squareBB(s))) & wpawns;
    }
    
    Bitboard b_pawn_attacks_to(const Bitboard& bpawns, Square s) {
        return (noEaOne(squareBB(s)) | noWeOne(squareBB(s))) & bpawns;
    }

    
    /* Pawn pushes */
    Bitboard w_pawn_single_push_targets(const Bitboard& wpawns, const Bitboard& empty) {
        return nortOne(wpawns) & empty;
    }
    
    Bitboard w_pawn_double_push_targets(const Bitboard& wpawns, const Bitboard& empty) {
        // Single push targets shifted 1 rank AND empty AND fourth rank
        return nortOne(w_pawn_single_push_targets(wpawns, empty)) & empty & RanksBB[3];
    }
    
    Bitboard b_pawn_single_push_targets(const Bitboard& bpawns, const Bitboard& empty) {
        return soutOne(bpawns) & empty;
    }
    
    Bitboard b_pawn_double_push_targets(const Bitboard& bpawns, const Bitboard& empty) {
        // Single push targets shifted 1 rank AND empty AND fifth rank
        return soutOne(b_pawn_single_push_targets(bpawns, empty)) & empty & RanksBB[4];
    }
    
#pragma mark -
#pragma mark Pawns Able to Push
    
    Bitboard w_pawns_able_to_push(const Bitboard& wpawns, const Bitboard& empty) {
        return soutOne(empty) & wpawns;
    }
    
    Bitboard w_pawns_able_to_double_push(const Bitboard& wpawns, const Bitboard& empty) {
        Bitboard emptyRank3 = soutOne(empty & RanksBB[3]) & empty;
        return w_pawns_able_to_push(wpawns, emptyRank3);
    }
    
    Bitboard b_pawns_able_to_push(const Bitboard& bpawns, const Bitboard& empty) {
        return nortOne(empty) & bpawns;
    }
    
    Bitboard b_pawns_able_to_double_push(const Bitboard& bpawns, const Bitboard& empty) {
        Bitboard emptyRank6 = nortOne(empty & RanksBB[5]) & empty;
        return b_pawns_able_to_push(bpawns, emptyRank6);
    }
    
};