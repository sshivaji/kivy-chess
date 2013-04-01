/*
 *  Demo.cpp
 *  
 *
 *  Created by Austen Green on 2/9/11.
 *  Copyright 2011 Austen Green Consulting. All rights reserved.
 *
 */

#include "wrapper.h"

#include "libagchess/StandardPosition.h"
#include "libagchess/EditablePosition.h"
#include "libagchess/PGNDatabase.h"
#include "libagchess/FEN.h"
#include "libagchess/AGChess_Exception.h"
#include "libagchess/Move.h"
#include <iostream>


void testPosition() {
    using namespace AGChess;

    std::cout << "---------------Begin testPosition()-----------------------" << std::endl;
    
    StandardPosition position; // Creates a chess position from the standard starting position
                               // This object knows the rules of chess and throws an exception if
                               // You try to make an invalid move;
    
    basic_move m(e2, e4);      // e2, e4 are defined in Square.h
    
    position.make(m);          // Make the move
    std::cout << position;
    
    position.unmake(m);        // Undo the move
    std::cout << position;
    
    basic_move bad_move(d2, d5); // Not a legal move
    try {
        position.make(bad_move); // Throws an AGChess_Exception for an illegal move
    }
    catch (AGChess_Exception& e) {
        std::cout << "Tried to make an illegal move" << std::endl;
        std::cout << e.what() << std::endl;
    }
    
    std::cout << "-----------------End testPosition()-----------------------" << std::endl;
}

 extern "C" {
    using namespace AGChess;
    StandardPosition current_pos =  StandardPosition();
    void test_c_position() {
      testPosition();
    }
    
    void reset_current_pos() {
      current_pos =  StandardPosition();
    }
    
    void get_board() {
      cout << current_pos.board();
      
    }
    
    
}

void testFEN() {
    using namespace AGChess;
    
    std::cout << "---------------Begin testFEN()----------------------------" << std::endl;
    
    StandardPosition position; // Creates a chess position from the standard starting position
    std::string fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"; // Position after 1.e4 c5 2.Nf3
    
    EditablePosition editablePosition = positionFromFen(fen); // You can do what you'd like with this position...  
    // Here we'll change the black pawn on d7 to a black queen
    
    editablePosition.clear(d7);   // Clear the d7 square
    editablePosition.set(d7, BQ); // Place a black queen on d7
    
    position.copy(editablePosition);  // Copy the contents of the editable position into the standard position
    std::cout << position;
    
    // What about illegal positions?
    editablePosition.clear(d2);
    editablePosition.set(d2, BQ); // Now Black has the move, but White is in check, so this position is illegal
    
    try {
        position.copy(editablePosition); // Throws an AGChess_Exception for trying to commit an illegal position to a StandardPosition
    }
    catch (AGChess_Exception& e) {
        std::cout << "Tried to set up an illegal position" << std::endl;
        std::cout << e.what() << std::endl;
    }
    
    std::cout << "-----------------End testFEN()----------------------------" << std::endl;
    
}
