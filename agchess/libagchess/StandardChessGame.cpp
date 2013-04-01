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


#include "StandardChessGame.h"
#include "PGNLexer.h"
#include "SAN.h"
#include "TagPair.h"
#include "FEN.h"
#include <stack>

namespace AGChess {

    StandardChessGame::StandardChessGame() {
        
    }
    
    StandardChessGame::StandardChessGame(const std::string& gameText) {
        GameTree::iterator pos = begin();
        PGNLexer lexer(gameText);
        std::stack<GameTree::iterator> positionStack;
        
        bool requiresSetup = false;
        
        const std::vector<Token>& tokens = lexer.tokens();
        
        for (vector<Token>::const_iterator i = tokens.begin(); i!= tokens.end(); i++) {
            
            if (i->tokenType == TokenMove) {
                // Append a move token to the tree
                try {
                    Move m = SanToMove(i->token, *pos);
                    pos = append(pos, SanToMove(i->token, *pos));
                }
                catch (AGChess_Exception& e) {
                    std::cout << "AGChess_Exception caught" << std::endl;
                    std::cout << e.what() << std::endl;
                    std::cout << "Move: " << i->token << std::endl;
                    std::cout << *pos;
                    throw e;
                }
                
            } else if (i->tokenType == TokenStartRAV) {
                // Start of variation - go to previous position, save current position 
                // on the stack
                positionStack.push(pos);
                pos.previous();
            } else if (i->tokenType == TokenEndRAV) {
                // End of variation - go back to previous position on the stack
                pos = positionStack.top();
                positionStack.pop();
            } else if (i->tokenType == TokenAnnotationText) {
                // Assumes that all annotations follow a move, therefore append the 
                // annotation to the move that resulted in the current position.
                try {
                    int index = pos.parentIndex();
                    pos.previous();
                    pos.at(index).setComment(i->token);
                    pos.next(index);                    
                }
                catch (AGChess_Exception& e) {
                    //std::cout << e.what();
                }
            } else if (i->tokenType == TokenTagPair) {
                TagPair tagPair = tagPairFromString(i->token);
                setTagPair(tagPair);
                
                // Handle FEN
                if ((tagPair.key == "SetUp") && (tagPair.value == "1")) requiresSetup = true;
                if ((tagPair.key == "FEN") && requiresSetup) {
                    EditablePosition e = positionFromFen(tagPair.value);
                    startPosition_.copy(e);
                    std::cout << "Initialized game with FEN position" << std::endl;
                }
            } else if (i->tokenType == TokenInvalid) {
                // Consider a null move.  A null move is not technically part of the
                // PGN Standard, but is widely used, so we'll allow it.
                if (i->token == "--") {
                    // This is a null move;
                    try {
                        Move m = SanToMove(i->token, *pos);
                        pos = append(pos, SanToMove(i->token, *pos));
                    }
                    catch (AGChess_Exception& e) {
                        std::cout << "AGChess_Exception caught" << std::endl;
                        std::cout << e.what() << std::endl;
                        std::cout << "Move: " << i->token << std::endl;
                        std::cout << *pos;
                        throw e;
                    }
                }
            }
        }
    }
}