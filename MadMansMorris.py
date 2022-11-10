from gettext import find
from operator import index
import numpy as np
import threading
import random
import time

# Player class takes the piece_type(white or black) and an instance of the game and
# holds the variables for each player's pieces in the deck and their pieces on the board


class Player():
    def __init__(self, piece_type, game):
        self.pieces_in_deck = 9
        self.pieces_on_board = 0
        
        self.piece_type = piece_type
        self.game = game

    def take_turn(self):
        pass

# ComputerPlayer is created as a subclass of Player as we will be
# using all of the Player class variables when a computer player is called
# AND we are extending the functionality, specifically the "take_turn()" method

class ComputerPlayer(Player):
    def __init__(self, piece_type, game):
        super().__init__(piece_type, game)

    def take_turn(self):
        spaces = list(self.game.board.spaces.keys())
        while self.game.current_player == self:
            # this is where the computer will take its turn
            if self.game.game_state == Game.PLACE_PIECE:
                self.game.place_piece(random.choice(spaces))
            elif self.game.game_state == Game.REMOVE_PIECE:
                self.game.remove_piece(random.choice(spaces))
            elif self.game.game_state == Game.MOVE_PIECE:
                self.game.move_piece(random.choice(spaces), random.choice(spaces))


# MoveRecord class is created to keep an array of information on each play that is made
# in order to improve functionality of the computerplayer and can also be used to implement
# an undo button along with other potential functionality 
            
class MoveRecord():
    def __init__(self, move_type, player : Player, from_space: str, to_space : str = ""):
        self.move_type = move_type
        self.player = player
        self.from_space = from_space
        self.to_space = to_space
    
    def __str__(self) -> str:
        player_name : str = "BLACK" if self.player.piece_type == BoardSpace.BLACK_SPACE else "WHITE"
        return f"{player_name} {self.move_type} {self.from_space} {self.to_space}"

# Each instance of the BoardSpace class cotains the information of the state of each space in the 7x7 grid.
# The variables and methods are used to indicate valid and invalid spaces as well as valid neighbors of 
# valid spaces.  Instances of the boardspace class will be created and referenced in the Game class.

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

#The main game logic is contained within the Game class

class Game():
    class Board:
        # Creating a 7x7 game board and identifying the invalid spaces within the grid. Once the BoardSpaces
        # have been added to the spaces array, add_neighbors identifies each individual space's neighbors and
        # the information is stored to limit the players to only valid moves 
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

        # set_space_value and get_space are used to modify and return the state of each BoardSpace
        # (Invalid space, empty space, taken by white player or taken by black player) 
        def set_space_value(self, space, value):
            if space in self.spaces:
                self.spaces[space].state = value


        def get_space(self, space_name):
            if space_name in self.spaces:
                return self.spaces[space_name].state
            else:
                return BoardSpace.INVALID_SPACE
    
    # 4 different game state variables 
    GAME_OVER : int = -1            # The game has ended, one of the players has one or there was a draw
    PLACE_PIECE: int = 0            # The player is able to move their piece to any valid space
    MOVE_PIECE: int = 1             # The player is able to move their piece to only the BoardSpace's neighbors
    REMOVE_PIECE: int = 2           # The player is able to remove an opponent's piece

    # Initializing the default game type as Human v. Human.  These variables can be changed on the main
    # menu to Human v. Computer or Computer v. Computer 
    def __init__(self, white_player_human : bool = True, black_player_human : bool = True):
        self.unplayed_pieces = 9
        self.board = Game.Board()

        self.white_player = Player(BoardSpace.WHITE_SPACE, self) if white_player_human else ComputerPlayer(BoardSpace.WHITE_SPACE, self)
        self.black_player = Player(BoardSpace.BLACK_SPACE, self) if black_player_human else ComputerPlayer(BoardSpace.BLACK_SPACE, self)

        self.current_player : Player = None
        self.next_player : Player = None

        self.move_history : list[MoveRecord] = []

        self.coin_toss()

        self.game_state = Game.PLACE_PIECE

        self.current_player.take_turn()

    # A basic randomization function to select which player starts first
    def coin_toss(self) -> Player:
        if random.randint(0, 1) == 0:
            self.current_player = self.white_player
            self.next_player = self.black_player
        else:
            self.current_player = self.black_player
            self.next_player = self.white_player

    # The check_for_mill method determines whether or not a selected piece is part of a formed mill,
    # needed when presented with two circumstances:
    # when the current player forms a mill with their move, enabling them to remove the opponent's piece
    # when the opponent player's piece is part of a formed mill if the current player tries to remove it 

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
    
    # place_piece sets up the logic for the beginning of the game when the pieces are not yet all on the board
    # and for when either/both players end up with 3 pieces on the board 

    def place_piece(self, space_name):
        if self.game_state != Game.PLACE_PIECE:
            return
        
        if self.board.get_space(space_name) != BoardSpace.EMPTY_SPACE:
            return

        # log piece placement
        self.move_history.append(MoveRecord("PLACE", self.current_player, space_name))
        
        # For the beginning of the game when players are placing each of their 9 pieces on the board
        if self.current_player.pieces_in_deck > 0:
            self.current_player.pieces_in_deck -= 1
            self.current_player.pieces_on_board += 1

            self.board.set_space_value(space_name, self.current_player.piece_type)

            if self.check_for_mill(space_name):
                self.game_state = Game.REMOVE_PIECE
            else:
                self.change_player()

    # Method remove_piece is called when player forms a mill
    
    def remove_piece(self, space_name):
        if self.game_state != Game.REMOVE_PIECE:
            return
        
        state = self.board.get_space(space_name)
        if (self.board.get_space(space_name) != self.next_player.piece_type):
            return
        
        if (self.check_for_mill(space_name)):
            return
        
        # log piece removal
        self.move_history.append(MoveRecord("REMOVE", self.current_player, space_name))
        
        self.board.set_space_value(space_name, BoardSpace.EMPTY_SPACE)
        self.current_player.formed_mill_this_turn = False

        self.next_player.pieces_on_board -= 1
        self.change_player()

    # The "main" part of the game largely utilizes the move_piece function, which limits the player's 
    # movement to only the empty, neighboring and valid spaces.  

    def move_piece(self, start_space_name, end_space_name):
        if self.game_state != Game.MOVE_PIECE:
            return

        if self.current_player.pieces_in_deck > 0:
            return

        #variables relevant to move_history
        start_space = self.board.get_space(start_space_name)
        end_space = self.board.get_space(end_space_name)

        if start_space != self.current_player.piece_type:
            return
                
        if end_space != BoardSpace.EMPTY_SPACE:
            return

        if end_space_name not in self.board.spaces[start_space_name].neighbors and self.current_player.pieces_on_board > 3:    
            return
        
        # log piece movement
        self.move_history.append(MoveRecord("MOVE", self.current_player, start_space_name, end_space_name))
        
        self.board.spaces[start_space_name].state = BoardSpace.EMPTY_SPACE
        self.board.spaces[end_space_name].state = self.current_player.piece_type

        if self.check_for_mill(end_space_name):
            self.game_state = Game.REMOVE_PIECE
        else:
            self.change_player()

    # change_player is called at the end of each move to swap current_player and next_player and to 
    # return the current game_state 
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
        
        threading.Thread(target=self.current_player.take_turn).start()
