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
from Queue import PriorityQueue, Queue
from Queue import Empty

import chess
import chess.pgn
import heapq
import os
import unittest
import leveldb
import time
from leveldict import LevelJsonDict
from collections import Counter, defaultdict, OrderedDict
from itertools import islice, izip, tee
import operator

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

class DBSortCriteria(object):
    def __init__(self, key, rank, asc, **kwargs):
        self.key = key
        self.rank = rank
        self.asc = asc

class DBGame(object):
    def __init__(self, id, **kwargs):
        self.id = id

    def __repr__(self):
        return "{0} {1} - {2} {3} {4} {5} {6}\n".format(self.white, self.whiteelo, self.black, self.blackelo, self.result, self.date, self.site)

class PlanPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item
    def get_nowait(self, *args, **kwargs):
        item = PriorityQueue.get_nowait(self, *args, **kwargs)
        # print item
        return item


class OpeningTestCase(unittest.TestCase):

    def get_game_header(self, db_index, g, header, first_line=False):

        try:

            record = db_index.Get("game_{0}_data".format(g))
            if header == "ALL":
                return record
            text = ""
            text = record.split("|")[DB_HEADER_MAP[header]]
            # try:
            #     j = json.loads(record, "latin-1")
            #     text = j[header]
            # except UnicodeDecodeError:
            #     print record
            # except ValueError:
            #     print record
            #     j = json.loads(repair_json(record), "latin-1")
            #     text = j[header]

            # text = self.db_index_book.Get("game_{0}_{1}".format(g,header))
            if first_line:
#                text = self.pgn_index["game_index_{0}".format(g)][header]
                if "," in text:
                    return text.split(",")[0]
            return text
