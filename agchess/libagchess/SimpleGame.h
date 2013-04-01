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


#include "StandardPosition.h"
#include <vector>

namespace AGChess {

    /*!
    @class
    @abstract    A chess Game which has a single main line and no branching variations.
    @discussion  A SimpleGame object is a Game in which there may only be a single 
                 main line of moves and no variations.  A SimpleGame can be thought of 
                 as the kind of game that would be entered if one were to play straight
                 through a single game without stopping to look at any variations.
     */

    class SimpleGame {
        
        typedef std::vector<Move> SimpleGameMoveList;
        
    public:
        SimpleGame();
        SimpleGame(const StandardPosition& startPosition);
        
        Move&     next();
        Move&     previous();
        void      begin();
        void      end();
        
        void insert(const Move& move);
        
        const StandardPosition& position() const {return position_;}
        bool  startOfGame() const;
        bool  endOfGame() const;
        
    private:
        StandardPosition position_;
        SimpleGameMoveList moveList_;
        int iter;  // Just an index right now - I didn't feel like playing around with iterators
        
    };
  
};