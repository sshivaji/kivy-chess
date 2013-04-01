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


#include "SAN.h"
#include "Position_MoveGen.h"

namespace AGChess {
    
    using namespace SAN;

    std::string moveToSan(const basic_move& move, const StandardPosition& position) {
        std::string san;
        
        /* This will be an inefficient implementation of moveToSan */
        basic_move       m = move;
        StandardPosition p = position;
        
        return san;
    }
    
    /* This SanToMove implementation works by copying the SAN string and removing information from
     * the copied string as the information is parsed, making it easier to parse other pieces of 
     * information from the simplified string. */
    basic_move SanToBasicMove(const std::string& SAN, const StandardPosition& position) {
        basic_move move;
        
        /* This will be an inefficient implementation of SanToMove */
        std::string      s = SAN;
        
        /* Remove extraneous characters that do not provide information needed by move */
        normalizeSanString(s);
        
        /* move is easy to set if SAN indicates castling */
        if (s == "O-O") {
            move.setTo((position.sideToMove() == White ? g1 : g8));
            move.setFrom((position.sideToMove() == White ? e1 : e8));
        } 
        else if (s == "O-O-O") {
            move.setTo((position.sideToMove() == White ? c1 : c8));
            move.setFrom((position.sideToMove() == White ? e1 : e8));
        } 
        else if (s == "--") {
            // This is a null move
            move.setTo(InvalidSquare);
            move.setFrom(InvalidSquare);
        }
        
        /* Otherwise it requires a bit more parsing */
        else {
            // Set a promotion piece
            move.setPromotionPiece(promotionPieceFromSan(s));
            if (move.promotionPiece().isPiece()) {
                s.erase(--s.end()); // Erase the last character from s if it indicates a promotion
            }
            
            Piece pt = movingPieceFromSan(s);
            if (pt != Pawn) {
                s.erase(s.begin()); // Erase the first character from s, so that the moving piece is
                                    // removed from the move.
            }
            
            move.setTo(destinationFromSan(s));
            s.erase(s.length() - 2, 2); // Erase the last two characters from s (the destination square)
            
            move.setFrom(disambiguateSourceFromSan(s, position, pt, move.to()));
        }
        
        return move;
    }
    
    Move SanToMove(const std::string& SAN, const StandardPosition& position) {
        Move move = SanToBasicMove(SAN, position);
        move.setSAN(SAN);
        return move;
    }
    
    /* Removes SAN characters which aren't integral 
     * to finding the to and from squares of the move.
     * Precondition: s is a legal SAN string containing no whitespace
     * Postcondition: s denotes castling, or contains only the moving piece (if applicable),
     * disambiguation information (if applicable), the destination square, and a 
     * promoting piece (if applicable). */
    void SAN::normalizeSanString(std::string& s) {
        findAndRemove('x', s);
        findAndRemove('=', s);
        findAndRemove('+', s);
        findAndRemove('#', s);
        
        if      (s == "0-0-0") { s = "O-O-O";}
        else if (s == "0-0")   { s = "O-O";}
    }
    /* Removes the first instance of c if it exists in s */
    void SAN::findAndRemove(char c, std::string& s) {
        size_t found = s.find(c);
        if (found!=std::string::npos) {
            s.erase(found, 1);
        }
    }
    
    /* Preconditions: san is a valid SAN move that has been normalized via normalizeSanString
     * Returns the promoted piece as designated by san or returns 'None'. */
    Piece SAN::promotionPieceFromSan(const std::string& san) {
        char c = *(--san.end()); // Last character in san.  Can't throw an exception since san must be 
                                 // at least 2 characters long
        return Piece(c);
    }
    
    /* Preconditions: san is a valid, non-castling SAN move that has been normalized.
     * Returns the PieceType moving as indicated by SAN, either indicated by the English
     * character representation of the piece, or lack of indicating a pawn. */
    Piece SAN::movingPieceFromSan(const std::string& san) {
        Piece p = Pawn;
        if (strchr("NBRQK", *san.begin())) {
            p = Piece(*san.begin());
        }
        return p;
    }
    
    /* Preconditions: san is a valid, non-castling SAN move that has been normalized, and 
     * trailing characters indicated a promotion piece have been removed from san.
     * Returns the destination square as indicated by san */
    Square SAN::destinationFromSan(const std::string& san) {
        std::string tmp = san.substr(san.length() - 2, 2);
        return Square(tmp);  // Pull the last 2 characters from the string
    }
    
    Square SAN::disambiguateSourceFromSan(const std::string& san, const StandardPosition& pos, Piece pt, Square dest) {

        // No need for disambiguation - the source square is given in the san move
        if (san.length() == 2) {
            return Square(san);
        }
        
        // Get the bitboard of all pieces of pt which can pseudo-legally move to the destination square
        ColoredPiece piece = ColoredPiece(pos.sideToMove(), pt);
        Bitboard b = coloredPiecePseduoLegalMovesTo(dest, piece, pos);
        
        /* 1 character for disambiguation:
         * Either rank or file.  Use the rank or file Bitboard as a mask for the
         * piece which needs disambiguation. */
        if (san.length() == 1) {
            Bitboard mask;
            if ((san.at(0) >= 'a') && (san.at(0) <= 'h')) {
                // Disambiguate ranks
                mask = FilesBB[(san.at(0) - 'a')];
            } else if ((san.at(0) >= '1') && (san.at(0) <= '8')) {
                // Disambiguate files
                mask = RanksBB[(san.at(0) - '1')];
            }
            b &= mask;
        }
        
        /* Throw an exception if there is still ambiguity in the source square */
        if (BBPopCount(b) != 1) {
            print_bitboard(b);
            throw AGChess_Exception("SAN::disambiguateSourceFromSan() ambiguous source square in move");
        }
        
        return squareForBitboard(b);
    }
};