#            return self.pgn_index["game_index_{0}".format(g)][header]
        except KeyError:
            return "Unknown"

    def get_game_headers(self, db_index, pos_hash, create_headers = False, db_filter_field = None, db_sort_criteria = None):
        try:
            game_ids = db_index.Get(pos_hash).split(',')[:-1]
            # print "frequency: {0}".format(db_index.Get(pos_hash+"_freq"))
            # print "score: {0}".format(db_index.Get(pos_hash+"_score"))
            # print "draws: {0}".format(db_index.Get(pos_hash+"_draws"))
            # print "moves: {0}".format(db_index.Get(pos_hash+"_white_score"))

        except KeyError, e:
            print "key not found!"
            game_ids = []
        db_game_list = []
        filter_text = []
        db_operator = ["-", " "]
        db_text = db_filter_field
        if db_text:
            operator_match = False
            for op in db_operator:
                if op in db_text:
                    filter_tokens = db_text.split(op)
                    for i, f in enumerate(filter_tokens):
                        filter_tokens[i] = f.strip()
                    filter_text = filter_tokens
                    operator_match = True
                    break
            if not operator_match:
                filter_text = [db_text]
        for i in game_ids:
            db_game = DBGame(i)
            record = self.get_game_header(db_index, i, "ALL")
            tokens = record.split("|")
            db_game.white = tokens[0]
            db_game.whiteelo = tokens[1]
            db_game.black = tokens[2]
            db_game.blackelo = tokens[3]
            db_game.result = tokens[4]
            db_game.date = tokens[5]
            db_game.event = tokens[6]
            db_game.site = tokens[7]
            db_game.eco = tokens[8]
            if len(filter_text) > 0:
                match = True
                # print filter_text
                for f in filter_text:
                    if f in db_game.white or f in db_game.black or f in db_game.event or f in db_game.site:
                        pass
                    else:
                        match = False
                if match:
                    db_game_list.append(db_game)
                    # db_game_list.append(db_game)
            else:
                db_game_list.append(db_game)
        if db_sort_criteria:
            # print self.db_sort_criteria[0].key
            sort_key = operator.attrgetter(db_sort_criteria[0].key)
            if db_sort_criteria[0].key == 'id':
                sort_key = lambda v: int(v.id)

            db_game_list = sorted(db_game_list, reverse=not db_sort_criteria[0].asc, key=sort_key)
        return db_game_list, game_ids

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

    def get_piece_str(self, piece):
        if piece == chess.KING:
            return "king"
        elif piece == chess.BISHOP:
            return "bishop"
        elif piece == chess.KNIGHT:
            return "knight"
        elif piece == chess.ROOK:
            return "rook"
        elif piece == chess.QUEEN:
            return "queen"
        elif piece == chess.PAWN:
            return "pawn"
            # print "\n"

            # print node.move
            # print node.board()

    def test_plans_pgn(self):
        # 131563

        db = leveldb.LevelDB('book/polyglot_index.db')
        start_fen = 'rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPPN1PPP/R1BQKBNR b KQkq - 1 3'
        b = chess.Bitboard(start_fen)
        pos_hash = str(b.zobrist_hash())

        # game_ids = db.Get(pos_hash).split(',')[:-1]
            # def get_game_headers(self, db_index, pos_hash, create_headers = False, db_filter_field = None, db_sort_criteria = None):
        db_sort_criteria = [DBSortCriteria('whiteelo', 1, True), DBSortCriteria('blackelo', 1, True)]
        db_sort_criteria = [DBSortCriteria('whiteelo', 1, True)]

        db_sort_criteria[0].asc = False
        # db_sort_criteria[1].asc = False

        game_list, game_ids = self.get_game_headers(db, pos_hash, db_sort_criteria=db_sort_criteria)


        # print db
        games = []
        for g in game_list[:50]:
            # print g
            games.append(self.get_game(db, int(g.id)))
        moves = defaultdict(Counter)
        # san_set = set()
        games1, games2 = tee(games, 2)

        for node in games1:
            # node = g
            # print node
            start = False
            # san_set &= san_set
            # game_moves = Counter()
            while node.variations:
                move = node.move
                if move:
                    # print move.from_square
                    # piece = node.parent.board().piece_type_at(move.from_square)
                    # print piece
                    # captured_piece = node.parent.board().piece_type_at(move.to_square) if move else NONE
                    # print node.board().fen()
                    fen = node.board().fen()
                    if start:
                        # print node.san()
                        moves[node.board().turn][node.san()] += 1

                        # san_set.add(node.san())
                    if fen == start_fen:
                        start = True

                    # print node.san()
                    # print "piece: {0}".format(self.get_piece_str(piece))

                    # if captured_piece:
                    #     print "captured piece: {0}".format(self.get_piece_str(captured_piece))

                node = node.variation(0)
            # if not moves:
            #     moves = game_moves
            # else:
            #     print moves
            #     print "game_moves: {0}".format(game_moves)
            #     moves = moves | game_moves
            # plans += Counter(izip(san, islice(san, 1, None)))

        # print moves.most_common(5)
        common_white_moves = moves[chess.BLACK].most_common(15)
        common_black_moves = moves[chess.WHITE].most_common(15)

        # print common_moves
        white_common_moves = [item[0] for item in common_white_moves]
        black_common_moves = [item[0] for item in common_black_moves]

        print "white plans: {0}".format(white_common_moves)
        print "black plans: {0}".format(black_common_moves)

        # plans = Counter()
        white_plans_priority = PlanPriorityQueue()
        black_plans_priority = PlanPriorityQueue()

        for node in games2:
            white_plans = OrderedDict()
            black_plans = OrderedDict()
            # game_plan_list = []
            # game_plans = Counter()
            headers = node.headers
            while node.variations:
                move = node.move
                if move:
                    # print node.san()
                    if node.san() in white_common_moves:
                        # print node.san()
                        # game_plan_list.append(node.san())
                        # game_plans[node.san()]+=1
                        white_plans[node.san()] = node.board().fullmove_number
                    elif node.san() in black_common_moves:
                        black_plans[node.san()] = node.board().fullmove_number
                node = node.variation(0)

            white_plans_priority.put((white_plans, headers), 1.0/len(white_plans))
            black_plans_priority.put((black_plans, headers), 1.0/len(black_plans))


            # if not plans:
            #     plans = game_plans
            # else:
            #     plans = plans | game_plans
            # print "white_plans: {0}".format(white_plans)
            # print "black_plans: {0}".format(black_plans)

        # print white_plans_priority[:5]
        # print len(white_plans_priority)
        for i in range(5):
            try:
                white_plan = white_plans_priority.get_nowait()
                # print white_plan
                sorted_white_plans = sorted(white_plan[0].items(), key=operator.itemgetter(1))
                print "white_plans: {0}".format(sorted_white_plans)

            except Empty:
                break

        for i in range(5):
            try:
                black_plan = black_plans_priority.get_nowait()
                sorted_black_plans = sorted(black_plan[0].items(), key=operator.itemgetter(1))
                print "black_plans: {0}".format(sorted_black_plans)
            except Empty:
                break
            # print
        # print white_plans_priority.get()
        # print white_plans_priority.get()

        # print white_plans_priority.get()

        # print black_plans_priority.get()


        # print plans

        # print san_set
        # print plans.most_common(5)
if __name__ == '__main__':
    unittest.main()
