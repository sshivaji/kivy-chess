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

#ifndef AGCHESS_BITBOARD_H
#define AGCHESS_BITBOARD_H

#include <stdint.h>
#include <iostream>
#include "Square.h"
#include "ColoredPiece.h"

namespace AGChess {
    
    typedef uint64_t Bitboard;
    
    enum Direction{
        noWe =  7, nort = 8,  noEa = 9,
        west = -1,            east = 1,
        soWe = -9, sout = -8, soEa = -7
    };
    
    extern const Bitboard RanksBB[8];
    extern const Bitboard FilesBB[8];
    extern const Bitboard SquaresBB[65];
    extern const Bitboard PieceMovesBB[5][64];
    extern const unsigned char occupancy_bitboards[8][256];
    
    const Bitboard EmptyBB = 0;
    const Bitboard notAFile = 0xfefefefefefefefeULL;
    const Bitboard notHFile = 0x7f7f7f7f7f7f7f7fULL;
    const Bitboard longDiag = 0x8040201008040201ULL; // Long diagonal a1-h8
    const Bitboard longAdiag =0x0102040810204080ULL; // Long antidiagonal a8-h1
    
    Bitboard pieceMoves(Piece, Square);
    
    Bitboard generate_ray(Square, Direction);
    unsigned char generate_first_rank(unsigned char, signed char);
    
    /* Basic shifts */
    inline Bitboard nortOne(const Bitboard& b) {return b << 8;}
    inline Bitboard soutOne(const Bitboard& b) {return b >> 8;}
    inline Bitboard eastOne(const Bitboard& b) {return (b << 1) & notAFile;}
    inline Bitboard noEaOne(const Bitboard& b) {return (b << 9) & notAFile;}
    inline Bitboard soEaOne(const Bitboard& b) {return (b >> 7) & notAFile;}
    inline Bitboard westOne(const Bitboard& b) {return (b >> 1) & notHFile;}
    inline Bitboard soWeOne(const Bitboard& b) {return (b >> 9) & notHFile;}
    inline Bitboard noWeOne(const Bitboard& b) {return (b << 7) & notHFile;}
    
    inline Bitboard nortX(const Bitboard& b, unsigned char x) {return (x < 8) ? b << (8 * x) : EmptyBB;}
    inline Bitboard soutX(const Bitboard& b, unsigned char x) {return (x < 8) ? b >> (8 * x) : EmptyBB;}
    inline Bitboard eastX(const Bitboard& b, unsigned char x) {
        Bitboard bb = b;
        for (int i = 0; i < x; i++) {
            bb = eastOne(bb);
        }
        return bb;
    }
    inline Bitboard westX(const Bitboard& b, unsigned char x) {
        Bitboard bb = b;
        for (int i = 0; i < x; i++) {
            bb = westOne(bb);
        }
        return bb;
    }
    
    
    /* The following four methods use kindergarten bitboards to generate a bitboard
     * of attacked squares for sliding pieces along a given line (rank, file, or diagonal). 
     * The returned set of squares represents those squares which can be attacked
     * by a sliding piece, and must be filtered based on color to make sure that a sliding
     * piece cannot move to a square occupied by a friendly piece. */
    Bitboard rank_attacks(Bitboard occupied, Square s);
    Bitboard file_attacks(Bitboard occupied, Square s);
    Bitboard diagonal_attacks(Bitboard occupied, Square s);
    Bitboard antidiagonal_attacks(Bitboard occupied, Square s);                          
        
    inline const Bitboard& squareBB(Square s) { return SquaresBB[char(s)]; }
    //inline const Bitboard& squareBB(int s) { return SquaresBB[s]; }  // Is this method really needed?
    inline const Bitboard& ranksBB(unsigned char rank) {return RanksBB[rank]; }
    inline const Bitboard& filesBB(unsigned char file) {return FilesBB[file]; }
    
    Square squareForBitboard(Bitboard);
    int BBPopCount(Bitboard);
    
    // Debug
    extern void print_bitboard(const Bitboard&);
    
    inline void print_hex(const Bitboard& bb) {
        printf("0x%016llXULL,\n", bb);
    }
}
#endif