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


#ifndef AGCHESS_TAG_PAIR_H
#define AGCHESS_TAG_PAIR_H

#include <string>
#include <exception>
#include <iostream>
#include <vector>

namespace AGChess {

    enum TagPairType {
        TagPairTypeEvent,
        TagPairTypeSite,
        TagPairTypeDate,
        TagPairTypeRound,
        TagPairTypeWhite,
        TagPairTypeBlack,
        TagPairTypeResult,
        TagPairTypeOther,
        TagPairTypeInvalidTag
    };
    
    struct TagPair {
        std::string key;
        std::string value;
        TagPairType tpType;
    };
    
    TagPair tagPairFromString(const std::string& s);    
    const std::vector<std::string> SevenTagRoster();
    std::ostream& operator<<(std::ostream& out, const TagPair& tagPair);
}
    
#endif // TagPair_H