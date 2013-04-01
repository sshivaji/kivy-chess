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


#ifndef AGCHESS_MOVETREENODE_H
#define AGCHESS_MOVETREENODE_H

#include "Move.h"
#include <vector>

namespace AGChess {

    class MoveTreeNode {
        
    public:
        MoveTreeNode() {
            parent = NULL;
        }
        
        MoveTreeNode(const Move& move_, MoveTreeNode* parent_) {
            move = move_;
            parent = parent_;
        }
        
        ~MoveTreeNode() {
            for (std::vector<MoveTreeNode*>::iterator i = children.begin(); i!=children.end(); i++) {
                delete *i;
                *i = NULL;
            }
        }
        
        MoveTreeNode& operator=(const MoveTreeNode& rhs) {
            
            if (this != &rhs) {
                // Delete current children
                for (std::vector<MoveTreeNode*>::iterator i = children.begin(); i!=children.end(); i++) {
                    delete *i;
                    *i = NULL;
                }
                
                move = rhs.move;
                
                for (std::vector<MoveTreeNode*>::const_iterator i = rhs.children.begin(); 
                     i!=rhs.children.end(); i++) {
                    MoveTreeNode* tmp = new MoveTreeNode(*(*i));
                    tmp->parent = this;
                    children.push_back(tmp);
                }
            }
            
            return *this;
        }
        
        MoveTreeNode(const MoveTreeNode& copy) {
            move = copy.move;
            
            for (std::vector<MoveTreeNode*>::const_iterator i = copy.children.begin(); 
                 i!=copy.children.end(); i++) {
                MoveTreeNode* tmp = new MoveTreeNode(*(*i));
                tmp->parent = this;
                children.push_back(tmp);
            }
        }
        
        Move move;
        std::vector<MoveTreeNode*>children;
        MoveTreeNode* parent;
        
    };
    
}

#endif