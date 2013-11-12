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

import libchess as chess
import types

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

    def __init__(self, previous_node, move, nags=[], comment="",
                 start_comment=""):
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

            GameNode.positions[self.__position.fen] = self

        self.__nags = nags
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
                "Expected comment to be string, got: %s." % comment)
        self.__comment = value

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

    def walk_tree(self, variation, move, format="normal", score=""):
        move += 1

        for v in variation:
            if not v.is_main_variation():
                score+= "{0} ".format("(",)
            if move % 2 == 1:
                score+= "{0} ".format((move + 1)/2,)

            if format=="ref":
                score+="[ref={0}]".format(v.fen)

            if v.__san:
                score+= "{0} ".format(v.__san,)
            else:
                score+= "{0} ".format(v.move)

            if format=="ref":
                score+=" [/ref] "

            if v.__variations:
                score+=self.walk_tree(v.__variations, move, format=format)
            if not v.is_main_variation():
                score+= "{0} ".format(")",)
        return score

    def fill_header_entry(self, attr):
        if self.headers.headers.has_key(attr):
            return self.headers.headers[attr]

    def write_header(self, header_score, attr, definition=True):
        if self.fill_header_entry(attr):
            if definition:
                header_score += attr+": "
            header_score += self.fill_header_entry(attr)
            header_score += '\n'
        return header_score

    def get_headers(self):
        if not self.header_score:
            header_score = ''

            header_score = self.write_header(header_score, 'White', definition=False)
            header_score = self.write_header(header_score, 'WhiteElo', definition=False)
            header_score = self.write_header(header_score, 'Black', definition=False)
            header_score = self.write_header(header_score, 'BlackElo', definition=False)

            header_score = self.write_header(header_score, 'Result', definition=False)
            header_score = self.write_header(header_score, 'Round')
            header_score = self.write_header(header_score, 'Event')
            header_score = self.write_header(header_score, 'Site')
            header_score = self.write_header(header_score, 'Date')
            header_score = self.write_header(header_score, 'ECO')
            print "generating headers.."
            self.header_score = header_score

        return self.header_score


    def game_score(self, format="ref"):
        # print self.headers.headers
        return self.get_headers() + self.walk_tree(self.__variations, move=0, format=format)
