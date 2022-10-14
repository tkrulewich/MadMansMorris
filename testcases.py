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
    
    # AC 1.2 (Generate New Deck)
    def test_board_creation_deck_size(self):
        self.assertEqual(self.game.white_player.pieces_in_deck, 9)
        self.assertEqual(self.game.black_player.pieces_in_deck, 9)
    
    # AC 1.3 (Test Invalid Row Access Out of Bounds)
    def test_invalid_row_access_out_of_bounds(self):
        space_state = self.game.board.get_space("H2")
        self.assertEqual(space_state, BoardSpace.INVALID_SPACE)

        space_state = self.game.board.get_space("A5")
        self.assertEqual(space_state, BoardSpace.INVALID_SPACE)
    
    # AC 1.4 (Test Invalid Column Access Out of Bounds)
    def test_invalid_col_access_out_of_bounds(self):
        space_state = self.game.board.get_space("A9")
        self.assertEqual(space_state, BoardSpace.INVALID_SPACE)
    
    # AC 1.5 (Test Invalid Space Access Within Bounds)
    def test_invalid_space_within_bounds(self):
        space_state = self.game.board.get_space("A2")
        self.assertEqual(space_state, BoardSpace.INVALID_SPACE)
    
    # AC 2.1 (Test Place White Piece)
    def test_white_player_valid_piece_placement(self):
        if self.game.current_player != self.game.white_player:
            self.game.place_piece("A1")
    
        self.assertTrue(self.game.current_player.pieces_in_deck > 0)
        self.assertEqual(self.game.current_player, self.game.white_player)

        self.game.place_piece("G1")
        space = self.game.board.get_space("G1")

        self.assertEqual(space, BoardSpace.WHITE_SPACE)
    
    # AC 2.2 (Test Place Black Piece)
    def test_black_player_valid_piece_placement(self):
        if self.game.current_player != self.game.black_player:
            self.game.place_piece("A1")
    
        
        self.assertEqual(self.game.current_player, self.game.black_player)

        self.game.place_piece("G1")
        space = self.game.board.get_space("G1")

        self.assertEqual(space, BoardSpace.BLACK_SPACE)
    

    def test_space_has_correct_neighbors(self):
        self.assertTrue( "G4" in self.game.board.spaces["G1"].neighbors)
        self.assertTrue( "D1" in self.game.board.spaces["G1"].neighbors)

        self.assertTrue( "C4" in self.game.board.spaces["B4"].neighbors)
        self.assertTrue( "F6" in self.game.board.spaces["D6"].neighbors)
    
    # AC 2.3 (Test Invalid White Move - Space Occupied)
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
    
    # AC 2.4 (Illegal Move - Out of Bounds)
    def test_invalid_move_out_of_bounds(self):
        first_player = self.game.current_player
        first_player_pieces_in_deck_at_start = first_player.pieces_in_deck
        first_player_pieces_on_board_at_start = first_player.pieces_on_board


        self.game.place_piece("A9")

        self.assertEqual(first_player.pieces_in_deck, first_player_pieces_in_deck_at_start)
        self.assertEqual(self.game.current_player.pieces_on_board, first_player_pieces_on_board_at_start)
        self.assertEqual(self.game.current_player, first_player)
        self.assertEqual(self.game.board.get_space("A9"), BoardSpace.INVALID_SPACE)

    def test_fewer_pieces_remaining_in_deck_after_valid_move(self):
        first_player = self.game.current_player
        first_player_pieces_at_start = first_player.pieces_in_deck

        self.game.place_piece("A1")

        second_player = self.game.current_player
        second_player_pieces_at_start = second_player.pieces_in_deck

        self.assertNotEqual(first_player, second_player)

        self.game.place_piece("A4")

        self.assertEqual(first_player.pieces_in_deck, first_player_pieces_at_start - 1)
        self.assertEqual(second_player.pieces_in_deck, second_player_pieces_at_start - 1)
    
    # AC 3.0 (Flying a Piece)
    def test_flying_a_piece(self):
        first_player = self.game.current_player   
        self.game.place_piece("A7")

        second_player = self.game.current_player
        self.game.place_piece("B6")

        self.game.place_piece("A4")
        self.game.place_piece("B4")
        self.game.place_piece("A1")
        self.game.remove_piece("B4")

        self.game.place_piece("D6")
        self.game.place_piece("D7")
        self.game.place_piece("B2")
        self.game.place_piece("G7")
        self.game.remove_piece("B2")

        self.game.place_piece("B2")
        self.game.place_piece("F2")
        self.game.place_piece("F4")
        self.game.place_piece("G1")
        self.game.place_piece("D2")
        self.game.place_piece("D1")
        self.game.remove_piece("D2")

        self.game.place_piece("D2")
        self.game.place_piece("G4")
        self.game.remove_piece("D2")

        self.game.place_piece("D2")

        self.game.move_piece("A4", "B4")
        self.game.move_piece("D6", "D5")
        
        self.game.move_piece("B4", "A4")
        self.game.remove_piece("B6")

        self.game.move_piece("D5", "D6")
        self.game.move_piece("A4", "B4")
        self.game.move_piece("D2", "D3")
        self.game.move_piece("B4", "A4")
        self.game.remove_piece("B2")

        # Now white has tjree pieces

        self.assertEqual(self.game.current_player.pieces_on_board, 3)

        # Now white should be able to fly

        self.game.move_piece("D3", "B6")

        self.assertEqual(self.game.board.get_space("B6"), second_player.piece_type)
    
    # AC 4.0 (Removing a piece)
    def test_remove_piece(self):
        first_player = self.game.current_player   
        self.game.place_piece("A7")

        second_player = self.game.current_player
        self.game.place_piece("B6")

        self.game.place_piece("A4")
        self.game.place_piece("B4")
        self.game.place_piece("A1")

        self.assertTrue(self.game.check_for_mill("A1"))

        self.game.remove_piece("B4")

        self.assertEqual(self.game.board.get_space("B4"), BoardSpace.EMPTY_SPACE)
    
    # AC 5.0 (Determine Game is Over)
    def test_game_over(self):
        first_player = self.game.current_player   
        self.game.place_piece("A7")

        second_player = self.game.current_player
        self.game.place_piece("B6")

        self.game.place_piece("A4")
        self.game.place_piece("B4")
        self.game.place_piece("A1")
        self.game.remove_piece("B4")

        self.game.place_piece("D6")
        self.game.place_piece("D7")
        self.game.place_piece("B2")
        self.game.place_piece("G7")
        self.game.remove_piece("B2")

        self.game.place_piece("B2")
        self.game.place_piece("F2")
        self.game.place_piece("F4")
        self.game.place_piece("G1")
        self.game.place_piece("D2")
        self.game.place_piece("D1")
        self.game.remove_piece("D2")

        self.game.place_piece("D2")
        self.game.place_piece("G4")
        self.game.remove_piece("D2")

        self.game.place_piece("D2")

        self.game.move_piece("A4", "B4")
        self.game.move_piece("D6", "D5")
        
        self.game.move_piece("B4", "A4")
        self.game.remove_piece("B6")

        self.game.move_piece("D5", "D6")
        self.game.move_piece("A4", "B4")
        self.game.move_piece("D2", "D3")
        self.game.move_piece("B4", "A4")
        self.game.remove_piece("B2")

        self.game.move_piece("F4", "E4")
        self.game.move_piece("G4", "F4")
        self.game.move_piece("E4", "E5")
        self.game.move_piece("F4", "G4")

        self.game.remove_piece("E5")

        self.assertTrue(self.game.game_state == Game.GAME_OVER)
    
    # AC 6.0 (Coin Toss Player Start)
    def test_starting_player_coin_toss(self):
        white_starts = 0
        black_starts = 0
        for i in range(1000):
            new_game = Game()
            if new_game.current_player == new_game.white_player:
                white_starts += 1
            elif new_game.current_player == new_game.black_player:
                black_starts += 1
        
        self.assertTrue(white_starts > 0)
        self.assertTrue(black_starts > 0)




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

    # AC 2.21 (Test Move Piece White Player)
    def test_white_player_valid_piece_movement(self):
        if self.game.current_player == self.game.white_player:
            self.game.move_piece("B4", "C4")

            self.assertEqual(self.game.board.get_space("B4"), BoardSpace.EMPTY_SPACE)
            self.assertEqual(self.game.board.get_space("C4"), self.game.white_player.piece_type)
        else:
            self.game.move_piece("B4", "C4")

            self.assertEqual(self.game.board.get_space("B4"), BoardSpace.EMPTY_SPACE)
            self.assertEqual(self.game.board.get_space("C4"), self.game.black_player.piece_type)


            self.game.move_piece("E4", "E5")

            self.assertEqual(self.game.board.get_space("E4"), BoardSpace.EMPTY_SPACE)
            self.assertEqual(self.game.board.get_space("E5"), self.game.white_player.piece_type)
    
    # AC 2.22 (Test Move Piece Black Player)
    def test_black_player_valid_piece_movement(self):
        if self.game.current_player == self.game.black_player:
            self.game.move_piece("B4", "C4")

            self.assertEqual(self.game.board.get_space("B4"), BoardSpace.EMPTY_SPACE)
            self.assertEqual(self.game.board.get_space("C4"), self.game.black_player.piece_type)
        else:
            self.game.move_piece("B4", "C4")

            self.assertEqual(self.game.board.get_space("B4"), BoardSpace.EMPTY_SPACE)
            self.assertEqual(self.game.board.get_space("C4"), self.game.white_player.piece_type)


            self.game.move_piece("E4", "E5")

            self.assertEqual(self.game.board.get_space("E4"), BoardSpace.EMPTY_SPACE)
            self.assertEqual(self.game.board.get_space("E5"), self.game.black_player.piece_type)

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
    
    # AC 3.1 (Forming a Horizontal Mill)
    def test_horizontal_mill_formation(self):
        self.game.move_piece("D6", "D5")
        self.game.move_piece("D7", "D6")

        self.assertEqual(self.game.check_for_mill("B6"), True)
        self.assertEqual(self.game.check_for_mill("D6"), True)
        self.assertEqual(self.game.check_for_mill("F6"), True)


    # AC 3.2 (Forming a Vertical Mill)    
    def test_vertical_mill_formation(self):
        self.game.move_piece("D3", "C3")
        self.game.move_piece("E4", "E5")
        self.game.move_piece("F4", "E4")
        self.game.move_piece("G4", "F4")

        self.assertEqual(self.game.check_for_mill("F6"), True)
        self.assertEqual(self.game.check_for_mill("F4"), True)
        self.assertEqual(self.game.check_for_mill("F2"), True)
    
        
    

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )