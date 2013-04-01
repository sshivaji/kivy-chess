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

#ifndef AGCHESS_GAME_HEADERS_H
#define AGCHESS_GAME_HEADERS_H

#include <string>
#include <map>
#include <vector>
#include "TagPair.h"
#include <iostream>

namespace AGChess {
    
    using namespace std;
    
    class GameHeaders {
    public:
        GameHeaders();
        
        const vector<TagPair>& headers() const;
        vector<TagPair> SevenTagRoster() const;
        
        string headerForTag(const string& tag) const;
        const string& headerForTagPairType(TagPairType tagPairType) const;
        
        void setHeaderForTag(const string& header, const string& tag);
        void setTagPair(const TagPair& tagPair);
        
        int indexOf(const string& tag) const;
        
    protected:
        vector<TagPair> headers_;
        
        int indexOf(TagPairType tagPairType) const;
        
    };
    
    ostream& operator<<(ostream& out, const GameHeaders& gameHeaders);
}

#endif