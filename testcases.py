import unittest

class NewGameTests(unittest.TestCase):
    def setup(self):
        self.game = Game()

    def test_board_creation(self):
        for space in self.game.board.spaces:
            self.assertEqual(space, Game.Board.EMPTY_SPACE)
    
    def test_board_creation_deck_size(self):
        self.assertEqual(self.game.white_player.unplayed_pieces, 9)
        self.assertEqual(self.game.black_player.unplayed_pieces, 9)
    
    def test_invalid_row_access(self):
        space_state = self.game.getSpace("H2")
        self.assertEqual(space_state, Game.Board.INVALID_SPACE)
    
    def test_invalid_col_access(self):
        space_state = self.game.getSpace("A9")
        self.assertEqual(space_state, Game.Board.INVALID_SPACE)
    
    def test_valid_white_move(self):
        if self.game.current_player() != self.game.white_player:
            self.game.black_player.place_piece("A1")
    
        
        self.assertEqual(self.game.current_player(), self.game.white_player)

        self.game.white_player.place_piece("G1")
        space = self.game.board.GetSpace("G1")

        self.assertEqual(space, Game.Board.WHITE_SPACE)
    
    def test_invalid_move_occupied_space(self):
        
        first_player = self.game.current_player()
        first_player.place_piece("A1")

        second_player = self.game.current_player()

        self.assertNotEqual(first_player, second_player)

        second_player.place_piece("A1")

        self.assertEqual(self.game.current_player(), second_player)

        space_value = self.board.getSpace("A1")

        if first_player == self.game.board.white_player:
            self.assertEqual(space_value, Game.Board.WHITE_SPACE)
        else:
            self.assertEqual(space_value, Game.Board.BLACK_SPACE)




        
        
        

