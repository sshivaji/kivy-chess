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


#ifndef AGCHESS_SQUARE_T_H
#define AGCHESS_SQUARE_T_H

#include <string>
#include <iostream>

namespace AGChess {
    
    class Square {
        
    public:
        enum AGChessSquareT {
            a1, b1, c1, d1, e1, f1, g1, h1,
            a2, b2, c2, d2, e2, f2, g2, h2,
            a3, b3, c3, d3, e3, f3, g3, h3,
            a4, b4, c4, d4, e4, f4, g4, h4,
            a5, b5, c5, d5, e5, f5, g5, h5,
            a6, b6, c6, d6, e6, f6, g6, h6,
            a7, b7, c7, d7, e7, f7, g7, h7,
            a8, b8, c8, d8, e8, f8, g8, h8,
            InvalidSquare
        };
        
        Square();
        Square(unsigned char square);
        Square(unsigned char rank, unsigned char file);
        Square(const std::string& squareString);
        
        unsigned char rank() const;
        unsigned char file() const;
        
        bool isValid() const;
        
        operator std::string() const;
        operator unsigned char() const;
        bool operator==(const Square& rhs) const;
        bool operator!=(const Square& rhs) const;
        
        static const Square sa1;
        
    private:
        unsigned char square_;
        
    };
    
    std::ostream& operator<<(std::ostream& out, const Square& square);
    
    /* Basic shifts for squares */
    Square nortOne(Square s);
    Square soutOne(Square s);
    Square eastOne(Square s);
    Square westOne(Square s);
    Square noEaOne(Square s);
    Square noWeOne(Square s);
    Square soEaOne(Square s);
    Square soWeOne(Square s);
    
    /* Validates that the Square is between a1 and h8, and throws an 
     Invalid_Square_Exception otherwise */
    void validateSquare(Square); 
    
    const Square a1 = Square(0);
    const Square b1 = Square(1);
    const Square c1 = Square(2);
    const Square d1 = Square(3);
    const Square e1 = Square(4);
    const Square f1 = Square(5);
    const Square g1 = Square(6);
    const Square h1 = Square(7);
    
    const Square a2 = Square(8);
    const Square b2 = Square(9);
    const Square c2 = Square(10);
    const Square d2 = Square(11);
    const Square e2 = Square(12);
    const Square f2 = Square(13);
    const Square g2 = Square(14);
    const Square h2 = Square(15);
    
    const Square a3 = Square(16);
    const Square b3 = Square(17);
    const Square c3 = Square(18);
    const Square d3 = Square(19);
    const Square e3 = Square(20);
    const Square f3 = Square(21);
    const Square g3 = Square(22);
    const Square h3 = Square(23);
    
    const Square a4 = Square(24);
    const Square b4 = Square(25);
    const Square c4 = Square(26);
    const Square d4 = Square(27);
    const Square e4 = Square(28);
    const Square f4 = Square(29);
    const Square g4 = Square(30);
    const Square h4 = Square(31);
    
    const Square a5 = Square(32);
    const Square b5 = Square(33);
    const Square c5 = Square(34);
    const Square d5 = Square(35);
    const Square e5 = Square(36);
    const Square f5 = Square(37);
    const Square g5 = Square(38);
    const Square h5 = Square(39);
    
    const Square a6 = Square(40);
    const Square b6 = Square(41);
    const Square c6 = Square(42);
    const Square d6 = Square(43);
    const Square e6 = Square(44);
    const Square f6 = Square(45);
    const Square g6 = Square(46);
    const Square h6 = Square(47);
    
    const Square a7 = Square(48);
    const Square b7 = Square(49);
    const Square c7 = Square(50);
    const Square d7 = Square(51);
    const Square e7 = Square(52);
    const Square f7 = Square(53);
    const Square g7 = Square(54);
    const Square h7 = Square(55);
    
    const Square a8 = Square(56);
    const Square b8 = Square(57);
    const Square c8 = Square(58);
    const Square d8 = Square(59);
    const Square e8 = Square(60);
    const Square f8 = Square(61);
    const Square g8 = Square(62);
    const Square h8 = Square(63);
    
    const Square InvalidSquare = Square(64);
    
}

#endif