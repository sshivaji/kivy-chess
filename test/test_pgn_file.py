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
import unittest
from chess.libchess import GameHeaderBag
from chess.leveldict import LevelJsonDict

class PgnIndexTestCase(unittest.TestCase):
    """Tests indexing PGN files."""

    def write_header(self, g, gm_book, i, tags):
        j = {}
        for tag in tags:
            if type(tag) is dict:
                for k,v in tag.iteritems():
                    j[k] = v
            elif g.__contains__(tag):
                # print g[tag]
                j[tag] = unicode(g[tag], "ISO-8859-1")

        # print j
        # try:
        gm_book["game_index_{0}".format(i)] = j
        # except UnicodeDecodeError:
        #     gm_book["game_index_{0}".format(i)] = j.unicode(("utf-8")

    def test_uncommented(self):
        """Tests indexing the uncommented Kasparov vs. Deep Blue PGN."""
        # gm_book = LevelJsonDict('gm_test.db')
        gm_book = LevelJsonDict('book/userbook.db')
        # # pgn_file = "test/kasparov-deep-blue-1997.pgn"
        # pgn_file = "test/2600_2013_34.pgn"
        #
        # index = chess.PgnIndex(pgn_file)
        # gm_book["total_game_count"] = index.__len__()
        # gm_book["pgn_filename"] = pgn_file
        # print "length:"
        # print index.__len__()
        # for i in range(0, index.__len__()):
        #     g = index.get_game_headers(i)
        #     # print index.get_pos(1)
        #     self.write_header(g, gm_book, i, [{"file_pos":index.get_pos(i)},'Event', 'Site', 'Date', 'White', 'Black', 'Result', 'PlyCount', 'ECO', 'Round', 'EventDate', 'WhiteElo', 'BlackElo', 'PlyCount', 'Source', 'EventType'])

        games = chess.PgnFile.open('test/watson_strategic.pgn', leveldb_book=gm_book)
        for game_index, g in enumerate(games):
            while g:
                if g.previous_node:
                    position_hash = str(g.previous_node.position.__hash__())
                    if position_hash not in gm_book:
                        gm_book[position_hash] = {"moves": [], "annotation": "",
                                                          "eval": "", "games": [game_index], "misc": ""}

                    entry = gm_book[position_hash]

                    if g.move:
                        moves = entry["moves"]
                        str_move = str(g.move)

                        if moves:
                            if str_move not in moves:
                                moves.append(str(g.move))
                                entry["moves"]=moves
                                gm_book[position_hash] = entry
                        else:
                            entry["moves"]=[str_move]
                            gm_book[position_hash] = entry

                    entry = gm_book[position_hash]

                    games = entry["games"]
                    if game_index not in entry["games"]:
                        games.append(game_index)
                        entry["games"] = games
                        gm_book[position_hash] = entry


                        #                print g.move
                g = g.get_next_main_move()

if __name__ == '__main__':
    unittest.main()
