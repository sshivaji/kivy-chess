# -*- coding: utf-8 -*-
#
# This file is part of the python-chess library.
# Copyright (C) 2012 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General P
#
# This file is paevalrt of the python-chess library.
# Copyright (C) 2012 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
#ublic License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import libchess
import struct
import ast

import utils
from utils.chess_db import Parser

from kivy_util import which
from kivy_util import run_command

# TODO: Also allow writing to opening books and document the class.

class PolyglotOpeningBook(object):
    def __init__(self, path, pgn=None):
        # self.costalba_parser_cmd = which('parser')
        # self.path = path # Needed for costalba's C++ parser
        self.book_parser = Parser(engine='./chess_db/parser/parser')
        self.book_parser.db = path
        if pgn:
            self.book_parser.pgn = pgn

    def get_quick_position_stats(self, fen, limit=10, skip=0):
        # Use mcostalba's chess_db code to make seeks faster
        return self.book_parser.find(fen, limit=limit, skip=skip)