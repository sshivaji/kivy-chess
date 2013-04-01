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

#include "DatabaseFilter.h"

namespace AGChess {

    DatabaseFilter::DatabaseFilter(PGNDatabase *database) {
        database_ = database;
        filterSet = false;
    }
    
    int DatabaseFilter::numberOfGames() const {
        if (filterSet) {
            return indexList.size();
        } else {
            return database()->numberOfGames();
        }
    }
    
    const PGNDatabase* DatabaseFilter::database() const {
        return database_;
    }
    
    StandardChessGame DatabaseFilter::getGame(int index) const {
        if (filterSet) {
            return database()->getGame(indexList.at(index));
        } else {
            return database()->getGame(index);
        }
    }

    GameHeaders DatabaseFilter::headers(int index) const {
        if (filterSet) {
            return database()->headers(indexList.at(index));
        } else {
            return database()->headers(index);
        }
    }
    
    std::string DatabaseFilter::getGameText(int index) const {
        if (filterSet) {
            return database()->getGameText(indexList.at(index));
        } else {
            return database()->getGameText(index);
        }
    }
    
#pragma mark -
#pragma mark Search and Sorting
    
    void DatabaseFilter::clear() {
        if (filterSet) {
            filterSet = false;
            indexList.clear();
        }
    }
    
    void DatabaseFilter::initializeIndexes() {
        if (!filterSet) {
            int count = numberOfGames();
            indexList.reserve(count);
            for (int i = 0; i < count; ++i) {
                indexList.push_back(count);
            }
            filterSet = true;
        }
    }
    
    // Doesn't allow chaining of finds - must find everything in one go
    // Clears the filter before performing the find.
    void DatabaseFilter::find(const SearchMask& searchMask) {
        clear();
        
        for (int i = 0; i < numberOfGames(); ++i) {
            if (searchMask(i) == true) {
                indexList.push_back(i);
            }
        }
        
        filterSet = true;
    }
}