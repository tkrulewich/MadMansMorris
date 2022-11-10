from hashlib import blake2b
from http.cookiejar import DefaultCookiePolicy
from string import whitespace
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsView, QSizePolicy, QVBoxLayout, QHBoxLayout, QMenuBar
from PyQt6.QtWidgets import QLabel, QMessageBox, QGraphicsBlurEffect, QGraphicsColorizeEffect, QDialog, QPushButton, QToolButton
from PyQt6.QtGui import QBrush, QColor, QPen, QPainter, QPaintEvent, QMouseEvent, QFont, QPalette, QResizeEvent, QIcon, QAction
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QRect, Qt, pyqtSignal, QObject, QThread, QSize
from threading import Thread
import time

from collections import deque

import MadMansMorris

black_piece_render = QSvgRenderer("images/black_piece.svg")
black_piece_mill_render = QSvgRenderer("images/black_piece_mill.svg")

white_piece_render = QSvgRenderer("images/white_piece.svg")
white_piece_mill_render = QSvgRenderer("images/white_piece_mill.svg")

empty_space_render = QSvgRenderer("images/empty_space.svg")

class QBoardSpace(QGraphicsSvgItem):
    def __init__(self, board_space: MadMansMorris.BoardSpace, game: MadMansMorris.Game,board_renderer: 'GameWidget'):
        super().__init__()

        self.board_renderer = board_renderer

        self.board_space : MadMansMorris = board_space
        self.game : MadMansMorris = game
        self.update()

    def update(self):
        if self.board_space.state == MadMansMorris.BoardSpace.BLACK_SPACE:
            if self.game.check_for_mill(self.board_space.space_name):
                self.setSharedRenderer(black_piece_mill_render)
            else:
                self.setSharedRenderer(black_piece_render)
        elif self.board_space.state == MadMansMorris.BoardSpace.WHITE_SPACE:
            if self.game.check_for_mill(self.board_space.space_name):
                self.setSharedRenderer(white_piece_mill_render)
            else:
                self.setSharedRenderer(white_piece_render)
        else:
            self.setSharedRenderer(empty_space_render)
        
        self.x, self.y = self.__position_from_space_name(self.board_space.space_name)

        self.setPos(self.x * 100.0 -354.0 / 2.0, self.y * 100.0 - 354.0 / 2.0)

        self.setTransformOriginPoint(self.boundingRect().center())
        self.setScale(0.15)
    
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.board_renderer.space_clicked(self.board_space.space_name)
        return super().mousePressEvent(event)
    
    def __position_from_space_name(self, space_name: str):
        x = ord(space_name[0]) - 65
        y = 7 - int(space_name[1]) 
        return x, y
    

class HumanComputerToggleButton(QWidget):
    human_icon = QIcon("images/human.svg")
    computer_icon = QIcon("images/computer.svg")

    human_computer_signal = pyqtSignal()

    def __init__(self, player: str):
        super().__init__()

        self.human = True
        self.player = player

        self.button = QToolButton()
        self.button.setIcon(self.human_icon)
        self.button.setIconSize(QSize(50, 50))

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(30, 30, 30, 30)
        self.layout().setSpacing(0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(f"{self.player}")

        self.button.clicked.connect(self.toggle)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.button)

    def toggle(self):
        self.human = not self.human

        if self.human:
            self.button.setIcon(self.human_icon)
        else:
            self.button.setIcon(self.computer_icon)
        
        self.human_computer_signal.emit()
        


class MainMenuWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(QVBoxLayout())

        self.main_menu_instructions = QLabel("Welcome to Mad Man's Morris. Please select computer or human for each player.")
        self.main_menu_instructions.setStyleSheet("font-size: 20px;text-align: center;")

        self.player_toggles_layout = QHBoxLayout()
        self.player_toggles_layout.setContentsMargins(0, 0, 0, 0)
        self.player_toggles_layout.setSpacing(0)
        self.player_toggles_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)



        
        self.white_player_human_button = HumanComputerToggleButton("White Player")
        self.black_player_human_button = HumanComputerToggleButton("Black Player")

        self.player_toggles_layout.addWidget(self.white_player_human_button)
        self.player_toggles_layout.addWidget(self.black_player_human_button)

        self.white_player_human_button.human_computer_signal.connect(self.__computer_human_toggle_clicked)
        self.black_player_human_button.human_computer_signal.connect(self.__computer_human_toggle_clicked)
        
        self.white_player_human = True
        self.black_player_human = True

        self.start_game_button = QPushButton("Start Game")

        self.layout().addWidget(self.main_menu_instructions)
        self.layout().addLayout(self.player_toggles_layout)
        self.layout().addWidget(self.start_game_button)

    def __computer_human_toggle_clicked(self):
        self.white_player_human = self.white_player_human_button.human
        self.black_player_human = self.black_player_human_button.human

class GameOverWidget(QWidget):
    def __init__(self, winner):
        super().__init__()

        self.setLayout(QVBoxLayout())

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.winner_label = QLabel(f"{winner} wins!")
        self.winner_label.setFont(QFont("Arial", 20))
        

        self.play_again_button = QPushButton("Play Again")

        self.layout().addWidget(self.winner_label)
        self.layout().addWidget(self.play_again_button)
    

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self._create_menu_bar()

        self.setMinimumSize(600, 600)

        self.setWindowTitle("Mad Man's Morris")

        self.show_main_menu()

        self.new_game_widget : GameWidget = None
    
    def show_main_menu(self):
        self.main_menu_widget = MainMenuWidget()
        self.main_menu_widget.start_game_button.clicked.connect(self.start_game)
        
        self.setCentralWidget(self.main_menu_widget)
    
    def start_game(self):
        if self.new_game_widget is not None:
            self.clean_up()
        
        self.game = MadMansMorris.Game(self.main_menu_widget.white_player_human, self.main_menu_widget.black_player_human)
        self.game_widget = GameWidget(self.game)
        
        self.game_widget.board_monitor.game_over_signal.connect(self.game_over)
        self.setCentralWidget(self.game_widget)

    def game_over(self):
        current = self.game.current_player

        winner = "Black" if current == self.game.white_player else "White"

        self.game_over_widget = GameOverWidget(winner)
        self.game_over_widget.play_again_button.clicked.connect(self.show_main_menu)
        self.setCentralWidget(self.game_over_widget)
    
    def _create_menu_bar(self):
        self.menu_bar = QMenuBar()
        self.menu_bar.setNativeMenuBar(False)

        self.game_menu = self.menu_bar.addMenu("Game")

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

        self.new_game_action = QAction("New Game", self)

        self.game_menu.triggered.connect(self.show_main_menu)

        self.game_menu.addAction(self.new_game_action)
        self.game_menu.addAction(self.exit_action)


        self.setMenuBar(self.menu_bar)


class BoardUpdater(QThread):
    update_board_signal = pyqtSignal()
    game_over_signal = pyqtSignal()

    def __init__(self, game: MadMansMorris.Game):
        super().__init__()
        self.game = game
    
    def run(self):
        number_moves = 0
        while self.game.game_state != MadMansMorris.Game.GAME_OVER:
            if number_moves != len(self.game.move_history):
                self.update_board_signal.emit()
                number_moves = len(self.game.move_history)
            time.sleep(0.1)
        
        if self.game.game_state == MadMansMorris.Game.GAME_OVER:
            if self.game.turn_thead != None:
                # wait for thread to finish
                self.game.turn_thead.join()
            self.game_over_signal.emit()

