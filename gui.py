from hashlib import blake2b
from http.cookiejar import DefaultCookiePolicy
from string import whitespace
<<<<<<< HEAD
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsView, QSizePolicy, QVBoxLayout
from PyQt6.QtWidgets import QLabel, QMessageBox, QGraphicsBlurEffect, QGraphicsColorizeEffect
=======
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsView, QSizePolicy, QVBoxLayout, QLabel,QGraphicsSceneMouseEvent
>>>>>>> 355a10ad10e727759faeb3af3702f2f730860963
from PyQt6.QtGui import QBrush, QColor, QPen, QPainter, QPaintEvent, QMouseEvent, QFont, QPalette, QResizeEvent
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QRect, Qt

import MadMansMorris


<<<<<<< HEAD
black_piece_render = QSvgRenderer("images/black_piece.svg")
black_piece_mill_render = QSvgRenderer("images/black_piece_mill.svg")

white_piece_render = QSvgRenderer("images/white_piece.svg")
white_piece_mill_render = QSvgRenderer("images/white_piece_mill.svg")

empty_space_render = QSvgRenderer("images/empty_space.svg")
=======
black_piece_render = QSvgRenderer("C:/Users/Adam/Desktop/CS_Shortcuts/MadMansMorris-main/MadMansMorris-main/images/black_piece.svg")
white_piece_render = QSvgRenderer("C:/Users/Adam/Desktop/CS_Shortcuts/MadMansMorris-main/MadMansMorris-main/images/white_piece.svg")
empty_space_render = QSvgRenderer("C:/Users/Adam/Desktop/CS_Shortcuts/MadMansMorris-main/MadMansMorris-main/images/empty_space.svg")
>>>>>>> 355a10ad10e727759faeb3af3702f2f730860963


class QBoardSpace(QGraphicsSvgItem):
    def __init__(self, board_space: MadMansMorris.BoardSpace, game: MadMansMorris.Game):
        super().__init__()

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

        # if self.game.check_for_mill(self.board_space.space_name):
        #     colorEffect = QGraphicsColorizeEffect()
        #     colorEffect.setColor(QColor(100, 100, 0, 200))
        #     self.setGraphicsEffect(colorEffect)
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
<<<<<<< HEAD
        if self.board_space.state == MadMansMorris.BoardSpace.EMPTY_SPACE:
            self.game.place_piece(self.board_space.space_name)
        elif self.board_space.state != self.game.current_player.piece_type:
            self.game.remove_piece(self.board_space.space_name)
        
=======
        white_deck = self.game.white_player.pieces_in_deck
        black_deck = self.game.black_player.pieces_in_deck
        player_board = self.game.current_player.pieces_on_board
        space_state = self.board_space.state
        space_name = self.board_space.space_name
        #Start of game before all pieces are on the board 
        if white_deck > 0 or black_deck > 0:# or (white_deck == 0 and black_deck == 0 and player_board == 3):
            if space_state == MadMansMorris.BoardSpace.EMPTY_SPACE:
                self.game.place_piece(self.board_space.space_name)
            else:
                return
        #here is where the game stops letting me make moves
        elif white_deck == 0 and black_deck == 0:
            if space_state == MadMansMorris.BoardSpace.EMPTY_SPACE and space_name in self.board_space.neighbors:
                self.game.place_piece(self.board_space.space_name)
            else:
                return
        morris_check = self.game.check_for_mill(space_name)

        if not morris_check:
            self.game.change_player()
        
        if morris_check:
            print("Morris!")

            
        
       # if not morris_check and space_state == self.game.other_player.piece_type:
         #   self.game.remove_piece(self.board_space.space_name)
          #  self.game.change_player()
        
            
          #  self.game.change_player()


            #else:
                #return
                #if self.board_space.state != self.game.current_player.piece_type:
                    #self.game.remove_piece(self.board_space.space_name)
            
>>>>>>> 355a10ad10e727759faeb3af3702f2f730860963
        return super().mousePressEvent(event)
    
    def __position_from_space_name(self, space_name: str):
        x = ord(space_name[0]) - 65
        y = 7 - int(space_name[1]) 
        return x, y


class MainWindow(QMainWindow):
    def __init__(self):
        self.game = MadMansMorris.Game()

        super().__init__()
        self.setWindowTitle("Mad Man's Morris")

        self.setMinimumSize(600, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.player_turn_text = QLabel("Player Turn: " )
        self.player_turn_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.player_turn_text)

        self.view = QGraphicsView()
        self.layout.addWidget(self.view)

        self.view.setFrameStyle(0)

        self.setStyleSheet("background-color: #FFFFFF; color: #000000; font-family: Arial; font-size: 20px;")

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.space_graphics = []

        self.draw_board()

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.update_board()


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
            space_graphic = QBoardSpace(space, self.game)
            
            self.space_graphics.append(space_graphic)
            self.scene.addItem(space_graphic)
    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        return super().resizeEvent(a0)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.update_board()
        return super().mousePressEvent(a0)
    
    def update_board(self):
        self.player_turn_text.setText("Player Turn: " + ("Black" if self.game.current_player == self.game.black_player else "White"))
        for space_graphic in self.space_graphics:
            space_graphic.update()
        
        # self.scene.setSceneRect(self.scene.itemsBoundingRect())
        # self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        








app = QApplication([])

window = MainWindow()
window.show()

app.exec()