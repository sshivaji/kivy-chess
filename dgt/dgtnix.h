/* dgtnix, a POSIX driver for the Digital Game Timer chess board and clock
Copyright (C) 2006 Pierre Boulenguez
              2012 Jean-Francois Romang
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
*/

/* 
 * This is the dgtnix driver 
 * In the following, what is called a "board representation" 
 * is a char [64] with :
 * 
 * Pieces defined as  :
 * empty square : ' ' 
 * white pawn : 'P'
 * white rook : 'R'
 * white knight : 'N'
 * white bishop : 'B'
 * white queen : 'Q' 
 * white king : 'K'
 * black pawn : 'p'
 * black rook : 'r'
 * 
 * Numbering defined as :
 * A8 is numbered 0
 * B8 is numbered 1
 * C8 is numbered 2
 * ..
 * A7 is numbered 8
 * ..
 * H1 is numbered 63
 * 
 * dgtnixQueryDriverVersion() and dgtnixSetOption(unsigned long, unsigned int) are the only functions that can be 
 * called before a successfull call to dgtnixInit. 
 *
 * If success, dgtnixInit(...) returns a read-only descriptor on which communications with the board will occur. 
 * You have to track for activity on this descriptor to figure out what is going on.
 * Message on the descriptor are :
 * 
 *  + The message DGTNIX_MSG_MV_ADD  : indicating that a piece was added on a square.
 * This type of message contains four character :
 * the first is the message code  DGTNIX_MSG_MV_ADD
 * the second is the column of the square on which the event occured
 * the third is the line of the square on which the event occured
 * and the fourth is the type of piece that was added.
 * Example : 
 *    DGTNIX_MSG_MV_ADD   A4K -> white king was added on A4
 *    DGTNIX_MSG_MV_ADD   B6n -> black knight was added on B6
 *  
 *  + The message DGTNIX_MSG_MV_REMOVE : indicating that a piece was removed from a square.
 * This type of message contains four character :
 * the first is the message code DGTNIX_MSG_MV_REMOVE 
 * the second is the column of the square on which the event occured
 * the third is the line of the square on which the event occured
 * and the fourth is the type of piece that was removed.
 * Example : 
 *     DGTNIX_MSG_MV_REMOVE A4K -> white king was removed from A4
 *     DGTNIX_MSG_MV_REMOVE B6n -> black knight was removed from B6
 * 
 *  + Message DGTNIX_MSG_TIME : the dgt XL clock as sent a time update with time information ( to be continued ) 
 * 
 * NOTE : dgtnixInit(const char *port) is not equivalent to something like the call to the 
 * open(const char *port) function. The communications between the chess engine and dgtnix 
 * occur on a different file than the file descriptor used internally by dgtnix to communicate with the device.
 * 
 * */

/******************************/
/* API Functions list         */
/******************************/
/*
  int dgtnixInit(const char *);
  int dgtnixClose();
  const char *dgtnixGetBoard();
  const char *dgtnixToPrintableBoard(const char *);
  int dgtnixTestBoard(const char *);
  const char *dgtnixQueryString(unsigned int);
  int dgtnixGetClockData(int *, int *, int *);
  void dgtnixSetOption(unsigned long, unsigned int);
*/

#ifndef __DGTNIX_H
#define __DGTNIX_H

#include <semaphore.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif
  /*
    Contains saved errno value after a failed system call 
  */
  extern int dgtnix_errno; 

  /************************/
  /* Constant definitions */
  /************************/
  /* message emitted when a piece is added onto the board */
#define DGTNIX_MSG_MV_ADD 0x00
  /* message emitted when a piece is removed from the board */
#define DGTNIX_MSG_MV_REMOVE 0x01
  /* message emitted when the clock send information */
#define DGTNIX_MSG_TIME  0x02
  /* serial tag for the dgtnixQueryString function */
#define DGTNIX_SERIAL_STRING  0x1F00
  /* busadress tag for the dgtnixQueryString function */
#define DGTNIX_BUSADDRESS_STRING 0x1F01
  /* the first busaddress was misspelled, this one is kept for compatibility */
  /*#define DGTNIX_BUSADRESS_STRING  DGTNIX_BUSADDRESS_STRING*/

  /* version tag for the dgtnixQueryString function */
#define DGTNIX_VERSION_STRING 0x1F02
  /* trademark tag for the dgtnixQueryString function */
#define DGTNIX_TRADEMARK_STRING 0x1F03

#define DGTNIX_DRIVER_VERSION 0x1F04

  
  /* options of dgtnixInit */
#define DGTNIX_BOARD_ORIENTATION 0x01
#define DGTNIX_DEBUG 0x02

#define DGTNIX_BOARD_ORIENTATION_CLOCKLEFT 0x01
#define DGTNIX_BOARD_ORIENTATION_CLOCKRIGHT 0x02
   
#define DGTNIX_DEBUG_ON 0x01
#define DGTNIX_DEBUG_OFF 0x04
#define DGTNIX_DEBUG_WITH_TIME 0x08

