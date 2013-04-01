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

#ifndef TOKEN_H
#define TOKEN_H
#include <string>

namespace AGChess {

    enum TokenType {
        TokenNone = 0,
        TokenStartTag = 1,
        TokenEndTag = 2,
        TokenStartAnnotation = 3,
        TokenEndAnnotation = 4,
        TokenStartRAV = 5,
        TokenEndRAV = 6,
        TokenPeriod = 7,
        //TokenNonPrinting = 8,
        TokenInteger = 8,  // = 8.  So we can do TokenType & 16 to determine whether to print
        //TokenPrinting = 16,
        TokenTagPair = 16,
        TokenAnnotationText = 17,
        TokenNAG = 18,
        TokenResult = 19,
        //TokenMovesOnly = 32,
        TokenMove = 32,
        TokenInvalid
        
    };
    
    struct Token {
        std::string token;
        TokenType tokenType;
    };

}
#endif