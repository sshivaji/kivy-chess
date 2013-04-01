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


#include "StandardPosition.h"
#include "Bitboard_MoveGen.h"
#include "Board_MoveGen.h"

namespace AGChess {

    /*
     * There are five layers of validation which occur in the make process:
     * 1. That the Position is in a consistent state.  A Standard_Position
     *    is designed so that the only inconsistency in its state can occur
     *    when 
     * 2. That the Move itself represents a valid move object.  That is,
     *    the source and destination squares are both unique and are
     *    on the chessboard.
     * 3. That there is, in fact, a piece on the source square and it is
     *    the same Color as the side to move.
     * 4. That the move is pseudo-legal.  A move which is pseudo-legal is
     *    one which is legal in the absence of any restrictions that
     *    the king is not in check.
     * 5. Finally, make sure that the move does not leave the king in check.
     *    This is currently
     */
    void StandardPosition::make(basic_move& move) {
        if (requires_promotion()) throw AGChess_Exception("Standard_Position::make() Unpromoted pawn before move.");
        if (!isPseudoLegal(move)) {
            if (move.isNull()) {
                makeSaveState(move);
                setSideToMove(sideToMove().opposite());  // Switch side to move
                setPly(ply() + 1);
                setHalfmoveClock(halfmoveClock() + 1);
                
                /* See if the side that just moved is in check.  If it is, unmake the move and throw
                 * an illegal move exception. */
                if (inCheck(sideToMove().opposite())) {
                    unmake(move);
                    throw AGChess_Exception("Standard_Position::make() King left in check.");
                }
                return;
            } else {
                throw AGChess_Exception("Standard_Position::make() Move is not pseudo-legal.");
            }
        }
        
        Square          from = move.from();
        Square          to   = move.to();
        ColoredPiece    p    = at(from);
        Piece           pt   = p.piece();
        
        /* Save state information */
        makeSaveState(move);
        
        /* Reset the en passant square if the moving piece isn't a pawn.  If it is a pawn,
         * it will be set by makePawnMove(). */
        if (pt != Pawn) {setEpSquare(InvalidSquare);}

        /* If piece moving is a king, then adjust castling rights or castle */
        if (pt == King) {makeKingMove(move);}
        
        /* If piece moving is a rook, then adjust castling rights */
        else if (pt == Rook) {makeRookMove(move);}
        
        /* If piece moving is a pawn, then adjust for promotion, en passant captures, and 
         * setting the en passant square if the move is a pawn push by two squares */
        else if (pt == Pawn) {makePawnMove(move);}
                
        /* Move the piece from the source square to the destination square */
        /* Regardless of the special nature of the move (castling, promotion, ep capture),
         * a piece always moves from the source to the destination square */
        /* Save captured piece information.  If the move was an en passant capture, it has
         * already been saved in makePawnMove(). Requires an if statement since there will
         * not be a piece on the destination square if the move is an en passant capture */
        if (at(to) != NoColoredPiece) {
            move.setCapturedPiece(at(to));
            move.setCapturedSquare(to);
            move.setIsCapture(true);
        }
        
        board_.move(from, to);
        setSideToMove(sideToMove().opposite());  // Switch side to move
        setPly(ply() + 1);
        
        setHalfmoveClock(halfmoveClock() + 1);
        
        if (move.isCapture() || (at(to).piece() == Pawn))
            setHalfmoveClock(0); // Reset halfmove clock for captures and pawn moves
        
        /* Promote immediately if the move has a promoted piece. */
        if (move.isPromotion() && move.promotionPiece().isPiece()) {
          try {
              promote(move.promotionPiece());
          }
          catch (AGChess_Exception & e) {
              std::cout << e.what() << std::endl;
          }
        }
        
        /* See if the side that just moved is in check.  If it is, unmake the move and throw
         * an illegal move exception. */
        if (inCheck(sideToMove().opposite())) {
            unmake(move);
            throw AGChess_Exception("Standard_Position::make() King left in check.");
        }
    }
    
