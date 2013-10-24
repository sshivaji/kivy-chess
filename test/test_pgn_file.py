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
from chess.leveldict import LevelJsonDict

class PgnIndexTestCase(unittest.TestCase):
    """Tests indexing PGN files."""

    def test_uncommented(self):
        """Tests indexing the uncommented Kasparov vs. Deep Blue PGN."""
#    gm_book = LevelJsonDict('gm_test.db')
#        index = chess.PgnIndex("kasparov-deep-blue-1997.pgn")
#        self.assertTrue(index.is_valid())
#
#        #print len(index)
#        first = index.get_pos(0)
#        second = index.get_pos(1)
#        #print second
#        f = open("kasparov-deep-blue-1997.pgn")
#        f.seek(first)
#        line = 1
#        lines = []
#        while line:
#            line = f.readline()
#            pos = f.tell()
#            #print pos
#            if pos<=second:
#                lines.append(line)
#            else:
#                break
#
#        games = chess.PgnFile.open_text(lines)
#        first_game = games[0]
#        print first_game

    games = chess.PgnFile.open('test/2600_2013_34.pgn')
#    g = games[5]
##    print g.headers.headers['Result']
#    for g in games[5:]:
##        print "\n"
#        while g:
#            if g.previous_node:
#                position_hash = g.previous_node.position.fen
#                if position_hash not in gm_book:
#                    gm_book[position_hash] = {"moves":[], "annotation":"",
#                                                      "eval":"", "games":[], "misc":""}
#                entry = gm_book[position_hash]
#
#                if g.move:
#                    print str(g.move)
#                    moves = entry["moves"]
#                    str_move = str(g.move)
#
#                    if moves:
#                        if str_move not in moves:
#                            moves.append(str(g.move))
#                            entry["moves"]=moves
#                            gm_book[position_hash] = entry
#                    else:
#                        entry["moves"]=[str_move]
#                        gm_book[position_hash] = entry
#
#                    #                print g.move
#            g = g.get_next_main_move()

#
#    print g.move
#    g = g .get_next_main_move()
#    print g.move

        # First game.
        #game = index.get_game_headers(0)
        #self.assertEqual(index.get_pos(0), 0)
        #self.assertEqual(game["Site"], "01")
        #self.assertEqual(game["PlyCount"], "89")
        #self.assertEqual(game["ECO"], "A06")

        # Second game.
        #game = index.get_game_headers(1)
        #self.assertEqual(game["Site"], "02")

        # Sixth (and last) game.
        #game = index.get_game_headers(5)
        #self.assertEqual(game["Site"], "06")
        #self.assertEqual(game["PlyCount"], "37")

if __name__ == '__main__':
    unittest.main()