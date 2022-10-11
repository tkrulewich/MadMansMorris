import unittest
import sys
from MadMansMorris import *

class NewGameTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    # AC 1.1 (Generate New Board)
    def test_board_creation(self):
        for space in self.game.board.spaces:
            self.assertEqual(self.game.board.spaces[space].state, BoardSpace.EMPTY_SPACE)
    
    def test_board_creation_deck_size(self):
        self.assertEqual(self.game.white_player.pieces_in_deck, 9)
        self.assertEqual(self.game.black_player.pieces_in_deck, 9)
    
    def test_invalid_row_access_out_of_bounds(self):
        space_state = self.game.board.get_space("H2")
        self.assertEqual(space_state, BoardSpace.INVALID_SPACE)

        space_state = self.game.board.get_space("A5")
        self.assertEqual(space_state, BoardSpace.INVALID_SPACE)
    
    def test_invalid_col_access_out_of_bounds(self):
        space_state = self.game.board.get_space("A9")
        self.assertEqual(space_state, BoardSpace.INVALID_SPACE)
    
    def test_invalid_space_within_bounds(self):
        space_state = self.game.board.get_space("A2")
        self.assertEqual(space_state, BoardSpace.INVALID_SPACE)
    
    def test_valid_white_move(self):
        if self.game.current_player != self.game.white_player:
            self.game.place_piece("A1")
    
        
        self.assertEqual(self.game.current_player, self.game.white_player)

        self.game.place_piece("G1")
        space = self.game.board.get_space("G1")

        self.assertEqual(space, BoardSpace.WHITE_SPACE)
    
    def test_space_has_correct_neighbors(self):
        self.assertTrue( "G4" in self.game.board.spaces["G1"].neighbors)
        self.assertTrue( "D1" in self.game.board.spaces["G1"].neighbors)

        self.assertTrue( "C4" in self.game.board.spaces["B4"].neighbors)
        self.assertTrue( "F6" in self.game.board.spaces["D6"].neighbors)
    
    def test_invalid_move_occupied_space(self):
        
        first_player = self.game.current_player
        
        self.game.place_piece("A1")

        second_player = self.game.current_player

        self.assertNotEqual(first_player, second_player)

        self.game.place_piece("A1")

        self.assertEqual(self.game.current_player, second_player)

        space_value = self.game.board.get_space("A1")

        if first_player == self.game.white_player:
            self.assertEqual(space_value, BoardSpace.WHITE_SPACE)
        else:
            self.assertEqual(space_value, BoardSpace.BLACK_SPACE)

        # self.assertEqual(self.game.current_player, first_player)

        # self.game.move_piece("A1", "D1")
        # self.assertEqual(self.game.current_player, second_player)

        # start_space = self.game.board.get_space("A1")
        # end_space = self.game.board.get_space("D1")

        # self.assertEqual(start_space, BoardSpace.EMPTY_SPACE)

        # self.assertEqual(end_space, first_player.piece_type)
    
    def test_fewer_pieces_remaining_after_valid_move(self):
        first_player = self.game.current_player
        first_player_pieces_at_start = first_player.pieces_in_deck

        self.game.place_piece("A1")

        second_player = self.game.current_player
        second_player_pieces_at_start = second_player.pieces_in_deck

        self.assertNotEqual(first_player, second_player)

        self.game.place_piece("A4")

        self.assertEqual(first_player.pieces_in_deck, first_player_pieces_at_start - 1)
        self.assertEqual(second_player.pieces_in_deck, second_player_pieces_at_start - 1)



class TestAllPiecesInDeckPlayedNoMills(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.first_player = self.game.current_player

        self.game.place_piece("A7")
        self.second_player = self.game.current_player

        self.game.place_piece("D7")

        self.game.place_piece("G7")
        self.game.place_piece("B6")

        self.game.place_piece("D6")
        self.game.place_piece("F6")
        
        self.game.place_piece("B4")
        self.game.place_piece("E4")

        self.game.place_piece("F4")   
        self.game.place_piece("G4")

        self.game.place_piece("G1")
        self.game.place_piece("D1")

        self.game.place_piece("A1")
        self.game.place_piece("A4")

        self.game.place_piece("B2")
        self.game.place_piece("D2")

        self.game.place_piece("D3")
        self.game.place_piece("F2")

    def test_valid_move_piece(self):
        self.game.move_piece("B4", "C4")

        self.assertEqual(self.game.board.get_space("B4"), BoardSpace.EMPTY_SPACE)
        self.assertEqual(self.game.board.get_space("C4"), self.first_player.piece_type)

        self.game.move_piece("E4", "E5")

        self.assertEqual(self.game.board.get_space("E4"), BoardSpace.EMPTY_SPACE)
        self.assertEqual(self.game.board.get_space("E5"), self.second_player.piece_type)
    
    def test_invalid_move_piece_non_adjacent_empty_space(self):
        self.game.move_piece("F4", "C5")

        self.assertNotEqual(self.game.board.get_space("F4"), BoardSpace.EMPTY_SPACE)
        self.assertEqual(self.game.board.get_space("C5"), BoardSpace.EMPTY_SPACE)
        
    
    def test_invalid_move_piece_non_adjacent_occupied_space(self):
        original_start_space_value = self.game.board.get_space("F4")
        original_goal_space_value = self.game.board.get_space("B6")

        self.game.move_piece("F4", "B6")

        self.assertEqual(self.game.board.get_space("F4"), original_start_space_value)
        self.assertEqual(self.game.board.get_space("B6"), original_goal_space_value)
    
    def test_horizontal_mill_formation(self):
        self.game.move_piece("D6", "D5")
        self.game.move_piece("D7", "D6")


    
    def test_vertical_mill_formation(self):
        self.game.move_piece("D3", "C3")
        self.game.move_piece("E4", "E3")
        self.game.move_piece("C3", "C4")
        self.game.move_piece("E3", "D3")


        self.game.move_piece("C3", "C4")
        self.game.move_piece("D3", "E3")
        self.game.move_piece("C4", "C3")
        self.game.move_piece("E3", "D3")
        
    

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )