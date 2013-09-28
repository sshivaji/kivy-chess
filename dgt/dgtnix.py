## This is a python binding for the dgtnix driver
## to use it :
##     from dgtnix import *
##     dgtnix = dgtnix("libdgtnix.so")
##     dgtnix.Init("/dev/ttySO")

## dgtnix, a POSIX driver for the Digital Game Timer chess board and clock
## Copyright (C) 2007 Pierre Boulenguez

## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


from ctypes import *

#API funtions
# int dgtnixInit(const char *);
# int dgtnixClose();
# const char *dgtnixGetBoard();
# void dgtnixPrintBoard(const char *, char *);
# int dgtnixTestBoard(const char *);
# void dgtnixSetOption(unsigned long,unsigned int);
# float dgtnixQueryDriverVersion();
# const char *dgtnixQueryString(unsigned int);
# int dgtnixGetClockData(int *, int *, int *);

class DgtnixError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#libname is dgtnix.so on unix
class dgtnix:
##
##   Constant definitions
##
    #   message emitted when a piece is added onto the board
    DGTNIX_MSG_MV_ADD=0x00
    #   message emitted when a piece is removed from the board
    DGTNIX_MSG_MV_REMOVE=0x01
    #   message emitted when the clock send information
    DGTNIX_MSG_TIME=0x02
    #   serial tag for the dgtnixQueryString function
    DGTNIX_SERIAL_STRING=0x1F00
    #  busadress tag for the dgtnixQueryString function
    DGTNIX_BUSADDRESS_STRING=0x1F01
    #   version tag for the dgtnixQueryString function
    DGTNIX_VERSION_STRING=0x1F02
    #   trademark tag for the dgtnixQueryString function
    DGTNIX_TRADEMARK_STRING=0x1F03
    # version of the driver
    DGTNIX_DRIVER_VERSION=0x1F04
    # Here come the options of setOption
    DGTNIX_BOARD_ORIENTATION=0x01
    DGTNIX_DEBUG=0x02
    # and here the possible values for each option
    DGTNIX_BOARD_ORIENTATION_CLOCKLEFT=0x01
    DGTNIX_BOARD_ORIENTATION_CLOCKRIGHT=0x02
    DGTNIX_DEBUG_ON=0x01
    DGTNIX_DEBUG_OFF=0x04
    DGTNIX_DEBUG_WITH_TIME=0x08


    def __init__(self,libName):
        self.libName=libName
        try:
            self.lib=cdll.LoadLibrary(self.libName)
        except OSError:
            raise DgtnixError, "cannot find the dgtnix library "+self.libName
        self.Init=self.lib.dgtnixInit
        self.Close=self.lib.dgtnixClose
        self.GetBoard=self.lib.dgtnixGetBoard
        self.GetFen = self.lib.getDgtFEN
        self.ToPrintableBoard=self.lib.dgtnixToPrintableBoard
        self.SendToClock=self.lib.dgtnixPrintMessageOnClock
        self.TestBoard=self.lib.dgtnixTestBoard
        self.QueryString=self.lib.dgtnixQueryString
        self.GetClockData=self.lib.dgtnixGetClockData
        self.SetOption=self.lib.dgtnixSetOption
        self.update = self.lib.dgtnixUpdate

        #parameters
        self.Init.argtypes = [c_char_p]
        self.Close.argtypes = None
        self.GetBoard.argtypes = None
        self.ToPrintableBoard.argtypes = [c_char_p]
        self.TestBoard.argtypes= [c_char_p]
        self.QueryString.argtypes = [c_uint]
        self.GetClockData.argtypes = [POINTER(c_int),POINTER(c_int),POINTER(c_int)]
        self.SetOption.argtypes = [c_ulong, c_uint]

        #return types
        self.Init.restype = c_int
        self.Close.restype = None
        self.GetBoard.restype = c_char_p
        self.GetFen.restype = c_char_p
        self.ToPrintableBoard.restype = c_char_p
        self.TestBoard.restype = c_int
        self.QueryString.restype = c_char_p
        self.GetClockData.restype = c_int
        self.SetOption.restype = None

