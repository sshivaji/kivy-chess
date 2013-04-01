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

#include "chess_iterator.h"
#include "AGChess_Exception.h"

namespace AGChess {

    chess_iterator::chess_iterator() {
        isValid_ = false;
    }
    
    chess_iterator::chess_iterator(GameTree::iterator begin) {
        nodes.push(chess_iterator_node(begin));
        nodes.top().popsOnIncrement = false;
        isValid_ = true;
    }
    
    chess_iterator& chess_iterator::operator=(GameTree::iterator rhs) {
        // clear stack
        while (!nodes.empty()) {
            nodes.pop();
        }
        nodes.push(chess_iterator_node(rhs));
        nodes.top().popsOnIncrement = false;
        isValid_ = true;
        
        return *this;
    }
    
    chess_iterator& chess_iterator::operator=(const chess_iterator& rhs) {
        if (this != &rhs) {
            *this = rhs.iterator();
        }
        
        return *this;
    }
    
    chess_iterator& chess_iterator::operator++() {
        
        /* If nodes is empty, we have gone through all the moves and the iterator is
         * no longer valid */
        if (nodes.empty()) {
            isValid_ = false;
            return *this;
        }
        
        chess_iterator_node& current = nodes.top();
        
        /* If we pop on increment, that means the current node is the first of a number of siblings,
         * and so we must visit the sibling nodes before continuing along the mainline */
        if (current.popsOnIncrement) {
            nodes.pop();
            ++(*this);
        } 
        
        /* If our position has no children, then we pop to the next place that had branching */
        else if (current.position.numberOfChildren() == 0) {
            nodes.pop();
            ++(*this);
        } 
        
        /* Note that reaching this point indicates that there must be at least one child node 
         * to visit, since otherwise we would have popped the current node due to the previous
         * conditional.  
         *
         * There first child (index 0) is a special case - if it has no siblings then we continue 
         * on normally, but if it has siblings then we must set popsOnIncrement = true. */
        else if (current.nextChildToVisit == 0) {
            // Create a new node with the next position to visit
            chess_iterator_node nextNode(current.position);
            ++nextNode.position;
            
            if (current.position.numberOfChildren() == 1) {
                nextNode.popsOnIncrement = false;
                nodes.pop();
            } else if (current.position.numberOfChildren() > 1) {
                nextNode.popsOnIncrement = true;
                ++current.nextChildToVisit;
                
            } else {
                throw AGChess_Exception("chess_iterator::operator++() nextChildToVisit == 0"
                                        "but current has no children.");
            }

            nodes.push(nextNode);
        }
        
        /* The current node had multiple children and has iterated through each of it's children.
         * Now it's time to revisit the first child and iterate over all its children. The current node
         * has exhausted its usefullness and will be popped from the stack. */
        else if (current.nextChildToVisit == current.position.numberOfChildren() ) {
            chess_iterator_node nextNode(current.position);
            ++nextNode.position;
            nextNode.popsOnIncrement = false;
            nodes.pop();
            nodes.push(nextNode);
            ++(*this);
        }
        
        /* The current node has multiple children and has not finished visiting them all. */
        else if ((current.nextChildToVisit > 0) && (current.nextChildToVisit < current.position.numberOfChildren())) {
            chess_iterator_node nextNode(current.position);
            nextNode.position+= (current.nextChildToVisit);
            nextNode.popsOnIncrement = false;
            ++current.nextChildToVisit;
            nodes.push(nextNode);
        }
        
        /* There shouldn' be any other cases, so throw an exception */
        else {
            std::cout << "Next child to visit: " << current.nextChildToVisit << std::endl;
            std::cout << "Number of children: " << current.position.numberOfChildren() << std::endl;
            throw AGChess_Exception("chess_iterator::operator++() unknown case reached");
        }
        
        return *this;
    }
    
    const StandardPosition& chess_iterator::operator*() const {
        if (!isValid()) {
            throw AGChess_Exception("chess_iterator::operator*() invalid iterator dereferenced.");
        }
        
        return *nodes.top().position;
    }
    
    bool chess_iterator::nextPopsVariation() const {
        return (nodes.top().position.numberOfChildren() == 0);
    }
    
    bool chess_iterator::nextPushesVariation() const {
        return nodes.top().popsOnIncrement;
    }
    
    bool chess_iterator::isValid() const {
        return isValid_;
    }
    
    const GameTree::iterator& chess_iterator::iterator() const {
        if (!isValid()) {
            throw AGChess_Exception("chess_iterator::iterator() invalid iterator position.");
        }
        
        return nodes.top().position;
    }

}