class GameWidget(QWidget):
    def __init__(self, game: MadMansMorris.Game):
        super().__init__()

        self.game = game
        self.spaces_selected_stack = deque()

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.player_turn_text = QLabel("Player Turn: " )
        self.player_turn_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout().addWidget(self.player_turn_text)

        self.last_move_text = QLabel("Last Move: " )
        self.last_move_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout().addWidget(self.last_move_text)

        self.view = QGraphicsView()
        self.layout().addWidget(self.view)

        self.view.setFrameStyle(0)

        self.setStyleSheet("background-color: #FFFFFF; color: #000000; font-family: Arial; font-size: 20px;")

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.space_graphics = []

        self.draw_board()

        self.update_board()

        self.board_monitor = BoardUpdater(self.game)
        self.board_monitor.update_board_signal.connect(self.update_board)

        self.thread = QThread()
        # Step 4: Move worker to the thread
        self.board_monitor.moveToThread(self.thread)
        self.thread.started.connect(self.board_monitor.run)

        self.thread.start()
    
    def clean_up(self):
        self.thread.quit()
        self.thread.wait()

    def draw_board(self):
        self.scene.addRect(0, 0, 600, 600, QPen(QColor(0, 0, 0)))
        self.scene.addRect(100, 100, 400, 400, QPen(QColor(0, 0, 0)))
        self.scene.addRect(200, 200, 200, 200, QPen(QColor(0, 0, 0)))

        self.scene.addLine(300, 0, 300, 200, QPen(QColor(0, 0, 0)))
        self.scene.addLine(300, 400, 300, 600, QPen(QColor(0, 0, 0)))

        self.scene.addLine(0, 300, 200, 300, QPen(QColor(0, 0, 0)))
        self.scene.addLine(400, 300, 600, 300, QPen(QColor(0, 0, 0)))

        for row in range(7):
            self.scene.addText(str(7 - row), QFont("Arial", 20)).setPos(-60, row * 100 - 20)
        
        for col in range(7):
            self.scene.addText(chr(65 + col), QFont("Arial", 20)).setPos(col * 100 - 15, 640)

        for y in range(0, 7):
            for x in range(0, 7):
                space_name = chr(x + 65) + str(y + 1)
                if space_name in self.game.board.spaces:
                    self.scene.addEllipse(x * 100 - 6, y * 100 - 6, 12, 12, QPen(QColor(0, 0, 0)), QBrush(QColor(0, 0, 0)))
        
        for space in self.game.board.spaces.values():
            space_graphic = QBoardSpace(space, self.game, self)
            
            self.space_graphics.append(space_graphic)
            self.scene.addItem(space_graphic)
    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        return super().resizeEvent(a0)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        return super().mousePressEvent(a0)
    
    def update_board(self):
        self.player_turn_text.setText("Player Turn: " + ("Black" if self.game.current_player == self.game.black_player else "White"))
        for space_graphic in self.space_graphics:
            space_graphic.update()
        
        if len(self.game.move_history) > 0:
            self.last_move_text.setText("Last Move: " + str(self.game.move_history[-1]))

        self.scene.update()
        
        # self.scene.setSceneRect(self.scene.itemsBoundingRect())
        # self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        
    def space_clicked(self, space_name: str):
        if self.game.game_state == MadMansMorris.Game.GAME_OVER:
            return
        
        if type(self.game.current_player) == MadMansMorris.ComputerPlayer:
            return

        if self.game.game_state == MadMansMorris.Game.PLACE_PIECE:
            self.game.place_piece(space_name)
        elif self.game.game_state == MadMansMorris.Game.REMOVE_PIECE:
            self.game.remove_piece(space_name)
        elif self.game.game_state == MadMansMorris.Game.MOVE_PIECE:
            if len(self.spaces_selected_stack) == 0 and self.game.board.get_space(space_name) == MadMansMorris.BoardSpace.EMPTY_SPACE:
                return

            if len(self.spaces_selected_stack) == 0:
                self.spaces_selected_stack.append(space_name)
            elif len(self.spaces_selected_stack) == 1:

                if (self.spaces_selected_stack[0] == space_name):
                    self.spaces_selected_stack.pop()
                else:
                    self.game.move_piece(self.spaces_selected_stack[0], space_name)
                    self.spaces_selected_stack.clear()

app = QApplication([])

window = MainApplication()
window.show()

app.exec()