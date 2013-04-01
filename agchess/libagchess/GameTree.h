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


#ifndef AGCHESS_GAMETREE_H
#define AGCHESS_GAMETREE_H

#include "MoveTreeNode.h"
#include "StandardPosition.h"

namespace AGChess {
  
    class GameTree {
      
    public:
        GameTree();
        ~GameTree();
        GameTree(const GameTree& copy);
        GameTree& operator=(const GameTree& rhs);
        
        class iterator;
        
        /* Returns an iterator to the start position of the game */
        iterator begin() const;
        /* Returns an iterator to the end of the main line of the game */
        iterator end() const;
        /* Appends move as the last child move of position and returns
         * an iterator to the child position resulting from making the move
         * from position */
        iterator append(iterator position, Move move);
        /* Replaces all children of position with move and returns
         * an iterator to the child position resulting from making the move
         * from position */
        iterator replace(iterator position, Move move);
        /* Deletes all children of position */
        void erase(iterator position);
        
        const StandardPosition& startPosition() const {return startPosition_;}
        bool requiresSetUp() const {StandardPosition s;
                                    return s != startPosition_;}
        
    protected:
        StandardPosition make(const iterator& position, Move& move);
        
        StandardPosition startPosition_;
        MoveTreeNode* root;
        
    };
    
    class GameTree::iterator {
        friend class GameTree;
        
    public:
        iterator();
        iterator(const StandardPosition& position, MoveTreeNode* node);
        
        const StandardPosition& operator*() const;
        const Move& at(int index) const;
        const Move& parentMove() const;
        int numberOfChildren() const;
        
        iterator& next(int index = 0);
        iterator& previous();
        
        iterator& operator++();
        iterator  operator++(int);
        iterator& operator--();
        iterator  operator--(int);
        iterator& operator+=(int variation);
        bool      operator==(const iterator& rhs);
        bool      operator!=(const iterator& rhs);
        const StandardPosition* operator->();
        
        bool endOfLine() const;
        int parentIndex() const;
        
    private:
        StandardPosition position_;
        MoveTreeNode* node_;
        
    };
    
};

#endif