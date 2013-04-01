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


#include "PGNLexer.h"

namespace AGChess {

PGNLexer::PGNLexer() {

}

PGNLexer::PGNLexer(const string& gametext, bool processHeaderOnly) {
    setGametext(gametext, processHeaderOnly);
}

const vector<Token>& PGNLexer::tokens() {
    return _tokens;
}

void PGNLexer::setGametext(const string& gametext, bool processHeaderOnly) {
    _gametext = gametext;    
    processTokens(processHeaderOnly);
}

void PGNLexer::skipWhitespace() {
    while ((it != end) && ((isspace(_gametext.at(it))))) {
        ++it;
    }
}

void PGNLexer::processTokens(bool processHeaderOnly) {
    lastTokenType = TokenNone;
    end = _gametext.length();   // End of string
    it  = 0;                    // Start of string
    Token t;
    
    skipWhitespace();
    while (it != end) {
        t = getNextToken();

#ifdef DEBUG
        cout << "TOKEN: " << t.token << endl;
#endif
        
        if (processHeaderOnly) {
            if ((t.tokenType != TokenStartTag) &&
                (t.tokenType != TokenEndTag) &&
                (t.tokenType != TokenTagPair)) {
                return;
            }
        }
        if (t.tokenType == TokenInvalid) {
            //cout << "Invalid Token: " << t.token << endl; // Debug
        }
        //cout << t.token << endl;
        _tokens.push_back(t);
        skipWhitespace();
        
        // Debug
        /*if (t.token != "\0") {
            cout << t.token << endl; }
         */
    }
    
    /* Add a '*' TokenResult if the _gametext doesn't
     * have a result at the end.
     */
    if (lastTokenType != TokenResult) {
        cout << "No TokenResult in PGNLexer::processTokens().  Adding '*' to end." << endl;
        t.tokenType = TokenResult;
        t.token = "*";
        _tokens.push_back(t);
    }
}

const Token PGNLexer::getNextToken() {
    Token t;
    char c = _gametext.at(it);
    
    /* The following tokens are tokens which require
     * a matching character to end the token
     * ex: '{' and '}', and '[' and ']'
     * We find the first instance of the closing character
     * and return the substring between the opening and
     * closing characters as the token.  Warns if no closing
     * character is present.
     */
    if (lastTokenType == TokenStartAnnotation) {
        size_t endOfToken = _gametext.find('}', it);
        // Our string isn't found - should be an error
        if (endOfToken == string::npos) {
            cout << "Error in PGNLexer::getNextToken [TokenStartAnnotation].  No closing '}' found" << endl;
            endOfToken = end;
        }
        t.tokenType = TokenAnnotationText;
        t.token = _gametext.substr(it, endOfToken - it);
        it = endOfToken;
    }
    else if (lastTokenType == TokenStartTag) {
        size_t endOfToken = _gametext.find(']', it);
        // Our string isn't found - should be an error
        if (endOfToken == string::npos) {
            cout << "Error in PGNLexer::getNextToken [TokenStartTag].  No closing ']' found" << endl;
            endOfToken = end;
        }
        t.tokenType = TokenTagPair;
        t.token = _gametext.substr(it, endOfToken - it);
        it = endOfToken;
    }
    
    /* The following tokens are self-terminating.  
     * We set the tokenType and token accordingly and increase
     * our "iterator." 
     */
      else if (c == '.') {
        t.tokenType = TokenPeriod;
        t.token = ".";
        it++;
    } else if (c == '(') {
        t.tokenType = TokenStartRAV;
        t.token = "(";
        it++;
    } else if (c == ')') {
        t.tokenType = TokenEndRAV;
        t.token = ")";
        it++;
    } else if (c == '{') {
        t.tokenType = TokenStartAnnotation;
        t.token = "{";
        it++;
    } else if (c == '}') {
        t.tokenType = TokenEndAnnotation;
        t.token = "}";
        it++;
    } else if (c == '[') {
        t.tokenType = TokenStartTag;
        t.token = "[";
        it++;
    } else if (c == ']') {
        t.tokenType = TokenEndTag;
        t.token = "]";
        it++;
    } else if (c == '*') {
        t.tokenType = TokenResult;
        t.token = "*";
        it++;
    }
    
    /* The remaining cases are moves, move numbers, and results.
     * The following code determines whether the first character
     * of the token is potentially a move or move number, and 
     * extends the token out to the first character which cannot
     * belong to that TokenType. 
     */
      else if (isstartofmove(c)) {
        size_t endOfToken = _gametext.find_first_not_of("RBNQKabcdefghx=+#!?O-12345678", it);
        if (endOfToken == string::npos) {
            endOfToken = end;
        }
        t.tokenType = TokenMove;
        t.token = _gametext.substr(it, endOfToken - it);
        it = endOfToken;
    } else if (isdigit(c)) {
        size_t endOfToken = _gametext.find_first_not_of("1234567890-/", it);
        if (endOfToken == string::npos) {
            endOfToken = end;
        }
        t.token = _gametext.substr(it, endOfToken - it);
        
        /* If t.token has a '-' in it, which means it's a castling move 
         * with a digit or a result.  Otherwise the token is a movenumber token.
         */
        if (t.token.find('-') != string::npos) {
            if ((t.token == "1-0") || (t.token == "0-1") || (t.token == "1/2-1/2")) {
                t.tokenType = TokenResult;
            } else if ((t.token == "0-0") || (t.token == "0-0-0")) {
                t.tokenType = TokenMove;
            } else {
                t.tokenType = TokenInvalid;
                cout << "TokenInvalid in PGNLexer::getNextToken() token with digit and '-'" << endl;
            }
        } else {
            t.tokenType = TokenInteger;
        }
        
        it = endOfToken;
    } else if (c == '$') {
        t.tokenType = TokenNAG;
        size_t endOfToken = _gametext.find_first_not_of("1234567890", it + 1);
        if (endOfToken == string::npos) {
            endOfToken = end;
        }
        t.token = _gametext.substr(it, endOfToken - it);
        it = endOfToken;
    } else {
        // This is an invalid token
        t.tokenType = TokenInvalid;
        
        size_t endOfToken = _gametext.find_first_of(" ", it);
        // Our string isn't found - should be an error
        if (endOfToken == string::npos) {
            cout << "Error in PGNLexer::getNextToken [TokenInvalid].  No ending \" \" ' found" << endl;
            endOfToken = end;
        }
        t.token = _gametext.substr(it, endOfToken - it);
        it = endOfToken;
    }

    
    lastTokenType = t.tokenType;
    
    return t;
    
}

/* Characters that can start a move token.  
 * 'R', 'B', 'N', 'Q', 'K' indicate pieces (for English SAN)
 * 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' indicate pawn moves
 * 'O' is the start of a castling move */
bool PGNLexer::isstartofmove(char c) {
    return strchr("RBNQKabcdefghO", c);
}

}