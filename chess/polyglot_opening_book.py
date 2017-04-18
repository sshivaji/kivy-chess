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

    def __len__(self):
        return self._entry_count

    def __getitem__(self, key):
        if key >= self._entry_count:
            raise IndexError()
        self.seek_entry(key)
        return self.next()

    def __iter__(self):
        self.seek_entry(0)
        return self

    def __reversed__(self):
        for i in range(len(self) - 1, -1, -1):
            self.seek_entry(i)
            yield self.next()

    def seek_entry(self, offset, whence=0):
        self._stream.seek(offset * 16, whence)

    def get_quick_position_stats(self, fen):
        # Use mcostalba's chess_db code to make seeks faster
        return self.book_parser.find(fen)

    def seek_position(self, position):
        # Calculate the position hash.
        # start_time = time.time()
        key = position.__hash__()
        # end_time = time.time()

        # Do a binary search.
        start = 0
        end = len(self)
        while end >= start:
            middle = (start + end) / 2

            self.seek_entry(middle)
            # start_time = time.time()
            raw_entry = self.next_raw()
            # end_time = time.time()
            # print("Elapsed next_raw_entry time was %g seconds" % (end_time - start_time))

            if raw_entry[0] < key:
                start = middle + 1
            elif raw_entry[0] > key:
                end = middle - 1
            else:
                # Position found. Move back to the first occurence.
                # This code block takes too long if we have many positions (e.g. start position has 1M game_id entries)
                # start_time = time.time()
                seek_count = 0
                self.seek_entry(-1, 1)
                while raw_entry[0] == key and middle > start:
                    # print("seek..")
                    seek_count +=1
                    middle -= 1
                    self.seek_entry(middle)
                    raw_entry = self.next_raw()

                    if middle == start and raw_entry[0] == key:
                        self.seek_entry(-1, 1)
                # end_time = time.time()
                # print("Elapsed move back to first occurence time was %g seconds" % (end_time - start_time))
                # print("seek counts: {0}".format(seek_count))

                return

        raise KeyError()

    def next_raw(self):
        try:
            return self._entry_struct.unpack(self._stream.read(16))
        except struct.error:
            raise StopIteration()

    def next(self):
        raw_entry = self.next_raw()
        # print("raw_move: {0}".format(raw_entry[1]))
        return libchess.PolyglotOpeningBookEntry(raw_entry[0], raw_entry[1],
                                              raw_entry[2], raw_entry[3])

    def get_entries_for_position(self, position):
        position_hash = position.__hash__()

        # Seek the position. Stop iteration if no entry exists.
        try:
            self.seek_position(position)
            # self.fast_seek_position(position)
        except KeyError:
            raise StopIteration()

        # Iterate.
        while True:
            entry = self.next()
            if entry.key == position_hash:
                yield entry
            else:
                break
