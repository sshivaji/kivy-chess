import unittest

import sys; sys.path.extend(['../', './'])
from position import Position
from move import Move
from notation import SanNotation
from piece import WHITE, BLACK
from fen import Fen
from game import Game

class TestGame(unittest.TestCase):

#    def setUp(self):
#        pass
#        self.game = Game()
#        self.pos_dup = Position()
#        self.pos_other = Position()
#        self.pos_other.make_move(Move.from_uci('e2e4'))



    def test_move_list(self):
        root = Game()
        variation = root.add_main_variation(Move.from_uci("e2e4"))
        assert len(root) == 1
        assert root[Move.from_uci("e2e4")] == variation
        assert root[0] == variation

        next_var = variation.add_main_variation(Move.from_uci("c7c5"))
        assert next_var.get_prev_moves() == "  e2e4 c7c5"
        assert next_var.get_prev_moves(format="san") == "  e2e4 c5"
        root.game_score()

if __name__ == '__main__':
    unittest.main()
