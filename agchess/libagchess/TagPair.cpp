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


#include "TagPair.h"

namespace AGChess {
    
    TagPair tagPairFromString(const std::string& s)
    {
        TagPair tp;
        
        try {
            size_t first, last;
            
            first = 0;
            last = s.find_first_of(' ', 0);
            tp.key =  s.substr(first, last);
            
            first = s.find_first_of('"');
            last = s.find_last_of('"');
            tp.value = s.substr(first + 1, last - (first + 1));
            
            if (tp.key == "Event") tp.tpType = TagPairTypeEvent;
            else if (tp.key == "Site") tp.tpType = TagPairTypeSite;
            else if (tp.key == "Date") tp.tpType = TagPairTypeDate;
            else if (tp.key == "Round") tp.tpType = TagPairTypeRound;
            else if (tp.key == "White") tp.tpType = TagPairTypeWhite;
            else if (tp.key == "Black") tp.tpType = TagPairTypeBlack;
            else if (tp.key == "Result") tp.tpType = TagPairTypeResult;
            else tp.tpType = TagPairTypeOther;
            
        }
        catch (...) {
            tp.tpType = TagPairTypeInvalidTag;
            tp.key = "-";
            tp.value = "";
        }
        
        return tp;
    }
    
    
    const std::vector<std::string> SevenTagRoster() {
        std::vector<std::string> STR;
        STR.push_back("Event");
        STR.push_back("Site");
        STR.push_back("Date");
        STR.push_back("Round");
        STR.push_back("White");
        STR.push_back("Black");
        STR.push_back("Result");
        return STR;
    }
    
    std::ostream& operator<<(std::ostream& out, const TagPair& tagPair) {
        out << "[" << tagPair.key << " \"" << tagPair.value << "\"]";
        return out;
    }  
}