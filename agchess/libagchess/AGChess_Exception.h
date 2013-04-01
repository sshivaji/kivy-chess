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

#ifndef AGCHESS_EXCEPTION_H
#define AGCHESS_EXCEPTION_H

#include <exception>
#include <string>

namespace AGChess {
    /* Exception to be thrown if an instance of an invalid Square occurs. */
    class AGChess_Exception : public std::exception{
    
    public:
        AGChess_Exception(std::string error) throw() {
            what_ = new std::string(error);
        }
        
        ~AGChess_Exception() throw() {
            delete what_;
        }
        
        const char* what() const throw()
        {
            *what_ = "AGChess_Exception: " + *what_;
            return what_->c_str();
        }

    private:
        std::string *what_ ;
    }; 
}
#endif