    /* Undoes a move.  Unmake should be called with the most recent move first.  Subsequent calls
     * to unmake() should be pass the moves made by make() in a stack order.  Calling unmake() in 
     * any other order can leave the Position in an illegal state.  This method checks to see if 
     * move is a valid move and throws an AGChess_Exception if the move is invalid. 
     */
    void StandardPosition::unmake(const basic_move& move) {
        if (move.isValid() == false) {
            if (move.isNull()) {
                unmakeSaveState(move);
                return;
            } else {
                throw AGChess_Exception("Standard_Position::unmake() invalid move");
            }
        }
        
        Square from = move.from();
        Square to   = move.to();
        
        if (move.isPromotion()) {
            Color c = at(to).color();
            board_.set(to, ColoredPiece(c, Pawn));
        }
        
        if (move.isCastle()) {
            unmakeCastle(move);
        }
        
        unmakeSaveState(move);
        
        board_.move(to, from); // Reverse move
        
        /* Replace captured piece */
        if (move.isCapture()) {
            board_.set(move.capturedSquare(), move.capturedPiece());
        }
    }
    
#pragma mark -
#pragma mark Queries on basic_move
    
    bool StandardPosition::isCastle(const basic_move& move) const {
        if ((pseudoLegalCastle(sideToMove()) & squareBB(move.to())) == 0) return false;
        else {return true;}
    }
    
    /* Preconditions: Move is valid and the moving piece is a pawn */
    bool StandardPosition::isEnPassantCapture(const basic_move& move) const {
        Square from = move.from();
        Square to   = move.to();
       
        if (to != epSquare()) return false;
        
        if (sideToMove() == White) {
            if ((noEaOne(from) == epSquare()) || (noWeOne(from) == epSquare()))
                return (at(soutOne(epSquare())) == BP);
        } else { // side_to_move() == Black
            if ((soEaOne(from) == epSquare()) || (soWeOne(from) == epSquare()))
                return (at(nortOne(epSquare())) == WP);
        }

        return false;
    }
    
    /* Preconditions: Move is pseudo-legal and the moving piece is a pawn */
    bool StandardPosition::isDoubleJump(basic_move& move) {
        Square from = move.from();
        Square to   = move.to();
        
        ColoredPiece p = at(from);
        //if (typeOfPiece(p) != Pawn) return false; // Is this redundant since only makePawnMove should call this?
        
        unsigned char from_rank = (p.color() == White ? 1 : 6);
        unsigned char to_rank   = (p.color() == White ? 3 : 4);
        
        if ((from.rank() != from_rank) || (to != Square(to_rank, to.file()))) return false;
        
        return true;
    }
    
    /* Preconditions: Move is pseudo-legal and the moving piece is a pawn */
    bool StandardPosition::isPromotion(basic_move& move) {
        unsigned char rank = move.to().rank();
        return (rank == 7) || (rank == 0);
    }
    
    /* Returns true if move is pseudo_legal given the arrangement of pieces on the board, 
     * the state of the en passant square and castling rights, and the side to move. */ 
    bool StandardPosition::isPseudoLegal(basic_move& move) {
        if (!is_valid(move)) return false;  // Source and destination square are valid and unique, the piece
                                            // on the source square is the right color to move
        
        Square to   = move.to();        
        Bitboard to_bb = squareBB(to);
        Bitboard moves = pseudoLegalMoves(move.from());
        
        //print_bitboard(moves); // Debug
        
        return to_bb & moves;
    }
    
    void StandardPosition::promote(Piece pt) {
        Bitboard wp = board().bitboard(WP) & ranksBB(7); // White pawn promotion candidates
        Bitboard bp = board().bitboard(BP) & ranksBB(0); // Black pawn promotion candidates
                
        /* Make sure there is only one promotion candidate */
        char pop = BBPopCount(wp | bp);
        if (pop > 1) {
            throw AGChess_Exception("Standard_Position::promote() Multiple promotion candidates");
        } else if (pop == 0) {
            return; // Do nothing when there is no pawn to promote
        }
        
        /* Promoted piece must be a Queen, Knight, Rook, or Bishop */
        if ((!pt.isPiece()) || (pt == Pawn) || (pt == King)) {
            throw AGChess_Exception("Standard_Position::promote() Illegal promotion piece type");
        }
        
        Square s = squareForBitboard(wp | bp);
        Color c  = (s.rank() == 0) ? Black : White;
        
        board_.set(s, ColoredPiece(c, pt));
        requires_promotion_ = false;
    }
    
#pragma mark -
#pragma mark Move generation bitboards

