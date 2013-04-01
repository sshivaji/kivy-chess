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

#ifndef AGCHESS_CHESS_ITERATOR_H
#define AGCHESS_CHESS_ITERATOR_H

#include "GameTree.h"
#include <stack>

namespace AGChess {

    struct chess_iterator_node {
        
        chess_iterator_node(const GameTree::iterator& iter) : position(iter) {
            nextChildToVisit = 0;
        }
        
        GameTree::iterator position;
        int nextChildToVisit;
        bool popsOnIncrement;
    };
    
    /*!
    @class
    @abstract    An iterator which visits each node in a GameTree
    @discussion  A chess_iterator behaves like a forward iterator which
     visits each node in a GameTree.
     */

    
    class chess_iterator {
    public:
        
        chess_iterator();
        chess_iterator(GameTree::iterator begin);
        chess_iterator& operator=(GameTree::iterator rhs);
        chess_iterator& operator=(const chess_iterator& rhs);
        chess_iterator& operator++();
        const StandardPosition& operator*() const;
        
        const GameTree::iterator& iterator() const;
        
        bool nextPushesVariation() const;
        bool nextPopsVariation() const;
        bool isValid() const;
        
    private:
        std::stack<chess_iterator_node> nodes;
        bool isValid_;
    };
    
}

#endif