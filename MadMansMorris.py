from gettext import find
from operator import index
import numpy as np

import random

class Player():
    def __init__(self, piece_type):
        self.unplayed_pieces = 9
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



class Game():
    class Board:


        def __init__(self):
            self.ROW_ARRAY = ["A", "B", "C", "D", "E", "F", "G"]
            self.COLUMN_ARRAY = [1, 2, 3, 4, 5, 6, 7]

            invalid_spaces = ["A2", "A3", "A5", "A6", "G2", "G3", "G5", "G6",
            "B1", "B3", "B5", "B7", "F1", "F3", "F5", "F7", "C1", "C2"
            "C6","C7", "E1", "E2", "E6", "E7", "D4"]

            self.spaces = {}

            for row in self.ROW_ARRAY:
                for col in self.COLUMN_ARRAY:
                    space_name = row + str(col)

                    if space_name not in invalid_spaces:
                        self.spaces[space_name] = BoardSpace(space_name)
            
            
            for space in invalid_spaces:
                self.set_piece(BoardSpace.INVALID_SPACE, space)
        
        def set_piece(self, piece_type, space):
            if self.get_space(space) == BoardSpace.EMPTY_SPACE:
                self.spaces[space].state = piece_type
                
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

    def make_move(self, space):
        if self.board.get_space(space) != BoardSpace.EMPTY_SPACE:
            return
            
        self.board.set_piece(self.current_player.piece_type, space)
        self.change_player()
    
    def move_piece(self, start_space_name, end_space_name):
        start_space = self.board.get_space(start_space_name)
        end_space = self.board.get_space(end_space_name)

        if start_space != self.current_player.piece_type:
            return
        
        if end_space != BoardSpace.EMPTY_SPACE:
            return
        
        self.board.set_piece(start_space_name, BoardSpace.EMPTY_SPACE)
        self.board.set_piece(end_space_name, self.current_player.piece_type)

        self.change_player()



    def change_player(self):
        if self.current_player == self.white_player:
            self.current_player = self.black_player

        elif self.current_player == self.black_player:
            self.current_player = self.white_player



game = Game()