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

#include "Piece.h"

namespace AGChess {

    Piece::Piece() {
        piece_ = 0;
    }
    
    /*
    Piece::Piece(AGChessPieceT piece) {
        if (piece > 6) {piece_ = 0;}
        else {
            piece_ = piece;
        }
    }
     */
    
    Piece::Piece(char c) {
        switch (c) {
            case 'K':
                piece_ = KingPiece;
                break;
            case 'Q':
                piece_ = QueenPiece;
                break;
            case 'P':
                piece_ = PawnPiece;
                break;
            case 'B':
                piece_ = BishopPiece;
                break;
            case 'N':
                piece_ = KnightPiece;
                break;
            case 'R':
                piece_ = RookPiece;
                break;
            default:
                piece_ = NoPiece;
                break;
        }
    }
    
    bool Piece::operator==(const Piece& rhs) const {
        return piece_ == rhs.piece_;
    }
    
    bool Piece::operator!=(const Piece& rhs) const {
        return piece_ != rhs.piece_;
    }
    
    Piece::operator char() const {
        switch (piece_) {
            case KingPiece:   return 'K';
            case QueenPiece:  return 'Q';
            case PawnPiece:   return 'P';
            case BishopPiece: return 'B';
            case KnightPiece: return 'N';
            case RookPiece:   return 'R';
            default:          return '*';
        }
    }
    
    Piece::operator std::string() const {
        switch (piece_) {
            case KingPiece:   return "King";
            case QueenPiece:  return "Queen";
            case PawnPiece:   return "Pawn";
            case BishopPiece: return "Bishop";
            case KnightPiece: return "Knight";
            case RookPiece:   return "Rook";
            default:          return "No Piece";
        }
    }
    
    bool Piece::isSlider() const {
        return (piece_ == QueenPiece) || (piece_ == BishopPiece) || (piece_ == RookPiece);
    }
    
    bool Piece::isPiece() const {
        return piece_ != NoPiece;
    }

    unsigned char Piece::enumValue() const {
        return piece_;
    }
    
    std::ostream& operator<<(std::ostream& out, const Piece& piece) {
        out << std::string(piece);
        return out;
    }
    
    bool operator==(const Piece& lhs, char rhs) {
        return lhs == Piece(rhs);
    }
    
    bool operator!=(const Piece& lhs, char rhs) {
        return lhs != Piece(rhs);
    }
}