import unittest
from madmans import *

class NewGameTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_board_creation(self):
        for row in self.game.board.spaces:
            for space in row:
                if space != Game.Board.INVALID_SPACE:
                    self.assertEqual(space, Game.Board.EMPTY_SPACE)
                
                if space != Game.Board.EMPTY_SPACE:
                    self.assertEqual(space, Game.Board.INVALID_SPACE)
    
    def test_board_creation_deck_size(self):
        self.assertEqual(self.game.white_player.unplayed_pieces, 9)
        self.assertEqual(self.game.black_player.unplayed_pieces, 9)
    
    def test_invalid_row_access(self):
        space_state = self.game.board.get_space("H2")
        self.assertEqual(space_state, Game.Board.INVALID_SPACE)

        space_state = self.game.board.get_space("A5")
        self.assertEqual(space_state, Game.Board.INVALID_SPACE)
    
    def test_invalid_col_access(self):
        space_state = self.game.board.get_space("A9")
        self.assertEqual(space_state, Game.Board.INVALID_SPACE)
    
    def test_valid_white_move(self):
        if self.game.current_player != self.game.white_player:
            self.game.make_move("A1")
    
        
        self.assertEqual(self.game.current_player, self.game.white_player)

        self.game.make_move("G1")
        space = self.game.board.get_space("G1")

        self.assertEqual(space, Game.Board.WHITE_SPACE)
    
    def test_invalid_move_occupied_space(self):
        
        first_player = self.game.current_player
        
        self.game.make_move("A1")

        second_player = self.game.current_player

        self.assertNotEqual(first_player, second_player)

        self.game.make_move("A1")

        self.assertEqual(self.game.current_player, second_player)

        space_value = self.game.board.get_space("A1")

        if first_player == self.game.white_player:
            self.assertEqual(space_value, Game.Board.WHITE_SPACE)
        else:
            self.assertEqual(space_value, Game.Board.BLACK_SPACE)




        
        
        

if __name__ == '__main__':
    unittest.main()