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
from Queue import Queue

import libchess as chess
import types

# Chess assistant free ttf map
PIECE_FONT_MAP = {
    "K": u'\u00a2',
    "Q": u'\u00a3',
    "B": u'\u00a5',
    "N": u'\u00a4',
    "R": u'\u00a6',
    "P": u'\u00a7'
}

NAG_TO_READABLE_MAP = {
    0: "",
    1: "!",
    2: "?",
    3: "!!",
    4: "??",
    5: "!?",
    6: "?!",
    10: "=",
    14: "+=",
    15: "=+",
    16: "+-",
    17: "-+",
    18: "+ -",
    19: "- +"
}

READABLE_TO_NAG_MAP = {v:k for k, v in NAG_TO_READABLE_MAP.iteritems()}

class GameNode(object):
    """A node in the tree of a game.

    :param previous_node:
        The parent node.
    :param move:
        The move that leads to the position of this node.
    :param nags:
        A list of numeric annotation glyphs. Defaults to no annotation
        glyphs.
    :param comment:
        The comment that goes along with the move. Defaults to no
        comment.
    :param start_comment:
        The first node of a variation can have a start comment.
        Defaults to no start comment.

    You can read the variations of the node as a dictionary. The key
    can be and index starting with `0` for the main variation or a
    move.

    >>> import chess
    >>> root = chess.GameNode(None, None)
    >>> variation = root.add_variation(chess.Move.from_uci("e2e4"))
    >>> len(root)
    1
    >>> assert root[chess.Move.from_uci("e2e4")] == variation
    >>> assert root[0] == variation
    >>> del root[0]
    >>> variation in root
    False
    >>> chess.Move.from_uci("e2e4") in root
    False
    """

    def __init__(self, previous_node, move, nags=None, comment="", start_comment=""):
        if not nags:
            nags = []
        self.__previous_node = previous_node
        self.__move = move

        self.__san = None
        self.header_score = None

        if previous_node:
            p = self.previous_node.position
            # print "move:"
            # print move
            try:
                move_info = p.make_move(move)
            except ValueError:
                print move
                raise
            self.__san = move_info.san
            self.half_move_num = previous_node.half_move_num + 1
        else:
            self.half_move_num = 1

        if move:
            self.__position = chess.Position(previous_node.position)
            self.__position.make_move(move)
#            print GameNode.positions

            GameNode.positions[str(self.__position.__hash__())] = self

        self.__nags = nags
        self.__evaluation = {}
        self.comment = comment
        self.start_comment = start_comment

        self.__variations = []

    @property
    def previous_node(self):
        """The previous node of the game."""
        return self.__previous_node

    @property
    def variations(self):
        """Return Variations"""
        return self.__variations

    @property
    def san(self):
        """The move that makes the position of this node from the
        previous node.
        """
        return self.__san


    @property
    def move(self):
        """The move that makes the position of this node from the
        previous node.
        """
        return self.__move

    @property
    def fen(self):
        return self.__position.fen

    @property
    def position(self):
        """A copy of the position."""
        return chess.Position(self.__position)

    @property
    def comment(self):
        """The comment. An empty string means no comment."""
        return self.__comment

    @comment.setter
    def comment(self, value):
        if not isinstance(value, basestring):
            raise TypeError(
                "Expected comment to be string, got: %s." % value)
        self.__comment = value

        # comment_lower = value.lower()
        # if comment_lower.find("medal") > -1:
        #     GameNode.interesting_positions.append(self)

    @property
    def start_comment(self):
        """The start comment of the variation.

        If the node is not the start of a variation it can not have a
        start comment.
        An empty string means no comment.
        """
        if self.can_have_start_comment():
            return self.__start_comment
        else:
            return ""

    @start_comment.setter
    def start_comment(self, value):
        if not isinstance(value, basestring):
            raise TypeError(
                "Expected start comment to be string, got: %s." % comment)

