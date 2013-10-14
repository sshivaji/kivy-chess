#!/usr/bin/python

## dgtnix.py,  a test program for the dgtnix driver python bindings,
## Copyright (C) 2007 Pierre Boulenguez

## dgtnix, a POSIX driver for the Digital Game Timer chess board and clock
## Copyright (C) 2006-2007 Pierre Boulenguez

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


import sys
import os
import errno
import time

from dgtnix import *

# Load the library
try:
    dgtnix = dgtnix("libdgtnix.so")
except DgtnixError, e:
    print "unable to load the librairie : %s " % e
    sys.exit()

print "dgtnixTest.py is a test Program for the dgtnix driver python bindings."
print "This is dgtnix version %s " % dgtnix.QueryString(dgtnix.DGTNIX_DRIVER_VERSION)

if len(sys.argv)!= 2:
 print "usage: ./dgtnixTest.py port"
 print "Port is the port to which the board is connected."
 print "For usb connection, try : /dev/usb/tts/0, /dev/usb/tts/1, /dev/usb/tts/2 ..."
 print "For serial, try : /dev/ttyS0, /dev/ttyS1, /dev/ttyS2 ..."
 print "For the virtual board /tmp/dgtnixBoard is the default but you can change it."
 sys.exit()

# Turn debug mode to level 2
# all debug informations are printed
dgtnix.SetOption(dgtnix.DGTNIX_DEBUG, dgtnix.DGTNIX_DEBUG_ON)
# Initialize the driver with port argv[1]
result=dgtnix.Init(sys.argv[1])
if result < 0:
    print "Unable to connect to the device on "+sys.argv[1]
    sys.exit()
print "The board was found"
dgtnix.update()
#board_out = ""
dgtnix.SendToClock("tall  ", True, False)
while True:
   # bd = ""
    print dgtnix.GetFen()
    time.sleep(1)
   # print dgtnix.GetBoard(True)
    #print bd
    #time.sleep(1)
dgtnix.Close()

