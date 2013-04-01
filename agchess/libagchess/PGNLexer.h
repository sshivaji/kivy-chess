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


#ifndef PGNLEXER_H
#define PGNLEXER_H

#include <iostream>
#include <string>
#include "Token.h"
#include <vector>

namespace AGChess {

    using namespace std;
    
    class PGNLexer {
        
    public:
        PGNLexer();
        PGNLexer(const string& gametext, bool processHeaderOnly = false);
        
        const vector<Token>& tokens();
        void setGametext(const string& gametext, bool processHeaderOnly = false);
        
    private:
        
        const Token getNextToken();
        void skipWhitespace();
        void processTokens(bool processHeaderOnly = false);
        
        /* Returns true if the character is one that can start a move */
        bool isstartofmove(char c);
        
        vector<Token>    _tokens;
        size_t           it;            // Iterator
        size_t           end;
        string           _gametext;
        TokenType        lastTokenType;
        
    };

}
#endif