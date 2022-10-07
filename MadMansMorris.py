from gettext import find
from operator import index
import numpy as np

import random

class Player():
    def __init__(self, piece_type):
        self.pieces_in_deck = 9
        self.pieces_on_board = 0

        self.piece_type = piece_type

        
        # if self.space == BoardSpace.EMPTY_SPACE:
        #     self.player_spaces.append(space)
        # else:
        #     print("invalid move, try again")
        #     # Player.set_piece(input())

class BoardSpace:
    INVALID_SPACE = -1
    EMPTY_SPACE = 0
    WHITE_SPACE = 1
    BLACK_SPACE = 2

    def __init__(self, space_name) -> None:
        self.state = BoardSpace.EMPTY_SPACE

        self.space_name = space_name
        self.neighbors = {}
    
    def add_neighbor(self, space):
        self.neighbors[space.space_name] = space
    
    def add_neighbors(self, spaces):
        for space in spaces:
            self.add_neighbor(space)



class Game():
    class Board:
        def __init__(self):
            self.COLUMN_ARRAY = ["A", "B", "C", "D", "E", "F", "G"]
            self.ROW_ARRAY = [1, 2, 3, 4, 5, 6, 7]

            invalid_spaces = ["A2", "A3", "A5", "A6", "G2", "G3", "G5", "G6",
            "B1", "B3", "B5", "B7", "F1", "F3", "F5", "F7", "C1", "C2"
            "C6","C7", "E1", "E2", "E6", "E7", "D4"]

            self.spaces = {}

            for row in self.ROW_ARRAY:
                for col in self.COLUMN_ARRAY:
                    space_name = col + str(row)

                    if space_name not in invalid_spaces:
                        self.spaces[space_name] = BoardSpace(space_name)
            
            self.spaces["A1"].add_neighbors([self.spaces["A4"], self.spaces["D1"]])
            self.spaces["A4"].add_neighbors([self.spaces["A1"], self.spaces["A7"], self.spaces["B4"]])
            self.spaces["A7"].add_neighbors([self.spaces["A4"], self.spaces["D7"]])

            self.spaces["B2"].add_neighbors([self.spaces["B4"], self.spaces["D2"]])
            self.spaces["B4"].add_neighbors([self.spaces["A4"], self.spaces["B2"], self.spaces["B2"], self.spaces["C4"]])
            self.spaces["B6"].add_neighbors([self.spaces["B4"], self.spaces["D6"]])


            self.spaces["C3"].add_neighbors([self.spaces["C4"], self.spaces["D3"]])
            self.spaces["C4"].add_neighbors([self.spaces["B4"], self.spaces["C3"], self.spaces["C5"]])
            self.spaces["C5"].add_neighbors([self.spaces["C4"], self.spaces["D5"]])
            
            self.spaces["D5"].add_neighbors([self.spaces["C5"], self.spaces["E5"], self.spaces["D6"]])
            self.spaces["D6"].add_neighbors([self.spaces["B6"], self.spaces["D5"], self.spaces["F6"], self.spaces["D7"]])
            self.spaces["D7"].add_neighbors([self.spaces["A7"], self.spaces["D6"], self.spaces["G7"]])

            self.spaces["E5"].add_neighbors([self.spaces["E4"], self.spaces["D5"]])
            self.spaces["E4"].add_neighbors([self.spaces["E3"], self.spaces["E5"], self.spaces["F4"]])
            self.spaces["E3"].add_neighbors([self.spaces["E4"], self.spaces["D3"]])

            self.spaces["D3"].add_neighbors([self.spaces["C3"], self.spaces["D2"], self.spaces["E3"]])
            self.spaces["D2"].add_neighbors([self.spaces["D3"], self.spaces["B2"], self.spaces["D1"], self.spaces["F2"]])
            self.spaces["D1"].add_neighbors([self.spaces["A1"], self.spaces["D2"], self.spaces["G1"]])

            self.spaces["F2"].add_neighbors([self.spaces["F4"], self.spaces["D2"]])
            self.spaces["F4"].add_neighbors([self.spaces["F2"], self.spaces["E4"], self.spaces["F6"], self.spaces["G4"]])
            self.spaces["F6"].add_neighbors([self.spaces["F4"], self.spaces["D6"]])

            self.spaces["G4"].add_neighbors([self.spaces["G4"], self.spaces["G7"], self.spaces["F4"]])
            self.spaces["G1"].add_neighbors([self.spaces["G4"], self.spaces["D1"]])
            self.spaces["G7"].add_neighbors([self.spaces["G4"], self.spaces["D7"]])
            
            
            for space in invalid_spaces:
                self.set_space_value(space, BoardSpace.INVALID_SPACE)
        
        def set_space_value(self, space, value):
            if self.get_space(space) == BoardSpace.EMPTY_SPACE:
                self.spaces[space].state = value


        def get_space(self, space_name):
            if space_name in self.spaces:
                return self.spaces[space_name].state
            else:
                return BoardSpace.INVALID_SPACE

    def __init__(self):
        self.unplayed_pieces = 9
        self.board = Game.Board()

        self.white_player = Player(BoardSpace.WHITE_SPACE)
        self.black_player = Player(BoardSpace.BLACK_SPACE)

        self.board = Game.Board()

        self.coin_toss()
    
    def coin_toss(self):
        if random.randint(0, 1) == 0:
            self.current_player = self.white_player
        else:
            self.current_player = self.black_player

    def place_piece(self, space):
        if self.board.get_space(space) != BoardSpace.EMPTY_SPACE:
            return
        
        if self.current_player.pieces_in_deck > 0:
            self.board.set_space_value(space, self.current_player.piece_type)
            self.current_player.pieces_in_deck -= 1

            self.current_player.pieces_on_board +=
        
            self.change_player()
        
    
    def move_piece(self, start_space_name, end_space_name):
        if self.current_player.pieces_in_deck > 0:
            return

        start_space = self.board.get_space(start_space_name)
        end_space = self.board.get_space(end_space_name)

        if start_space != self.current_player.piece_type:
            return
        
        
        if end_space != BoardSpace.EMPTY_SPACE:
            return

        if end_space_name not in self.board.spaces[start_space_name].neighbors and self.current_player.pieces_on_board > 3:    
            return
        
        
        self.board.spaces[start_space_name].state = BoardSpace.EMPTY_SPACE
        self.board.spaces[end_space_name].state = self.current_player.piece_type

        self.change_player()



    def change_player(self):
        if self.current_player == self.white_player:
            self.current_player = self.black_player

        elif self.current_player == self.black_player:
            self.current_player = self.white_player



game = Game()