    inline Bitboard StandardPosition::sliding_attacks(Piece p, Square s) const {
        return AGChess::sliding_attacks(board().occupied(), p, s);
    }
    
    /* Returns all the squares that are pseudo-legal for the piece at Square s to move to.  Returns
     * empty bitboard if there is no piece at s */
    Bitboard StandardPosition::pseudoLegalMoves(Square s) const {
        ColoredPiece p = at(s);
        Bitboard b = EmptyBB;
        if (!p.isPiece()) {return b;}  // Return EmptyBB if s doesn't have a piece on it
        Piece pt = p.piece();  // Get Piece immediately rather than inline a bunch of piece() calls        
        Color c = p.color();
        
        if (pt.isSlider()) {  // Rook, Bishop, or Queen
            b = ~board().occupied(c) & sliding_attacks(pt, s);  // Sliding attacks and squares not occupied
                                                                   // by friendly pieces of p
            
        } else if (pt == Knight) {
            b = pieceMoves(Knight, s) & ~board().occupied(c);  // Precomputed knight moves and not occupied
                                                                  // by friendly pieces of p
        } else if (pt == King) {
            b = (pieceMoves(King, s) & ~board().occupied(c)) | // Regular king moves minus friendlies
                    pseudoLegalCastle(c);
        } else if (pt == Pawn) {
            // Insert code for pseudo-legal pawn moves here
            Bitboard pawn = squareBB(s);
            Bitboard push;
            Bitboard attack;
            Bitboard opponents;
            
            if (p.color() == White) {
                push      = w_pawn_push_targets(pawn, board().empty());
                attack    = w_pawn_attacks(pawn);
                opponents = board().occupied(Black);
                if (epSquare().rank() == 5) opponents |= squareBB(epSquare());
            } else { // p.color() == Black
                push      = b_pawn_push_targets(pawn, board().empty());
                attack    = b_pawn_attacks(pawn);
                opponents = board().occupied(White);
                if (epSquare().rank() == 2) opponents |= squareBB(epSquare());
            }
            
            b = push | (attack & opponents);
        }
        
        return b;
    }    
    
    Bitboard StandardPosition::pseudoLegalCastle(Color c) const {
        // Surely there's a nice optimization for this method
        Bitboard oc = board().occupied();  // Store occupancy bitboard
        
        // Branchless method for determining if intermediate castling squares are empty
        
        /* SquaresBB[g1 + 56*color_index(c)] is a trick to shift the square by 7 ranks if c==1, and keep the
         * square the same if c==0 
         *
         * (oc | (oc << 1)) and the similar code (oc | (oc >> 1) | (oc << 1)) maps each square in between
         * the king and rook to the king's destination square.  If any of these is occupied, then taking
         * the complement of the resulting Bitboard results in the destination square having a 0 bit, and
         * consequently masking with only the destination square results in a 0 value and thus the destination
         * square is not a pseudo-legal castle move because one of the intermediate squares is occupied.
         *
         * Multiplying by castling_right(c, CastlingSide), which is a boolean, will set the destination square
         * to 0 if the CastlingRight isn't available. 
         */
        Bitboard bb = (~(oc | (oc << 1)) & squareBB(Square(g1 + 56 * c.color_index()))) * hasCastlingRight(c, Kingside) ;
        bb |= (~(oc | (oc >> 1) | (oc << 1)) & squareBB(Square(c1 + 56 * c.color_index() ))) * hasCastlingRight(c, Queenside);
        
        return bb;
    }
    
    bool StandardPosition::inCheck(Color c) const {
        Square s = squareForBitboard(board_.bitboard(ColoredPiece(c, King))); // Get the king square
        return AGChess::squareAttackedByColor(board_, s, c.opposite());
    }
    
#pragma mark -
#pragma mark Make and Unmake helper methods

