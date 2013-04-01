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


#include "Square.h"
#include "AGChess_Exception.h"

namespace AGChess {
    
    const Square Square::sa1 = Square(0);

    Square::Square() {
        square_ = 64;
    }
    
    Square::Square(unsigned char square) {
        if (square > 64) {
            square = 64;
        }
        square_ = square;
    }
    
    Square::Square(unsigned char rank, unsigned char file) {
        if ((rank > 7) || (file > 7)) {
            square_ = 64;
        } else {
            square_ = rank * 8 + file;
        }
    }
    
    Square::Square(const std::string& str) {
        if (str.length() != 2) {
            square_ = 64;
        }
        
        unsigned char file = (unsigned char)(str.at(0) - 'a');
        unsigned char rank = (unsigned char)(str.at(1) - '1');
        if ((rank > 7) || (file > 7)) {
            square_ = 64;
        } else {
            square_ = rank * 8 + file;
        }
    }
    
    bool Square::isValid() const {
        return square_ != 64;
    }
    
    unsigned char Square::rank() const {
        if (isValid()) return square_ / 8;
        else {
            return 8;
        }
    }
    
    unsigned char Square::file() const {
        if (isValid()) return square_ % 8;
        else {
            return 8;
        }
    }
    
    Square::operator std::string() const {
        std::string name;
        if (isValid()) {
            char tmp = file() + 'a';
            name += tmp;
            tmp = rank() + '1';
            name += tmp;
        } else {
            name = "Invalid Square";
        }
        
        return name;
    }
    
    Square::operator unsigned char() const {
        return square_;
    }
    
    bool Square::operator==(const Square& rhs) const {
        return square_ == rhs.square_;
    }
    
    bool Square::operator!=(const Square& rhs) const {
        return square_ != rhs.square_;
    }
    
    std::ostream& operator<<(std::ostream& out, const Square& square) {
        out << std::string(square);
        return out;
    }
    
    void validateSquare(Square s)
    {
        if (!s.isValid()) {
            throw AGChess_Exception("validateSquare() Invalid Square");
        }
    }
    
#pragma mark -
#pragma mark Square shifts
    
    Square nortOne(Square s) { return Square(s.rank() + 1, s.file())    ; }
    Square soutOne(Square s) { return Square(s.rank() - 1, s.file())    ; }
    Square eastOne(Square s) { return Square(s.rank()    , s.file() + 1); }
    Square westOne(Square s) { return Square(s.rank()    , s.file() - 1); }
    Square noEaOne(Square s) { return Square(s.rank() + 1, s.file() + 1); }
    Square noWeOne(Square s) { return Square(s.rank() + 1, s.file() - 1); }
    Square soEaOne(Square s) { return Square(s.rank() - 1, s.file() + 1); }
    Square soWeOne(Square s) { return Square(s.rank() - 1, s.file() - 1); }
    
}