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


#include "SimpleGame.h"

namespace AGChess {

    SimpleGame::SimpleGame() {
        iter = 0;
    }
    
    SimpleGame::SimpleGame(const StandardPosition& startPosition) {
        position_ = startPosition;
        iter = 0;
    }
    
    Move& SimpleGame::next() {
        position_.make(moveList_.at(iter));
        ++iter;
        return moveList_.at(iter -1);
    }
    
    Move& SimpleGame::previous() {
        --iter;
        position_.unmake(moveList_.at(iter));
        return moveList_.at(iter);
    }
    
    void SimpleGame::insert(const Move& move) {
        Move tmp = move;
        position_.make(tmp);
        
        // Erase remaining moves if not at the end of the game
        if (!endOfGame()) {
            moveList_.erase(moveList_.begin() + iter + 1, moveList_.end());
        }
        
        if (!moveList_.empty()) {
            ++iter;   
        }
        
        moveList_.push_back(tmp);
        
    }
    
    void SimpleGame::begin() {
        if (startOfGame()) return;
        
        for (int i = iter; i >= 0; i--) {
            position_.unmake(moveList_.at(i));
        }
        iter = 0;
        
    }
    
    void SimpleGame::end() {
        if (endOfGame()) return;
        
        for (int i = iter; i < moveList_.size(); i++) {
            position_.make(moveList_.at(i));
        }
        iter = moveList_.size() - 1;
    }
    
    bool SimpleGame::startOfGame() const {
        return iter == 0;
    }
    
    bool SimpleGame::endOfGame() const {
        if (moveList_.empty()) return true;
        
        return iter == moveList_.size() - 1;
    }
};