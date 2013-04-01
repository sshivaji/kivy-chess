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


#include "FEN.h"
#include "AGChess_Exception.h"
#include <sstream>

namespace AGChess {
    
    /* Counts the number of occurrences of aChar in str */
    int count(const std::string& str, char aChar)
    {
        int count = 0;
        for (int i = 0; i < str.length(); i++) {
            if (str.at(i) == aChar) {
                count++;
            }
        }
		
        return count;
    }
    
    /* Converts aChar to it's integral value */
    int charToInt(char aChar) {
        return (aChar - '0');
    }
    
    /* Returns true if str contains aChar */
    bool instr(const std::string& str, char aChar)
    {	
        return strpbrk(str.c_str(), &aChar);
    }
    
    EditablePosition positionFromFen(const std::string& fen) {
        EditablePosition p;
        p.reset();
        
        /* Tokenize the fen string */
        std::stringstream fenStream;
        fenStream.str(fen);
        std::string fenPos, fenActiveColor, fenCastling,
        fenEP, fenHalfmove, fenFullmove;
        
        std::getline(fenStream, fenPos, ' ');
        std::getline(fenStream, fenActiveColor, ' ');
        std::getline(fenStream, fenCastling, ' ');
        std::getline(fenStream, fenEP, ' ');
        std::getline(fenStream, fenHalfmove, ' ');
        std::getline(fenStream, fenFullmove, ' ');
        
        if (fenStream.fail()) {
            throw AGChess_Exception("Bad FEN Position Syntax");
        }
        
        /* Parse the board */
        Board board = processFenPosition(fenPos);
        std::cout << board;
        p.setBoard(board);
        
        /* Parse side to move */
        if      (fenActiveColor == "w") {p.setSideToMove(White);} 
        else if (fenActiveColor == "b") {p.setSideToMove(Black);}
        else                            {throw AGChess_Exception("positionFromFen() Invalid castling color");}
        
        /* Parse castling rights */
        if (instr(fenCastling, '-')) {
            // No castling rights
            p.setCastlingRights(NoCastling);
        } else {
            std::cout << "Processing castling rights" << std::endl;
            
            if (instr(fenCastling, 'K')) {p.set_castling_right(White, Kingside, true);} 
            if (instr(fenCastling, 'Q')) {p.set_castling_right(White, Queenside, true);}
            if (instr(fenCastling, 'k')) {p.set_castling_right(Black, Kingside, true);}
            if (instr(fenCastling, 'q')) {p.set_castling_right(Black, Queenside, true);}
        }
        
        /* Parse en passant square */
        Square epSquare;
        if (instr(fenEP, '-')) {
            epSquare = InvalidSquare;
            p.setEpSquare(epSquare);
        } else {
            epSquare = Square(fenEP);
            if (epSquare == InvalidSquare) {
                throw AGChess_Exception("positionFromFen() InvalidSquare set in En Passant");
            } else {
                p.setEpSquare(epSquare);
            }
        }
        
        /* Parse the halfmove clock */
        p.setHalfmoveClock(atoi(fenHalfmove.c_str()));
        
        /* Parse fullmove clock */
        p.set_move_number(atoi(fenFullmove.c_str()));
        return p;
    }
    
    Board processFenPosition(const std::string& pos)
    {	
        Board board(EmptyStartPosition);
        
        if ((count(pos, '/') != 7) || (count(pos, 'k') != 1) || (count(pos, 'K') != 1)) {
            throw AGChess_Exception("processFenPosition() Invalid number of Kings or Ranks.");
        } 
        
        int rank = 7;
        int file = 0;
        for (int i = 0; i < pos.length(); i++) {
            char c = pos.at(i);
            //cout << c;
            if (c == '/') {
                rank--;
                file = 0;
            } else if (isnumber(c)) {
                file += charToInt(c);
            } else {
                ColoredPiece p(c);
                if (!p.isPiece()) {
                    std::string throwStr = "processFenPosition() Invalid piece character in FEN: ";
                    throwStr = throwStr + c;
                    throw AGChess_Exception(throwStr);} 
                else
                {
                    Square s = Square(rank, file);
                    board.set(s, p);
                    file++;
                }
            }
        }
        
        return board;
    }
    
    std::string fenFromPosition(const Position& position) {
        std::string fenString;
        
        /* Describe the board position */
        int empty = 0; // Number of empty squares in a row
        for (int i = 7; i >= 0; i--) {
            for (int j = 0; j < 8; j++) {
                ColoredPiece p = position.at(Square(i, j));
                if (p == NoColoredPiece) {
                    empty++;
                } else {
                    if (empty > 0) {
                        fenString += (char('0' + empty));
                    } 
                    fenString += char(p);
                    empty = 0;
                }
            }
            if (empty > 0) {
                fenString += char('0' + empty);
                empty = 0;
            }
            fenString.append("/");
        }
        
        fenString.erase(--fenString.end());  // Remove the extra '/' at the end
        fenString += " ";
        
        /* Side to move */
        fenString += (position.sideToMove() == White ? "w" : "b");
        fenString += " ";
        
        /* Castling rights */
        if (position.castlingRights() == NoCastling) {
            fenString += "-";
        } else {
            if (position.hasCastlingRight(White, Kingside))  fenString += "K";
            if (position.hasCastlingRight(White, Queenside)) fenString += "Q";
            if (position.hasCastlingRight(Black, Kingside))  fenString += "k";
            if (position.hasCastlingRight(Black, Queenside)) fenString += "q";
        }
        fenString += " ";
        
        /* En passant square */
        if (position.epSquare() != InvalidSquare) {
            fenString += std::string(position.epSquare());
        } else {
            fenString += "-";
        }
        fenString += " ";
            
        
        /* Halfmove clock */
        std::stringstream out;
        out << position.halfmoveClock();
        fenString += out.str();
        fenString += " ";
        
        /* Fullmove clock */
        std::stringstream out2;
        out2 << position.moveNumber();
        fenString += out2.str();
        
        return fenString;
    }

};