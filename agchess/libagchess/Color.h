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

#ifndef AGCHESS_COLOR_H
#define AGCHESS_COLOR_H

#include <string>
#include <ostream>

namespace AGChess {
    
    class Color {
     
    public:
        
        enum AGChessColorT {
            WhiteColor = 0,
            BlackColor = 1,
            NoColor = 2
        };
        
        Color();
        Color(AGChessColorT color);
        Color(char color);
        
        bool isValid() const;
        bool operator==(const Color& rhs) const;
        bool operator!=(const Color& rhs) const;
        
        operator std::string() const;
        
        unsigned char color_index() const;
        Color opposite() const;
        
        
    protected:
        unsigned char color_;
    };
    
    std::ostream& operator<<(std::ostream& out, const Color& color);
    
    const Color White = Color(Color::WhiteColor);
    const Color Black = Color(Color::BlackColor);
    
}

#endif