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


#include "GameTree.h"

namespace AGChess {

#pragma mark GameTree
    
    GameTree::GameTree() {
        root = new MoveTreeNode;
    }
    
    GameTree::~GameTree() {
        delete root;
    }
    
    GameTree::GameTree(const GameTree& copy) {
        root = new MoveTreeNode(*copy.root);
        root->parent = NULL;
        startPosition_ = copy.startPosition_;
    }
    
    GameTree& GameTree::operator=(const GameTree& rhs) {
        if (this != &rhs) {
            delete root;
            root = new MoveTreeNode(*rhs.root);
            root->parent = NULL;
            startPosition_ = rhs.startPosition_;
        }
        return *this;
    }
    
    GameTree::iterator GameTree::begin() const {
        return iterator (startPosition_, root);
    }
    
    GameTree::iterator GameTree::end() const {
        GameTree::iterator i = begin();
        for (i; !i.endOfLine(); i.next()) {
            
        }
        return i;
    }
    
    GameTree::iterator GameTree::append(iterator position, Move move) {
        StandardPosition p = make(position, move); // Attempt to make the move, throw exception if move is invalid
        
        // Create a new child node
        MoveTreeNode *tmp = position.node_; 
        MoveTreeNode* newChild = new MoveTreeNode();
        newChild->move = move;
        newChild->parent = tmp;
        
        // Add the child node to the end of the current node's move list
        tmp->children.push_back(newChild);
        
        return GameTree::iterator(p, newChild);
    }
    
    GameTree::iterator GameTree::replace(iterator position, Move move) {
        StandardPosition p = make(position, move);  // Attempt to make the move
        
        // Create a new child node
        MoveTreeNode *tmp = position.node_;
        MoveTreeNode *newChild = new MoveTreeNode();
        newChild->move = move;
        newChild->parent = tmp;
        
        // Clear the current node's move list and replace it with newChild
        tmp->children.clear();
        tmp->children.push_back(newChild);
        
        return GameTree::iterator(p, newChild);
    }
    
    void GameTree::erase(iterator position) {
        position.node_->children.clear();
    }
    
    StandardPosition GameTree::make(const iterator& position, Move& move) {
        StandardPosition p = *position;
        try {
            p.make(move);
        }
        catch (AGChess_Exception& e) {
            throw AGChess_Exception("GameTree::make illegal move for position");
        }
        return p;
    }
    
#pragma mark -
#pragma mark iterator
    
    GameTree::iterator::iterator() {
        node_ = NULL;
    }
    
    GameTree::iterator::iterator(const StandardPosition& position, MoveTreeNode* node) {
        position_ = position;
        node_ = node;
    }
    
    const StandardPosition& GameTree::iterator::operator*() const {
        return position_;
    }
    
    GameTree::iterator& GameTree::iterator::operator++() {
        next(0);
        return *this;
    }
    
    GameTree::iterator  GameTree::iterator::operator++(int) {
        GameTree::iterator ret = *this;
        next(0);
        return ret;
    }
    
    GameTree::iterator& GameTree::iterator::operator--() {
        previous();
        return *this;
    }
    
    GameTree::iterator GameTree::iterator::operator--(int) {
        GameTree::iterator ret = *this;
        next(0);
        return ret;
    }
    
    GameTree::iterator& GameTree::iterator::operator+=(int variation) {
        next(variation);
        return *this;
    }
    
    bool GameTree::iterator::operator==(const GameTree::iterator& rhs) {
        return (node_ == rhs.node_) &&
        (position_ == rhs.position_);
    }
    
    bool GameTree::iterator::operator!=(const GameTree::iterator& rhs) {
        return (node_ != rhs.node_) ||
        (position_ != rhs.position_);
    }
    
    const StandardPosition* GameTree::iterator::operator->() {
        return &position_;
    }
    
    const Move& GameTree::iterator::at(int index) const {
        MoveTreeNode *tmp = node_->children.at(index);
        return tmp->move;
    }
    
    const Move& GameTree::iterator::parentMove() const {
        int index = parentIndex();
        return node_->parent->children.at(index)->move;
    }
    
    GameTree::iterator& GameTree::iterator::next(int index) {
        MoveTreeNode *tmp = node_->children.at(index); // Redundant use of code
        position_.make(tmp->move);
        node_ = tmp;
        return *this;
    }
    
    GameTree::iterator& GameTree::iterator::previous() {
        MoveTreeNode *tmp = node_->parent; // Redundant use of code
        position_.unmake(node_->move);
        node_ = tmp;
        return *this;
    }
    
    int GameTree::iterator::numberOfChildren() const {
        return node_->children.size();
    }
    
    bool GameTree::iterator::endOfLine() const {
        return node_->children.empty();
    }
    
    int GameTree::iterator::parentIndex() const {
        if (node_->parent == NULL) {
            throw AGChess_Exception("GameTree::iterator::parentIndex() iterator position has NULL parent");
        }
        
        std::vector<MoveTreeNode*>& children = node_->parent->children;
        int i;
        
        for (i = 0; children.at(i) != node_; ++i);
        return i;
        
    }
};