    /* Precondition: move describes a castling act and it is legal for the moving side to castle */
    void StandardPosition::makeCastle(basic_move& move) {
        /* Since we're working with a standard chess position, we can hard code in source and destination
         * squares for castling (e1 is always the white king square, h1 is always the white O-O square, etc.).
         * This will need to be changed in a subclass made to support Chess960. */
        
        if (move.to() == g1) {
            board_.move(h1, f1);
        } else if (move.to() == c1) {
            board_.move(a1, d1);
        } else if (move.to() == g8) {
            board_.move(h8, f8);
        } else if (move.to() == c8) {
            board_.move(a8, d8);
        }
        
        move.setIsCastle(true);
    }
    
    void StandardPosition::unmakeCastle(const basic_move& move) {
        /* Reset the rook's position to where it was before the move.
         * The king's position will be reset in unmake() */
        if (move.to() == g1) {
            board_.move(f1, h1);
        } else if (move.to() == c1) {
            board_.move(d1, a1);
        } else if (move.to() == g8) {
            board_.move(f8, h8);
        } else if (move.to() == c8) {
            board_.move(d8, a8);
        } 
    }
    
    /* Precondition: Move has been validated and PieceType at move.from() is Pawn */
    void StandardPosition::makePawnMove(basic_move& move) {
        /* Set a new en passant square if a pawn is pushed two squares */
        if (isDoubleJump(move)) {
            if (sideToMove() == White) {
                setEpSquare(nortOne(move.from()));
            } else { // side_to_move() == Black
                setEpSquare(soutOne(move.from()));
            }
            return; // Nothing more to do, return early
        } 
        
        /* Update capture information if the move is an en passant capture */
        else if (isEnPassantCapture(move)) {
            move.setCapturedSquare(ep_capture_square());
            move.setCapturedPiece( ColoredPiece(sideToMove().opposite(), Pawn) );  // Pawn opposite color of side moving
            move.setIsCapture(true);
            board_.clear(move.capturedSquare());
        } 
        
        /* Set the requires promotion flag.  make() will attempt to promote if a promotion piece is designated */
        else if (isPromotion(move)) {
            requires_promotion_ = true;
            move.setIsPromotion(true);
        }
            
        /* Reset the en passant square.  If the move was a two-square push the ep square was set
         * earlier and the method returned */
        setEpSquare(InvalidSquare);        
        
    }
        
    /* Preconditions:  Move has been validated and the PieceType at move.from() is 
     * a king.  */
    void StandardPosition::makeKingMove(basic_move& move) {
        if (isCastle(move)) {
            // Can't castle if in check
            if (inCheck(sideToMove())) { 
                throw AGChess_Exception("Standard_Position::makeKingMove() castling out of check.");
            }
            
            Square to = move.to();
    
            // Can't castle into check
            if (squareAttackedByColor(board(), to, sideToMove().opposite())) {
                throw AGChess_Exception("Standard_Position::makeKingMove() castling into check.");   
            }
            
            // Can't castle through check
            if ((to == g1) && (squareAttackedByColor(board(), f1, Black))) {
                throw AGChess_Exception("Standard_Position::makeKingMove() castling squares attacked.");   
            } else if ((to == c1) && (squareAttackedByColor(board(), d1, Black))) {
                throw AGChess_Exception("Standard_Position::makeKingMove() castling squares attacked.");   
            } else if ((to == g8) && (squareAttackedByColor(board(), f8, White))) {
                throw AGChess_Exception("Standard_Position::makeKingMove() castling squares attacked.");   
            } else if ((to == c8) && (squareAttackedByColor(board(), d8, White))) {
                throw AGChess_Exception("Standard_Position::makeKingMove() castling squares attacked.");   
            } 
                
            // Make the castling move.  Any invalid conditions throw exceptions
            makeCastle(move);
        }
        
        // Reset castling rights
        set_castling_right(sideToMove(), Kingside,  false);
        set_castling_right(sideToMove(), Queenside, false);
        
    }
    
