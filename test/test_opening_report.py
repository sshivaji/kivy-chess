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
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import chess
import chess.pgn
import os
import unittest
import leveldb
from leveldict import LevelJsonDict
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import textwrap

INITIAL_BOARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
INDEX_FILE_POS = "last_pos"

DB_HEADER_MAP = {"White": 0, "WhiteElo": 1, "Black": 2,
                 "BlackElo": 3, "Result": 4, "Date": 5, "Event": 6, "Site": 7,
                 "ECO": 8, INDEX_FILE_POS:9, "FEN":10}

class OpeningTestCase(unittest.TestCase):
    def get_game(self, db_index, game_num):
        first = db_index.Get("game_{0}_data".format(game_num)).split("|")[DB_HEADER_MAP[INDEX_FILE_POS]]
        first = int(first)
        #        if game_num+1 < self.pgn_index[INDEX_TOTAL_GAME_COUNT]:
        #            second = self.db_index_book.Get("game_{0}_{1}".format(game_num+1,INDEX_FILE_POS))
        #        second = self.pgn_index["game_index_{0}".format(game_num+1)][INDEX_FILE_POS]
        try:
            second = db_index.Get("game_{0}_data".format(game_num + 1)).split("|")[DB_HEADER_MAP[INDEX_FILE_POS]]
            second = int(second)
        except KeyError:
            second = None

        file_name = db_index.Get("pgn_filename")
        if not os.path.isfile(file_name):
            file_name = file_name.replace("home", "Users")
        # print file_name
        # print "first: {0}".format(first)
        # print "second: {0}".format(second)

        with open(file_name) as f:
            first = int(first)

            f.seek(first)
            line = 1
            lines = []
            first_line = False
            while line:
                line = f.readline()
                temp = line.strip()
                if not first_line:
                    temp = '[' + temp
                first_line = True
                # line = line.strip()
                pos = f.tell()
                if second and pos >= second:
                    break
                    # print pos
                if temp:
                    lines.append(temp)
        # f.close()
        # for l in lines:
        #     print l
        # print dir(PgnFile)
        # print lines
        game_text = "\n".join(lines)
        # g = chess.pgn.read_game(game_text)
        # print g
        pgn = StringIO(textwrap.dedent(game_text))

        games = chess.pgn.read_game(pgn)
        # games = PgnFile.open_text(lines)
        return games

    def test_load_complex_pgn(self):
        # 131563

        db = leveldb.LevelDB('book/polyglot_index.db')
        # print db
        g = self.get_game(db, 1)
        node = g
        # print node
        while node.variations:              
            move = node.move
            piece = node.piece_type_at(move.from_square)
            print piece

            print node.move
            # print node.board()
            node = node.variation(0)
if __name__ == '__main__':
    unittest.main()
