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


#include "PGNDatabase.h"
#include "PGNLexer.h"

namespace AGChess {

    PGNDatabase::PGNDatabase(const char* filepath) {
        initWithFile(filepath);
    }
    
    PGNDatabase::PGNDatabase(const std::string& filepath) {
        initWithFile(filepath.c_str());
    }
    
    void PGNDatabase::initWithFile(const char* file) {
        database.open(file);
        
        if (database.is_open()) {
            initializeGameIndexes();
        } else {
            std::string except = "PGNDatabase::initWithFile() Unable to open ";
            except += file;
            throw AGChess_Exception(except);
        }

    }
    
    PGNDatabase::~PGNDatabase() {
        
    }
    
#pragma mark -
#pragma mark Public Interface
    
    int PGNDatabase::numberOfGames() const {
        return numGames;
    }
    
    GameHeaders PGNDatabase::headers(int index) const {
        GameHeaders headers_;
        PGNLexer lexer(getGameText(index), true); // Process header only
        
        const std::vector<Token>& tokens = lexer.tokens();
        
        for (vector<Token>::const_iterator i = tokens.begin(); i!= tokens.end(); i++) {
            
            if (i->tokenType == TokenTagPair) {
                headers_.setTagPair(tagPairFromString(i->token));
            }
        }
            
        return headers_;
    }
    
    /* Returns the game string for index */
    StandardChessGame PGNDatabase::getGame(int index) const {
        string gameText = getGameText(index);
        return StandardChessGame(gameText);
        
    }
    
    string PGNDatabase::getGameText(int index) const
    {
        unsigned long start, end;
        start = gameIndexes.at(index);
        string game;
        
        if (index != numGames-1) {
            end = gameIndexes.at(index + 1) -1;  
            // subtract one to get the last character in the 
            // requested game
        } else {
            database.seekg(0, ios_base::end);
            end = database.tellg();		
        }
        
        database.clear();
        database.seekg(start, ios_base::beg);
        char memblock[end - start +1];
        database.read(memblock, end - start);
        memblock[end - start] = '\0';
        game += memblock;
        
        return game;
    }
    
#pragma mark - 
#pragma mark Database Initialization
    
    void PGNDatabase::initializeGameIndexes() {
        numGames = 0;
        char buffer[256];
        unsigned long offset = 0;
        bool logNextBracket = true;
        bool countNextLinebreak = false;
        int lineBreakCount = 0;
        
        while(!database.eof())
        {
            // Resets failbit - only needed if the PGN file doesn't meet
            // specifications (line length over 80 [121 implemented] characters)
            if (database.fail() && !database.eof()) {
                database.clear();
            }
            
            database.getline(buffer, 255);
            char c = buffer[0];
            
            // The first '[' marks the start of the game
            /* Assumption: Every game starts with at least one
             * Tag Pair */
            if (logNextBracket && (c == '[')) {
                logNextBracket = false;
                offset = (unsigned long)database.tellg() - (strlen(buffer) + 1);
                gameIndexes.push_back(offset);
                numGames++;
                countNextLinebreak = true;
                //cout << "Logging bracket at: " << offset << endl;
                // offset is equal to the current position minus the length
                // of the string that was just read (+ 1 more character for the newline)
            } 
            
            /* We ignore all brackets that don't appear at the beginning of the game
             * This method is here for debugging purposes only */
            /*
             else if (!logNextBracket && (c== '[')) {
             //cout << "Unlogged bracket: " << buffer << endl;
             }
             */
            
            /* Count the number of linebreak sections - there should be two per game:
             * One after the Tag Pair, and one following the Movetext */
            else if (countNextLinebreak && (!isprint(c))) {
                //cout << "non-printing line" << endl;
                lineBreakCount ++;
                countNextLinebreak = false;
                if (lineBreakCount == 2) {
                    //cout << "setting log next bracket: " << buffer << endl;
                    lineBreakCount = 0;
                    logNextBracket = true;
                }
            } 
            
            /* This isn't supposed to happen - PGN standards call for
             * no spaces as the starting character of a line.  We check 
             * for it anyway */
            else if (countNextLinebreak && (c == ' ')) {
                bool lineIsEmpty = true;
                
                /* Determine whether a line that starts with a ' ' is empty
                 * or contains relevent data. */
                if (c == ' ') {
                    for (int j = 0; j < strlen(buffer); j++) {
                        if (!isstartempty(buffer[j])) {
                            //cout << "Found space-began line: " << endl;
                            lineIsEmpty = false;
                            break;
                        }
                    }
                } 
                
                /* Processed as a linebreak */
                if (lineIsEmpty) {
                    //cout << "non-printing line" << endl;
                    lineBreakCount ++;
                    countNextLinebreak = false;
                    if (lineBreakCount == 2) {
                        //cout << "setting log next bracket: " << buffer << endl;
                        lineBreakCount = 0;
                        logNextBracket = true;
                    }                
                } 
                /* Processed as a non-empty line */
                else {
                    //cout << "Count next line break: " << buffer <<  endl;
                    countNextLinebreak = true;
                }
            }
            /* Process non-empty lines */
            else if (logNextBracket == false && (isprint(c))
                     && (c != '[')) {
                //cout << "Count next line break: " << buffer <<  endl;
                countNextLinebreak = true;
            }
        }
        
        
        /* Clear the failbit and push the eof as the last index
         * if it's not the last index already */
        database.clear();
        offset = database.tellg();
        
        if (gameIndexes.back() != offset) {
            gameIndexes.push_back(offset);
        }
        
        cout << "Last offset: " << offset <<  endl;
        cout << "Initialized indexes. " << numGames << " in current db." << endl;
    }
    
    /* An empty line can start with a non-printing character
     * i.e. a '\n' or '\r' or '\0', or can be a ' '.
     */
    bool PGNDatabase::isstartempty(char c) {
        return (!isprint(c) || (c == ' '));
    }
    
}