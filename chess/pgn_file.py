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
import re

tag_regex = re.compile(r"\[([A-Za-z0-9]+)\s+\"(.*)\"\]")
movetext_regex = re.compile(r"""
    (\;.*?[\n\r])
    |(\{.*?[^\\]?\})
    |(\$[0-9]+)
    |(\()
    |(\))
    |(\*|1-0|0-1|1/2-1/2)
    |(
        ([a-hKQRBN][a-hxKQRBN1-8+#=\-]{1,6}
        |O-O(?:\-O)?)
        ([\?!]{1,2})*
    )
    """, re.DOTALL | re.VERBOSE)

class PgnFile(object):
    def __init__(self):
        self._games = []

    def add_game(self, game):
        self._games.append(game)

    def __len__(self):
        return len(self._games)

    def __getitem__(self, key):
        return self._games[key]

    def __setitem__(self, key, value):
        self._games[key] = value

    def __delitem__(self, key):
        del self._games[key]

    def __iter__(self):
        for game in self._games:
            yield game

    def __reversed__(self):
        for game in reversed(self._games):
            yield game

    def __contains__(self, game):
        return game in self._games

    @classmethod
    def __parse_movetext(cls, game, movetext, game_num = None, leveldb = None):
        variation_stack = [game]
        in_variation = False
        start_comment = ""
        # print "movetext:"
        # print movetext
        for match in movetext_regex.finditer(movetext):
            token = match.group(0)
            # print "token: {0}".format(token)
            if token in ["1-0", "0-1", "1/2-1/2", "*"] and len(variation_stack) == 1:
                game.headers["Result"] = token
            elif token.startswith("%"):
                # Ignore rest of line comments.
                pass
            elif token.startswith("{"):
                # print "token: {0}".format(token)
                if in_variation:
                    variation_stack[-1].comment += token[1:-1].strip()
                elif len(variation_stack) == 1:
                    variation_stack[0].start_comment += token[1:-1].strip()
                else:
                    start_comment += token[1:-1].strip()
            elif token.startswith("$"):
                if not in_variation:
                    raise PgnError("NAGs must go behind moves.")
                variation_stack[-1].nags.append(int(token[1:]))
            elif token == "(":
                try:
                    variation_stack.append(variation_stack[-1].previous_node)
                except IndexError, e:
                    print "Variation Index error"
                    print e
                    return
                in_variation = False
            elif token == ")":
                variation_stack.pop()
            else:
                in_variation = True
                try:
                    pos = variation_stack[-1].position
                except IndexError:
                    print "Odd error"
                    print "pos:"
                    print pos
                    print "token:"
                    print token
                    return
                try:
                    mv = pos.get_move_from_san(str(token))
                    variation_stack[-1] = variation_stack[-1].add_variation(mv)
                    if game_num and leveldb is not None:
                        cls.write_to_ldb(variation_stack[-1], mv, game_num, leveldb)
                except ValueError, e:
                    if str(e).startswith('Variation already in set:'):
                        variation_stack[-1] = variation_stack[-1].add_variation(pos.get_move_from_san(str(token)), force=True)
                    elif str(e).startswith('Invalid argument: move') or str(e).startswith('san'):
                        print "Illegal move encountered in game"
                        print "position:"
                        print pos
                        print "token:"
                        print token
                        # return
                    else:
                        print pos
                        print token
                        # raise


