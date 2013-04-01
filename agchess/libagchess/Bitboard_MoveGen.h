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

#ifndef AGCHESS_BITBOARD_MOVEGEN_H
#define AGCHESS_BITBOARD_MOVEGEN_H

#include "Bitboard.h"

namespace AGChess {
  
    Bitboard sliding_attacks(const Bitboard& occupied, Piece pt, Square s);
    inline Bitboard sliding_attacks(const Bitboard& occupied, ColoredPiece p, Square s) {return sliding_attacks(occupied, p.piece(), s);}
    
    /* Bitboards for intermediate calculations of pawn attacks */
    
    /* Pawn attacks */
    inline Bitboard w_pawn_attacks(const Bitboard& wpawns) {return noEaOne(wpawns) | noWeOne(wpawns);}
    inline Bitboard b_pawn_attacks(const Bitboard& bpawns) {return soEaOne(bpawns) | soWeOne(bpawns); }
    
    Bitboard w_pawn_attacks_to(const Bitboard& wpawns, Square s);
    Bitboard b_pawn_attacks_to(const Bitboard& bpawns, Square s);
    
    Bitboard pawn_attacks_from_square(Square s, Color c);
    
    /* Pawn pushes intermediate values */
    Bitboard w_pawn_single_push_targets(const Bitboard& wpawns, const Bitboard& empty);
    Bitboard w_pawn_double_push_targets(const Bitboard& wpawns, const Bitboard& empty);
    Bitboard b_pawn_single_push_targets(const Bitboard& bpawns, const Bitboard& empty);
    Bitboard b_pawn_double_push_targets(const Bitboard& bpawns, const Bitboard& empty);
    
    /* Pawn pushes */
    inline Bitboard w_pawn_push_targets(const Bitboard& wpawns, const Bitboard& empty) {
        return w_pawn_single_push_targets(wpawns, empty) | w_pawn_double_push_targets(wpawns, empty); }
    
    inline Bitboard b_pawn_push_targets(const Bitboard& bpawns, const Bitboard& empty) {
        return b_pawn_single_push_targets(bpawns, empty) | b_pawn_double_push_targets(bpawns, empty); }
    
    /* Pawns able to push */
    Bitboard w_pawns_able_to_push(const Bitboard& wpawns, const Bitboard& empty);
    Bitboard w_pawns_able_to_double_push(const Bitboard& wpawns, const Bitboard& empty);
    Bitboard b_pawns_able_to_push(const Bitboard& bpawns, const Bitboard& empty);
    Bitboard b_pawns_able_to_double_push(const Bitboard& bpawns, const Bitboard& empty);
    
};

#endif