#        if value != "" and not self.can_have_start_comment():
#            raise ValueError("Game node can not have a start comment.")

        self.__start_comment = value

    @property
    def nags(self):
        """A list of numeric annotation glyphs."""
        return self.__nags

    @property
    def evaluation(self):
        """Position Evaluation map ('move_eval', and 'pos_eval' are keys)"""
        return self.__evaluation

    def set_eval(self, key, value):
        self.__evaluation[key] = value

    def get_prev_moves(self, format="raw"):
        if self.previous_node:
            if format == "raw":
                return self.previous_node.get_prev_moves() + [str(self.move)]
            else:
                return self.previous_node.get_prev_moves(format=format) + [self.__san]
        return []

    def can_have_start_comment(self):
        """:return: If the node can have a start comment.

        Only nodes that are at the start of a variation can have a
        start comment.
        """
        if self.__previous_node is None:
            return True
        else:
            return self.__previous_node.index(self) != 0

    def get_next_main_move(self):
        if len(self.__variations)>0:
            return self.__variations[0]

    def is_main_line(self):
        """:return: If the node is in the main line of the game."""
        if self.__previous_node is None:
            return True
        else:
            return (self.__previous_node.index(self) == 0 and
                    self.__previous_node.is_main_line())

    def is_main_variation(self):
        """Checks if the node is the main variation.

        :return:
            If the node is the main variation looking from the previous
            node.
        """
        if self.__previous_node is None:
            return True
        else:
            return self.__previous_node.index(self) == 0

    def __len__(self):
        return len(self.__variations)

    def __nonzero__(self):
        return True

    def __getitem__(self, key):
        if type(key) is types.IntType:
            return self.__variations[key]
        elif type(key) is chess.Move:
            for node in self.__variations:
                if node.move == key:
                    return node
            raise KeyError(key)
        else:
            raise TypeError("Expected integer or move as key, got: %s." % key)

    def __delitem__(self, key):
        if type(key) is chess.Move:
            for i, node in enumerate(self.__variations):
                if node.move == key:
                    key = i
                    break
            else:
                raise KeyError(key)
        if type(key) is types.IntType:
            del self.__variations[key]
        else:
            raise TypeError("Expected integer or move as key, got: %s." % key)

    def __iter__(self):
        for node in self.__variations:
            yield node.move

    def __contains__(self, item):
        if isinstance(item, GameNode):
            return item in self.__variations
        else:
            return item in [node.move for node in self.__variations]

    def index(self, variation):
        """:return: The index of a variation.

        :param variation:
            A game node or move to get the index of.
        """
        for i, node in enumerate(self.__variations):
            if node == variation or node.move == variation:
                return i
        raise ValueError("No such variation: %s." % repr(value))

    def promote(self, variation):
        """Moves a variation one up, if possible.

        :param variation:
            A game node or move to promote.
        """
        i = self.index(variation)
        if i > 0:
            old = self.__variations[i - 1]
            self.__variations[i - 1] = self.__variations[i]
            self.__variations[i] = old

    def demote(self, variation):
        """Moves a variation one down, if possible.

        :param variation:
            A game node or move to demote.
        """
        i = self.index(variation)
        if i < len(self._variations) - 1:
            old = self.__variations[i + 1]
            self.__variations[i + 1] = self.__variations[i]
            self.__variations[i] = old

    def promote_to_main(self, variation):
        """Makes one variation the main variation of the previous node.

        :param variation:
            The game node or move to promote to the main variation.
        """
        i = self.index(variation)
        new_mainline = self.__variations[i]
        del self.__variations[i]
        self.__variations.insert(0, new_mainline)

    def __prepare_variation(self, variation, force=False):
        if type(variation) is chess.Move:
            variation = GameNode(self, variation)
        if not force and variation.move in self:
            raise ValueError("Variation already in set: %s." % variation.move)
        if variation.previous_node != self:
            raise ValueError("Variation already has a parent.")
        return variation

    def add_variation(self, variation, force=False):
        """Appends a variation to the list of variations.

        :param variation:
            The game node or move to add.

        :return:
            The game node that has been added.
        """
        variation = self.__prepare_variation(variation, force=force)
        self.__variations.append(variation)
        return variation

    def add_main_variation(self, variation):
        """Adds a variation and makes it the main variation.

        :param variation:
            The game node or move to add.

        :return:
            The game node that has been added.
        """
        variation = self.__prepare_variation(variation)
        self.__variations.insert(0, variation)
        return variation

    def remove_variation(self, variation):
        """Removes a variation.

        :param variation:
            The game node or move to remove.
        """
        del self.__variations[self.index(variation)]


    def walk_tree_iterative(self, variation, move, format="normal", score="", figurine=False):
        score = u''
        q = [variation]
        # tree_depth = 1

        while len(q)>0:
            # move += 1
            n = q.pop()

            for el in n:

                    # tree_depth +=1

                if format == "ref":
                    font_size = 16-len(q)
                    if font_size < 10:
                        font_size = 10
                    score += "[ref={0}][size={1}]".format(el.__position.__hash__(), font_size)
                    if el.is_main_line():
                        score +="[b]"

                if not el.is_main_variation():
                    # score += " ("*tree_depth
                    score += "\n{0} {1} ".format(" "*len(q)*2, " (",)

                move = el.half_move_num
                if move % 2 == 0:
                    score += "{0}. ".format((move + 1)/2,)
                if el.__san:
                    san = el.__san.encode('utf-8')
                    if figurine:
                        for k, v in PIECE_FONT_MAP.iteritems():
                            san = san.replace(k, v)

                    score += u"{0} ".format(san,)
                else:
                    score += "{0} ".format(el.move)

                try:
                    # print "evaluation: "
                    # print el.evaluation
                    # print "nags:: "
                    # print el.nags
                    if el.evaluation.has_key("move_eval") or el.evaluation.has_key("pos_eval"):
                        el.__nags = []

                    if el.evaluation.has_key("move_eval"):
                        el.__nags.append(el.evaluation["move_eval"])
                        # score += "{0} ".format(el.evaluation["move_eval"])
                    if el.evaluation.has_key("pos_eval"):
                        el.__nags.append(el.evaluation["pos_eval"])

                        # score += "{0} ".format(el.evaluation["pos_eval"])
                    if el.nags:
                        for nag in el.nags:
                            if format == "file":
                                if nag:
                                    score += "${0} ".format(nag)
                            else:
                                if nag in NAG_TO_READABLE_MAP:
                                    score += "{0} ".format(NAG_TO_READABLE_MAP[nag])
                except UnicodeDecodeError, e:
                    print e

                try:
                    if el.comment:
                        if format == "file":
                            score += " {{{0}}} ".format(el.comment)
                        else:
                            score += "[color=3333ff]{0}[/color]".format(el.comment)
                except UnicodeEncodeError, e:
                    print e

                if not el.is_main_line() and len(el.__variations) == 0:
                    # print "move: {0} is a leaf".format(el.__san)
                    score += " )\n "
                    # len -=1

                if format == "ref":
                    score += " "
                    if el.is_main_line():
                        score +="[/b]"
                    score += "[/size][/ref] "

                if len(el)>0:
                    for v in el.__variations:
                        q.append([v])
                    # q.append(el.__variations)

                # print "move: {0}, variations: {1}, length: {2}".format(el.__san, el.__variations, len(el.__variations))

        # print score
        return score

    def fill_header_entry(self, attr):
        if self.headers.headers.has_key(attr):
            return self.headers.headers[attr]

    def write_header(self, header_score, attr, definition='hide_type', newline=True, force_new_line=False):
        if definition=='file':
            newline=True
            force_new_line = False
        if self.fill_header_entry(attr):
            if definition=='view':
                # header_score += attr+": "
                # if attr == 'Round':
                # header_score += attr+": "
                header_score += self.fill_header_entry(attr)
            elif definition == 'file':
                header_score += '['+attr+' "'+self.fill_header_entry(attr)+'"]'
            else:
                if attr == 'Round':
                    header_score += attr+": "
                header_score += self.fill_header_entry(attr)

            if newline:
                header_score += '\n'
            else:
                header_score += '   '
        else:
            if force_new_line:
                header_score += '\n'
        return header_score

    def get_headers(self, definition):
        if not self.header_score or definition=="file":
            header_score = ''

            header_score = self.write_header(header_score, 'White', definition=definition, newline=False)
            header_score = self.write_header(header_score, 'WhiteElo', definition=definition, force_new_line=True)
            header_score = self.write_header(header_score, 'Black', definition=definition, newline=False)
            header_score = self.write_header(header_score, 'BlackElo', definition=definition, force_new_line=True)

            header_score = self.write_header(header_score, 'Result', definition=definition)

            default_def = "hide_type"
            if definition == "file":
                default_def = "file"

            header_score = self.write_header(header_score, 'Round', definition=default_def)
            header_score = self.write_header(header_score, 'Event', definition=default_def)
            header_score = self.write_header(header_score, 'Site', definition=default_def)
            header_score = self.write_header(header_score, 'Date', definition=default_def)
            header_score = self.write_header(header_score, 'ECO', definition=default_def)
            # print "generating headers.."
            if definition=="file":
                return header_score

            self.header_score = header_score

        return self.header_score


    def game_score(self, format="ref", figurine=False):
        header = "view"
        if format == "file":
            header = "file"

        result = self.fill_header_entry('Result')
        if not result:
            result = '*'

        body = self.walk_tree_iterative(self.__variations, move=0, format=format, figurine=figurine)
        # if format == "file":
        #     body = re.sub("(.{80})", "\\1\n", body, 0, re.DOTALL)

        if format == "file":
            delimiter = '\n'
        else:
            delimiter = ''
            result = "[size=16][b][color=3333ff]"+result+"[/color][/b][/size]"

        return delimiter + self.get_headers(header) + delimiter + body + ' ' + result + delimiter
