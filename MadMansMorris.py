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
    INVALID_SPACE: int = -1
    EMPTY_SPACE: int = 0
    WHITE_SPACE: int = 1
    BLACK_SPACE: int = 2

    def __init__(self, space_name: str) -> None:
        self.state = BoardSpace.EMPTY_SPACE

        self.space_name :str = space_name
        self.neighbors : dict = {}
    
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
            "B1", "B3", "B5", "B7", "F1", "F3", "F5", "F7", "C1", "C2",
            "C6","C7", "E1", "E2", "E6", "E7", "D4", "C6"]

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
            self.spaces["B4"].add_neighbors([self.spaces["A4"], self.spaces["B2"], self.spaces["B6"], self.spaces["C4"]])
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

            self.spaces["G4"].add_neighbors([self.spaces["G1"], self.spaces["G7"], self.spaces["F4"]])
            self.spaces["G1"].add_neighbors([self.spaces["G4"], self.spaces["D1"]])
            self.spaces["G7"].add_neighbors([self.spaces["G4"], self.spaces["D7"]])
            
            
            for space in invalid_spaces:
                self.set_space_value(space, BoardSpace.INVALID_SPACE)
        
        def set_space_value(self, space, value):
            if space in self.spaces:
                self.spaces[space].state = value


        def get_space(self, space_name):
            if space_name in self.spaces:
                return self.spaces[space_name].state
            else:
                return BoardSpace.INVALID_SPACE
    
    GAME_OVER : int = -1
    PLACE_PIECE: int = 0
    MOVE_PIECE: int = 1
    REMOVE_PIECE: int = 2

    def __init__(self):
        self.unplayed_pieces = 9
        self.board = Game.Board()

        self.white_player = Player(BoardSpace.WHITE_SPACE)
        self.black_player = Player(BoardSpace.BLACK_SPACE)

        self.current_player : Player = None
        self.next_player : Player = None

        self.coin_toss()

        self.game_state = Game.PLACE_PIECE

    
    def coin_toss(self) -> Player:
        if random.randint(0, 1) == 0:
            self.current_player = self.white_player
            self.next_player = self.black_player
        else:
            self.current_player = self.black_player
            self.next_player = self.white_player

    def place_piece(self, space_name):
        if self.game_state != Game.PLACE_PIECE:
            return
        
        #make_mill = False
        if self.board.get_space(space_name) != BoardSpace.EMPTY_SPACE:
            return
        
        if self.current_player.pieces_in_deck > 0:
            self.current_player.pieces_in_deck -= 1
            self.current_player.pieces_on_board += 1

            self.board.set_space_value(space_name, self.current_player.piece_type)

            if self.check_for_mill(space_name):
                self.game_state = Game.REMOVE_PIECE
            else:
                self.change_player()
    
    
    def remove_piece(self, space_name):
        if self.game_state != Game.REMOVE_PIECE:
            return
        
        state = self.board.get_space(space_name)
        if (self.board.get_space(space_name) == self.current_player.piece_type or 
            self.board.get_space(space_name) == BoardSpace.EMPTY_SPACE):
            return
        
        if (self.check_for_mill(space_name)):
            return
        
        self.board.set_space_value(space_name, BoardSpace.EMPTY_SPACE)
        self.current_player.formed_mill_this_turn = False

        
        self.next_player.pieces_on_board -= 1
        self.change_player()

    
    def check_for_mill(self, space_name):
        if self.board.get_space(space_name) == BoardSpace.EMPTY_SPACE:
            return False

        space = self.board.spaces[space_name]

        visited_horizontal = set([space])
        visited_vertical = set([space])

        for neighbor in space.neighbors.values():
            if neighbor.state == space.state:
                # First letter of name changes on vertical movement, second number part on horizontal

                if neighbor.space_name[0] != space_name[0]:
                    direction = "horizontal"
                    visited_horizontal.add(neighbor)
                else:
                    direction = "vertical"
                    visited_vertical.add(neighbor)
                
                for neighbors_neighbor in neighbor.neighbors.values():
                    if neighbors_neighbor.state != space.state:
                        continue

                    # if we've already visited this neighbor skip it
                    if neighbors_neighbor in visited_vertical or neighbors_neighbor in visited_horizontal:
                        continue

                    if direction == "vertical":
                        # if the direction of movment changed skip this neighbor
                        if neighbors_neighbor.space_name[0] != space_name[0]:
                            continue

                        visited_vertical.add(neighbors_neighbor)
                    else:
                        # if the direction of movment changed skip this neighbor
                        if neighbors_neighbor.space_name[1] != space_name[1]:
                            continue

                        visited_horizontal.add(neighbors_neighbor)
        
        if len(visited_vertical) == 3:
            return True
        
        if len(visited_horizontal) == 3:
            return True
        
        return False




                


        
    
    def move_piece(self, start_space_name, end_space_name):
        if self.game_state != Game.MOVE_PIECE:
            return

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

        if self.check_for_mill(end_space_name):
            self.game_state = Game.REMOVE_PIECE
        else:
            self.change_player()



    def change_player(self):

        temp = self.current_player
        self.current_player = self.next_player
        self.next_player = temp
        
        if self.current_player.pieces_in_deck + self.current_player.pieces_on_board < 3:
            self.game_state = Game.GAME_OVER
            return
        
        if self.current_player.pieces_in_deck > 0:
            self.game_state = Game.PLACE_PIECE
        else:
            self.game_state = Game.MOVE_PIECE
