from gettext import find
from operator import index
import numpy as np

import random

class Player():
    def __init__(self, piece_type):
        self.unplayed_pieces = 9
        self.piece_type = piece_type

        
        # if self.space == Game.Board.EMPTY_SPACE:
        #     self.player_spaces.append(space)
        # else:
        #     print("invalid move, try again")
        #     # Player.set_piece(input())

class Game():
    class Board:
        INVALID_SPACE = -1
        EMPTY_SPACE = 0
        WHITE_SPACE = 1
        BLACK_SPACE = 2


        def __init__(self):
            self.spaces = []
            self.ROW_ARRAY = ["A", "B", "C", "D", "E", "F", "G"]
            self.COLUMN_ARRAY = [1, 2, 3, 4, 5, 6, 7]

            invalid_spaces = ["A2", "A3", "A5", "A6", "G2", "G3", "G5", "G6",
            "B1", "B3", "B5", "B7", "F1", "F3", "F5", "F7", "C1", "C2"
            "C6","C7", "E1", "E2", "E6", "E7", "D4"]

            for i in range(7):
                self.spaces.append([])
                for j in self.COLUMN_ARRAY:
                    self.spaces[i].append(self.EMPTY_SPACE)
            
            for space in invalid_spaces:
                self.set_piece(Game.Board.INVALID_SPACE, space)
        
        def set_piece(self, piece_type, space):
            if self.get_space(space) == Game.Board.EMPTY_SPACE:
                r, c = self.get_space_index(space)
                self.spaces[r][c] = piece_type
            
        def get_space_index(self, space_name):
            try:
                r = self.ROW_ARRAY.index(space_name[0])
            except:
                r = -1
            
            c = int(space_name[1]) - 1

            return (r, c)

        def get_space(self, spaceName):
            r, c = self.get_space_index(spaceName)

            if 0 <= r <= 6 and 0 <= c <=6:
                return self.spaces[r][c]
            else:
                return Game.Board.INVALID_SPACE

    def __init__(self):
        self.unplayed_pieces = 9
        self.board = Game.Board()

        self.white_player = Player(Game.Board.WHITE_SPACE)
        self.black_player = Player(Game.Board.BLACK_SPACE)

        self.board = Game.Board()

        self.coin_toss()
    
    def coin_toss(self):
        if random.randint(0, 1) == 0:
            self.current_player = self.white_player
        else:
            self.current_player = self.black_player

    def make_move(self, space):
        if self.board.get_space(space) != Game.Board.EMPTY_SPACE:
            return
            
        self.board.set_piece(self.current_player.piece_type, space)
        self.change_player()
    
    def move_piece(self, start_space_name, end_space_name):
        start_space = self.board.get_space(start_space_name)
        end_space = self.board.get_space(end_space_name)

        if start_space != self.current_player.piece_type:
            return
        
        if end_space != Game.Board.EMPTY_SPACE:
            return
        
        self.board.set_piece(start_space_name, Game.Board.EMPTY_SPACE)
        self.board.set_piece(end_space_name, self.current_player.piece_type)

        self.change_player()



    def change_player(self):
        if self.current_player == self.white_player:
            self.current_player = self.black_player

        elif self.current_player == self.black_player:
            self.current_player = self.white_player



game = Game()