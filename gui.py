from hashlib import blake2b
from http.cookiejar import DefaultCookiePolicy
from string import whitespace
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsView, QSizePolicy, QVBoxLayout
from PyQt6.QtWidgets import QLabel, QMessageBox, QGraphicsBlurEffect, QGraphicsColorizeEffect
from PyQt6.QtGui import QBrush, QColor, QPen, QPainter, QPaintEvent, QMouseEvent, QFont, QPalette, QResizeEvent
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QRect, Qt

from collections import deque

import MadMansMorris

black_piece_render = QSvgRenderer("images/black_piece.svg")
black_piece_mill_render = QSvgRenderer("images/black_piece_mill.svg")

white_piece_render = QSvgRenderer("images/white_piece.svg")
white_piece_mill_render = QSvgRenderer("images/white_piece_mill.svg")

empty_space_render = QSvgRenderer("images/empty_space.svg")

class QBoardSpace(QGraphicsSvgItem):
    def __init__(self, board_space: MadMansMorris.BoardSpace, game: MadMansMorris.Game,board_renderer: 'BoardRenderer'):
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

        if self.game.check_for_mill(self.board_space.space_name):
            colorEffect = QGraphicsColorizeEffect()
            colorEffect.setColor(QColor(100, 100, 0, 200))
            self.setGraphicsEffect(colorEffect)
    
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.board_renderer.space_clicked(self.board_space.space_name)
        return super().mousePressEvent(event)
    
    def __position_from_space_name(self, space_name: str):
        x = ord(space_name[0]) - 65
        y = 7 - int(space_name[1]) 
        return x, y


class BoardRenderer(QMainWindow):
    def __init__(self):
        self.game = MadMansMorris.Game()

        self.spaces_selected_stack = deque()

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
            space_graphic = QBoardSpace(space, self.game, self)
            
            self.space_graphics.append(space_graphic)
            self.scene.addItem(space_graphic)
    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        return super().resizeEvent(a0)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.update_board()
        self.scene.update()
        return super().mousePressEvent(a0)
    
    def update_board(self):
        self.player_turn_text.setText("Player Turn: " + ("Black" if self.game.current_player == self.game.black_player else "White"))
        for space_graphic in self.space_graphics:
            space_graphic.update()
        
        # self.scene.setSceneRect(self.scene.itemsBoundingRect())
        # self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        
    def space_clicked(self, space_name: str):
        if self.game.current_player.pieces_in_deck > 0:

            if self.game.board.get_space(space_name) == MadMansMorris.BoardSpace.EMPTY_SPACE:
                self.game.place_piece(space_name)
            else:
                self.game.remove_piece(space_name)
        else:
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
        
        self.update_board()








app = QApplication([])

window = BoardRenderer()
window.show()

app.exec()