#                     pass
                except IndexError:
                    pass
                variation_stack[-1].start_comment = start_comment
                start_comment = ""


    @classmethod
    def write_to_ldb(cls, g, mv, i, leveldb_book):
        if g.previous_node:
            position_hash = str(g.previous_node.position.__hash__())
            if position_hash not in leveldb_book:
                leveldb_book[position_hash] = {"moves": [], "annotation": "", "color":["white"],
                                               "eval": 5, "games": [i], "misc": ""}

            entry = leveldb_book[position_hash]

            if mv:
            #                    print str(g.move)
                moves = entry["moves"]
                str_move = str(g.move)

                if moves:
                    if str_move not in moves:
                        moves.append(str(mv))
                        entry["moves"] = moves
                        leveldb_book[position_hash] = entry
                else:
                    entry["moves"] = [str_move]
                    leveldb_book[position_hash] = entry

            entry = leveldb_book[position_hash]

            games = entry["games"]
            if i not in entry["games"]:
                games.append(i)
                entry["games"] = games
                leveldb_book[position_hash] = entry

    @classmethod
    def open(cls, path, leveldb_book=None):
        level_db_book_present = False
        if leveldb_book is not None:
            level_db_book_present = True
        pgn_file = PgnFile()
        leveldb_start_index = 0
        current_game = None
        in_tags = False
        game_num = 0
        for line in open(path, 'r'):
            # Decode and strip the line.
            line = line.decode('latin-1').strip()
#            line = line.strip()
            # Skip empty lines and comments.
            if not line or line.startswith("%"):
                continue

            # Check for tag lines.
            tag_match = tag_regex.match(line)
            if tag_match:
                tag_name = tag_match.group(1)
                tag_value = tag_match.group(2).replace("\\\\", "\\").replace("\\[", "]").replace("\\\"", "\"")
                if current_game:
                    if in_tags:
                        current_game.headers[tag_name] = tag_value
                    else:
                        # if game_num <2220:
                        #     continue
                        cls.__parse_movetext(current_game, movetext, game_num=game_num, leveldb=leveldb_book)
                        if game_num % 10 == 0:
                            print "Processing game:{0}".format(game_num)
                        # if game_num % 1000 == 0 and level_db_book_present:
                        #     pgn_file = cls.write_to_leveldb(game_num, leveldb_book, leveldb_start_index, pgn_file)
                        # else:
                        if not level_db_book_present:
                            pgn_file.add_game(current_game)
                        current_game = None
                        game_num += 1

                if not current_game:
                    current_game = chess.Game()
                    current_game.headers[tag_name] = tag_value
                    movetext = ""
                in_tags = True
            # Parse movetext lines.
            else:
                if current_game:
                    movetext += "\n" + line
                    pass
                else:
                    raise chess.PgnError("Invalid PGN. Expected header before movetext: %s", repr(line))
                in_tags = False

        if current_game:
            cls.__parse_movetext(current_game, movetext, game_num=game_num, leveldb=leveldb_book)
            if not level_db_book_present:
                pgn_file.add_game(current_game)

        # if level_db_book_present:
        #     pgn_file = cls.write_to_leveldb(game_num, leveldb_book, leveldb_start_index, pgn_file)

        return pgn_file

    @classmethod
    def open_text(cls, text):
        pgn_file = PgnFile()
        current_game = None
        in_tags = False

        for i, line in enumerate(text):
            # print line
            # Decode and strip the line.
            line = line.decode('latin-1').strip()
            # print line

            if i == 0 and not line.startswith('[') and line.endswith(']'):
                line = "[" + line
            # print line
            # Skip empty lines and comments.
            if not line or line.startswith("%"):
                continue

            # Check for tag lines.
            tag_match = tag_regex.match(line)
            if tag_match:
                tag_name = tag_match.group(1)
                tag_value = tag_match.group(2).replace("\\\\", "\\").replace("\\[", "]").replace("\\\"", "\"")
                if current_game:
                    if in_tags:
                        current_game.headers[tag_name] = tag_value
                    else:
                        cls.__parse_movetext(current_game, movetext)
                        pgn_file.add_game(current_game)
                        current_game = None
                if not current_game:
                    current_game = chess.Game()
                    current_game.headers[tag_name] = tag_value
                    movetext = ""
                in_tags = True
            # Parse movetext lines.
            else:
                if current_game:
                    movetext += "\n" + line
                    pass
                else:
                    raise chess.PgnError("Invalid PGN. Expected header before movetext: %s", repr(line))
                in_tags = False

        if current_game:
            cls.__parse_movetext(current_game, movetext)
            pgn_file.add_game(current_game)

        return pgn_file
