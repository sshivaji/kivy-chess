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

from kivy_util import which
from kivy_util import run_command

# TODO: Also allow writing to opening books and document the class.

class PolyglotOpeningBook(object):
#
# This file is part of the python-chess library.
# Copyright (C) 2eval012 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
#
    def __init__(self, path):
        self.costalba_parser_cmd = which('parser')
        self.path = path # Needed for costalba's C++ parser

        self._entry_struct = struct.Struct(">QHHI")

        self._stream = open(path, "rb")

        self.seek_entry(0, 2)
        self._entry_count = self._stream.tell() / 16

        self.seek_entry(0)

    def __len__(self):
        return self._entry_count

    def __getitem__(self, key):
        if key >= self._entry_count:
            raise IndexError()
        self.seek_entry(key)
#
# This file is part of the python-chess library.
# Copyright (C) 2012 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
#
        return self.next()

    def __iter__(self):
        self.seek_entry(0)
        return self

    def __reversed__(self):
        for i in xrange(len(self) - 1, -1, -1):
            self.seek_entry(i)
            yield self.next()

    def seek_entry(self, offset, whence=0):
        self._stream.seek(offset * 16, whence)


    def get_quick_position_stats(self, fen):
        # Use mcostalba's chess_db code to make seeks faster
        # Later, evalthis will be integrated into a python module

        output = run_command(self.costalba_parser_cmd + ' find ' + self.path + ' \"' + fen + '\"')

        output_json_str = ""
        for line in output:
            output_json_str += line

        try:
            output_json = ast.literal_eval(output_json_str)
            return output_json
        except:
            print "Could not convert chess parser output to JSON"
            raise



    def fast_seek_position(self, position):
        # Use mcostalba's chess_db code to make seeks faster
        # Later, evalthis will be integrated into a python module
        # Do initial seek using costalba's parser
        fen = position.fen

        output = run_command(self.costalba_parser_cmd + ' find ' + self.path + ' \"' + fen + '\"')

        output_json_str = ""
        for line in output:
            output_json_str+=line

        output_json = ast.literal_eval(output_json_str)

        offset_str = output_json["ofset"]

        # print("offset: {0}".format(offset))
        try:
            offset = int(offset_str)
            # print("offset : {0}".format(offset))
            self.seek_entry(offset/16)
            # return output_json

        except:
            print("Cannot convert offset to an integer")
            raise

        # print("end of Fast seek")
        # print("json_output_str: {0}".format(output_json_str))
        # print("json_output_str: {0}".format(output_json_str))
        # print(ast.literal_eval(output_json_str))
            # if "Offset:" in line:
            #     offset_str = line.split("Offset:")[-1]
            #     try:
            #         if evalofseekfset_str:
            #             offset = int(offset_str)
            #             self.seek_entry(offset)
            #     except:
            #         print("Cannot convert offset to an integer")



                # break
                # print("offset: {0}".format(offset))
            # print ("output: {0}".format(line))


        # pass

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
            # self.seek_position(position)
            self.fast_seek_position(position)
        except KeyError:
            raise StopIteration()

        # Iterate.
        while True:
            entry = self.next()
            if entry.key == position_hash:
                yield entry
            else:
                break