/*Options to display dot's an ones on the clock */
#define DGTNIX_RIGHT_DOT 0x01
#define DGTNIX_RIGHT_SEMICOLON 0x02
#define DGTNIX_RIGHT_1 0x04
#define DGTNIX_LEFT_DOT 0x08
#define DGTNIX_LEFT_SEMICOLON 0x10
#define DGTNIX_LEFT_1 0x20
  
  /******************************/
  /* API Functions declarations */
  /******************************/
  /* int dgtnixInit(const char *port); 
   * Try to initialize the DGT board and clock on port. 
   * example : have a look at the dgtnixTest program and at the 
   * dgtnixTest.cpp file
   * In case of errors (the return value of the function is negative), 
   * one can try to guess the origin of the error by decoding the dgtnix_errno variable 
   * (see 'man errno' for details)
   *
   * dgtnixSetOption() and dgtnixQueryDriverVersion() are the only functions that can be 
   * called before a successfull call to dgtnixInit
   *
   * after a sucessfull dgtnixInit(), you have to call dgtnixClose 
   * if you want to do another dgtnixInit()
   *
   *
   * Parameter :
   * + const char *port: the port to which try to connect the board (ex:"/dev/ttyS0")
   * Return :
   * + -1 if fails to open the port
   * + -2 if the port can be opened but the device does'nt seems to be a DGT chess board (does'nt respond to some basic messages)
   * + a positive number if success, this number is the descriptor of the read-only file on which the communications with the board will occur.
   */
  int dgtnixInit(const char *);
  
  /* int dgtnixClose();
   * Simpy kill running thread and opened descriptors if any.
   * 
   * dgtnixInit() always do a call to dgtnixCall before anything else to clear 
   * everything
   *
   * Return :
   * + 1 if everything went ok
   * + -1 if a problem has occured
   */
  int dgtnixClose();
  
  /* const char *dgtnixGetBoard(bool update);
   * The update flag updates the board in case of a reverse orientation
   * Return a copy of the representation of the board
   *
   * Return :
   * + a char[64], the representation of the board. 
   */
  const char *dgtnixGetBoard(bool update);
  
  /* void dgtnixDumpBoard(const char *board, char *dst);
   * Fill dst with a printable representation of the board 
   * destination is a '\0' terminated array of char of size 145
   * example to print the current board position do : 
   *
   * char str[145];
   * dgtnixDumpBoard(dgtnixGetBoard(), str);
   * printf("%s\n", str);
   *
   * results in :
   *
   * |r|n|b|q|k|b|n|r|
   * |p|p|p|p|p|p|p|p|
   * | | | | | | | | |
   * | | | | | | | | |
   * | | | | | | | | |
   * | | | | | | | | |
   * |P|P|P|P|P|P|P|P|
   * |R|N|B|Q|K|B|N|R|
   * 
   * Parameters :
   * + const char *board: a reprensation of a board (a char [64]) to print
   * + char *dst: a char [145] 
   */
  /*void dgtnixPrintBoard(const char *, char *);*/
  
  /* int dgtnixTestBoard(const char *board);
   * Test if the represenation of the board in parameter is equal to the 
   * inner representation maintained by the driver.
   *
   * Parameter :
   * + const char *board: a reprensation of a board (a char [64]) to test
   * 
   * Return :
   * + 1: if the boards are the same 
   * + 0: elsewhere
   */
  int dgtnixTestBoard(const char *);
 
  const char* getDgtFEN (char tomove);

  /* void dgtnixSetOption(unsigned long option, unsigned int value)
   * set various options for the driver,
   * currently supported options are :
   * 
   *
   * DGTNIX_DEBUG with values :
   *   DGTNIX_DEBUG_OFF : no debug info 
   *   DGTNIX_DEBUG_ON : all debug info except time messages are printed on stderr
   *   DGTNIX_DEBUG_WITH_TIME : all debug info are printed on stderr
   *
   * DGTNIX_BOARD_ORIENTATION with values :
   *   DGTNIX_BOARD_ORIENTATION_CLOCKLEFT 
   *   DGTNIX_BOARD_ORIENTATION_CLOCKRIGHT 
   * 
   * example :
   * dgtnixSetOption(DGTNIX_DEBUG, DGTNIX_DEBUG_ON);
   * set the debug mode on.
   * 
   */
  void dgtnixSetOption(unsigned long, unsigned int);
  
  
  /* const char *dgtnixQueryString(unsigned int flag);
   * Query a vendor string 
   * example of use : 
   * cout <<"Serial number :" << dgtnixQueryString(DGTNIX_SERIAL_STRING) << endl;
   * 
   * Parameter :
   * + flag : the string to return, must be one of 
   *            DGTNIX_SERIAL_STRING
   *            DGTNIX_BUSADRESS_STRING 
   *            DGTNIX_VERSION_STRING 
   *            DGTNIX_TRADEMARK_STRING
   *            DGTNIX_VERSION
   * Return : the requested string in a printable form
   * ATTENTION : the returned string must not be freed !!!
   */  
  const char *dgtnixQueryString(unsigned int);
  
   /* int dgtnixGetClockData(int *pwhite_time, int *pblack_time, int *pwhite_turn);
    * Query the data for the DGT clock (if present). If no clock was found,  the 
    * values pointed by the parameters are left unchanged.
    *
    * All the time info are in seconds.
    * Parameters :
    * + int *pwhite_time : the integer pointed will contain the white time as sent by the clock
    * + int *pblack_time : the integer pointed will contain the black time as sent by the clock
    * + int *pwhite_turn : regarding the button pressed on the DGT clock, 
    * *pwhite_turn will be set to 1 if it is white's turn, otherwise 0 (black's turn).
    * 
    * Return : 1 if a DGT clock was found, otherwise 0
    * 
   */  
  int dgtnixGetClockData(int *, int *, int *);
  
  const char *dgtnixToPrintableBoard(const char *);
  
  /* Prints a 6 character string message on the DGT Clock */
  void dgtnixPrintMessageOnClock(const char *, unsigned char beep, unsigned char dots);
  void dgtnixUpdate();

  /* Manage clock buttons */
  int getClockButtonState();
  extern int clockButtonState;
  
  /* Event semaphore */
  extern sem_t dgtnixEventSemaphore;
  
#ifdef __cplusplus
}
#endif 

/* End #ifndef __DGTNIX_H */
#endif
