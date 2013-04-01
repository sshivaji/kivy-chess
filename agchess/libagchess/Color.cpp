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

#include "Color.h"
#include "AGChess_Exception.h"

namespace AGChess {

    Color::Color() {
        color_ = 2;
    }
    
    Color::Color(AGChessColorT color) {
        if ((color != WhiteColor) && (color != BlackColor)) {
            color_ = NoColor;
        } else {
            color_ = color;
        }
    }
    
    Color::Color(char color) {
        if ((color == 'W') || (color == 'w')) {
            color_ = WhiteColor;
        } else if ((color == 'B') || (color == 'b')) {
            color_ = BlackColor;
        } else {
            color_ = NoColor;
        }
    }
    
    bool Color::isValid() const {
        return color_ != 2;
    }
    
    bool Color::operator==(const Color& rhs) const {
        return color_ == rhs.color_;
    }
    
    bool Color::operator!=(const Color& rhs) const {
        return color_ != rhs.color_;
    }
    
    Color Color::opposite() const {
        return Color(AGChessColorT(1 - color_));
    }
    
    unsigned char Color::color_index() const {
        if (!isValid()) {
            throw AGChess_Exception("Color::color_index() NoColor has no index");
        }
        return color_;
    }
    
    Color::operator std::string() const {
        if (color_ == 0) {
            return "White";
        } else if (color_ == 1) {
            return "Black";
        } else {
            return "NoColor";
        }
    }
    
    std::ostream& operator<<(std::ostream& out, const Color& color) {
        out << std::string(color);
        return out;
    }
}