    /* Preconditions: Move has been validated and the PieceType at move.from() is
     * a rook. */
    void StandardPosition::makeRookMove(basic_move& move) {
        /* Reset castling rights when a rook moves */
        if ((move.from() == a1) && (sideToMove() == White)) {
            set_castling_right(White, Queenside, false);
        } else if ((move.from() == h1) && (sideToMove() == White)) {
            set_castling_right(White, Kingside, false);
        } else if ((move.from() == a8) && (sideToMove() == Black)) {
            set_castling_right(Black, Queenside, false);
        } else if ((move.from() == h8) && (sideToMove() == Black)) {
            set_castling_right(Black, Kingside, false);
        }
        
    }
    
    /* Saves the current state of the Position into move for use with unmake */
    void StandardPosition::makeSaveState(basic_move& move) {
        move.setCastlingRights(castlingRights());
        move.setEpSquare(epSquare());
        move.setPly(ply());
        move.setHalfmoveClock(halfmoveClock());
        move.setSideToMove(sideToMove());
    }
    
    void StandardPosition::unmakeSaveState(const basic_move& move) {
        setCastlingRights(move.castlingRights());
        setEpSquare(move.epSquare());
        setPly(move.ply());
        setHalfmoveClock(move.halfmoveClock());
        setSideToMove(move.sideToMove());
    }
    
    void StandardPosition::makeNullMove(basic_move& move) {
        
    }
    
#pragma mark -
#pragma mark Copying
    
    StandardPosition& StandardPosition::copy(const Position& position) {
        if (isLegalStandardPosition(position)) {
            setCastlingRights(position.castlingRights());
            setEpSquare(position.epSquare());
            setSideToMove(position.sideToMove());
            setBoard(position.board());
            setPly(position.ply());
            setHalfmoveClock(position.halfmoveClock());
        } else {
            throw AGChess_Exception("StandardPosition::copy() cannot copy illegal position");
        }
            
        
        return *this;
    }
    
#pragma mark -
#pragma mark Nonmember Methods
    
    bool isLegalStandardPosition(const Position& position) {
        /* Check color of side to move */
        if (!position.sideToMove().isValid()) return false;
        
        const Board& board = position.board();
        
        /* Make sure there's only one king */
        if ((coloredPieceCount(board, WK) != 1) ||
            (coloredPieceCount(board, BK) != 1)) {
            return false;
        }
        
        /* Can the side to move capture the opponents king? */
        if (inCheck(position, position.sideToMove().opposite())) return false;
        
        /* Are there more than two checkers? */
        Square king = kingSquare(board, position.sideToMove());
        if (BBPopCount(squareAttackedByColor(board, king, position.sideToMove().opposite())) > 2)
            return false;
        
        /* En Passant square ok? */
        Square ep = position.epSquare();
        if (ep == InvalidSquare) {/* Do nothing */}
        else {
            // Square must be on the 6th rank of the side to move
            if (ep.rank() != (position.sideToMove() == White ? 5 : 2))
                return false;
        } 

        /* Piece counts */
        int wpawns = coloredPieceCount(board, WP);
        int bpawns = coloredPieceCount(board, BP);
        
        if ((wpawns > 8) || (bpawns > 8)) return false; // Too many pawns
        if ((wpawns + coloredPieceCount(board, WQ) > 9) ||
            (bpawns + coloredPieceCount(board, BQ) > 9)) return false; // Too many queens
        if ((wpawns + coloredPieceCount(board, WR) > 10) ||
            (bpawns + coloredPieceCount(board, BR) > 10)) return false; // Too many rooks
        if ((wpawns + coloredPieceCount(board, WN) > 10) ||
            (bpawns + coloredPieceCount(board, BN) > 10)) return false; // Too many knights
        if ((wpawns + coloredPieceCount(board, WB) > 10) ||
            (bpawns + coloredPieceCount(board, BB) > 10)) return false; // Too many bishops
        
        if ((colorCount(board, White) > 16) || (colorCount(board, Black) > 16))
            return false; // Too many pieces of the same color
        
        return true;
    }
    
    bool inCheck(const Position& position, Color c) {
        Square s = kingSquare(position.board(), c); // Get the king square
        return squareAttackedByColor(position.board(), s, c.opposite() );
    }
};