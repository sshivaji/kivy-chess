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

#ifndef AGCHESS_DATABASE_FILTER_H
#define AGCHESS_DATABASE_FILTER_H

#include "PGNDatabase.h"
#include <vector>
#include <algorithm>
#include "SearchMask.h"

namespace AGChess {
    
    class DatabaseFilter {
      
    public:
        DatabaseFilter(PGNDatabase* database = NULL);
        int numberOfGames() const;
        const PGNDatabase* database() const;
        
        //void sort();
        void clear();
        void find(const SearchMask& searchMask);
        
        StandardChessGame getGame(int index) const;
        GameHeaders headers(int index) const;
        std::string getGameText(int index) const;
        
    protected:
        vector<int> indexList;
        bool filterSet;
        PGNDatabase* database_;
        
        void initializeIndexes();
    };
}

#endif