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


#include "GameHeaders.h"
#include "AGChess_Exception.h"

namespace AGChess {

    GameHeaders::GameHeaders() {
        headers_.reserve(7);
        
        TagPair tp;
        tp.value = "";
        
        tp.key = "Event";
        tp.tpType = TagPairTypeEvent;
        headers_.push_back(tp);
        
        tp.key = "Site";
        tp.tpType = TagPairTypeSite;
        headers_.push_back(tp);
        
        tp.key = "Date";
        tp.tpType = TagPairTypeDate;
        headers_.push_back(tp);
        
        tp.key = "Round";
        tp.tpType = TagPairTypeRound;
        headers_.push_back(tp);
        
        tp.key = "White";
        tp.tpType = TagPairTypeWhite;
        headers_.push_back(tp);
        
        tp.key = "Black";
        tp.tpType = TagPairTypeBlack;
        headers_.push_back(tp);
        
        tp.key = "Result";
        tp.tpType = TagPairTypeResult;
        headers_.push_back(tp);
    }
    
    const vector<TagPair>& GameHeaders::headers() const {
        return headers_;
    }
    
    std::string GameHeaders::headerForTag(const std::string& tag) const {
        int i = indexOf(tag);
        
        if (i != -1) {
            return headers_.at(i).value;
        } else {
            return "";
        }
    }
    
    const string& GameHeaders::headerForTagPairType(TagPairType tagPairType) const {
        int index = indexOf(tagPairType);
        
        if (index == -1) {
            throw AGChess_Exception("GameHeaders::headerForTagPairType tagPairType is not "
                                    "one of the Seven Tag Roster.");
        } else {
            return headers_.at(index).value;
        }
    }

    
    void GameHeaders::setHeaderForTag(const std::string& header, const std::string& tag) {
        int i = indexOf(tag);
        
        if (i != -1) {
            headers_.at(i).value = header;
        } else {
            TagPair tagPair;
            tagPair.key = tag;
            tagPair.value = header;
            tagPair.tpType = TagPairTypeOther;
            headers_.push_back(tagPair);
        }
    }
    
    void GameHeaders::setTagPair(const TagPair& tagPair) {
        if (tagPair.tpType == TagPairTypeOther) {
            setHeaderForTag(tagPair.value, tagPair.key);
        } else if (tagPair.tpType == TagPairTypeInvalidTag) {
            throw AGChess_Exception("GameHeaders::setTagPair invalid tag type.");
        } else {
            int index = indexOf(tagPair.tpType);
            headers_.at(index).value = tagPair.value;
        }
    }
    
    int GameHeaders::indexOf(const string& tag) const {
        for (int i = 0; i < headers_.size(); i++) {
            if (headers_.at(i).key == tag) {
                return i;
            }
        }
        return -1;
    }
    
    std::vector<TagPair> GameHeaders::SevenTagRoster() const {
        std::vector<TagPair> sevenTagRoster;
        sevenTagRoster.assign(headers_.begin(), headers_.begin() + 7);
        
        return sevenTagRoster;
    }    
    
    int GameHeaders::indexOf(TagPairType tagPairType) const {
        int index;
        switch (tagPairType) {
            case TagPairTypeEvent:
                index = 0;
                break;
            case TagPairTypeSite:
                index = 1;
                break;
            case TagPairTypeDate:
                index = 2;
                break;
            case TagPairTypeRound:
                index = 3;
                break;
            case TagPairTypeWhite:
                index = 4;
                break;
            case TagPairTypeBlack:
                index = 5;
                break;
            case TagPairTypeResult:
                index = 6;
                break;
            default:
                index = -1;
                break;
        }
        return index;
    }
    
    ostream& operator<<(ostream& out, const GameHeaders& gameHeaders) {
        const vector<TagPair>& headers = gameHeaders.headers();
        vector<TagPair>::const_iterator i;
        
        for (i = headers.begin(); i != headers.end(); ++i) {
            out << *i << std::endl;
        }
        
        return out;
    }
};