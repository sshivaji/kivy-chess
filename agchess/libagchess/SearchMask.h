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
 
 SearchMask.h - Abstract base class for searching a PGNDatabase
 
 */

#ifndef AGCHESS_SEARCH_MASK_H
#define AGCHESS_SEARCH_MASK_H

#include "PGNDatabase.h"

namespace AGChess {
    
    /*!
    @class
    @abstract    Abstract base class for searching a PGNDatabase
    @discussion  A SearchMask object binds to a database and implements the () operator for 
     an integral index, and should return true if database->getGame(index) matches the
     search mask.  The SearchMask is used by a DatabaseFilter object to find all games in a 
     database which match the SearchMask.
     */

    class SearchMask {
    public:
        SearchMask(PGNDatabase* database = NULL);
        PGNDatabase* database() const;
        
        virtual bool operator() (int index) const = 0;
        
    protected:
        PGNDatabase* database_;
    };
}

#endif