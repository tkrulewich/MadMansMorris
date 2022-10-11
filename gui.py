from hashlib import blake2b
from string import whitespace
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsView, QSizePolicy, QVBoxLayout, QLabel
from PyQt6.QtGui import QBrush, QColor, QPen, QPainter, QPaintEvent, QMouseEvent
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QRect

import MadMansMorris


black_piece_render = QSvgRenderer("images/black_piece.svg")
white_piece_render = QSvgRenderer("images/white_piece.svg")
empty_space_render = QSvgRenderer("images/empty_space.svg")

class QBoardSpace(QGraphicsSvgItem):
    def __init__(self, board_space: MadMansMorris.BoardSpace):
        super().__init__()
        self.board_space : MadMansMorris = board_space

        self.update()

    def update(self):
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)

        if self.board_space.state == MadMansMorris.BoardSpace.BLACK_SPACE:
            self.setSharedRenderer(black_piece_render)
        elif self.board_space.state == MadMansMorris.BoardSpace.WHITE_SPACE:
            self.setSharedRenderer(white_piece_render)
        else :
            self.setSharedRenderer(empty_space_render)
            self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        
        self.x, self.y = self.__position_from_space_name(self.board_space.space_name)

        self.setPos(self.x * 100.0 -354.0 / 2.0, self.y * 100.0 - 354.0 / 2.0)

        self.setTransformOriginPoint(self.boundingRect().center())
        self.setScale(0.15)
    
    def __position_from_space_name(self, space_name: str):
        x = ord(space_name[0]) - 65
        y = 7 - int(space_name[1]) 
        return x, y


class MainWindow(QMainWindow):
    def __init__(self):
        self.game = MadMansMorris.Game()

        super().__init__()
        self.setWindowTitle("Mad Man's Morris")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.player_turn_text = QLabel("Player Turn: " )
        self.layout.addWidget(self.player_turn_text)

        self.view = QGraphicsView()
        self.layout.addWidget(self.view)

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.space_graphics = []

        self.draw_board()

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        for space in self.game.board.spaces.values():
            space_graphic = QBoardSpace(space)
            
            self.space_graphics.append(space_graphic)
            self.scene.addItem(space_graphic)
        

        self.game.place_piece("A7")
        self.game.place_piece("A1")
        self.game.place_piece("A4")
        
        self.game.remove_piece("A7")

        self.update_board()
        

        self.setMinimumHeight(700)
        self.setMinimumWidth(700)

        self.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Minimum)
        self.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Minimum)




    def draw_board(self):
        self.scene.addRect(0, 0, 600, 600, QPen(QColor(0, 0, 0)))
        self.scene.addRect(100, 100, 400, 400, QPen(QColor(0, 0, 0)))
        self.scene.addRect(200, 200, 200, 200, QPen(QColor(0, 0, 0)))

        self.scene.addLine(300, 0, 300, 200, QPen(QColor(0, 0, 0)))
        self.scene.addLine(300, 400, 300, 600, QPen(QColor(0, 0, 0)))

        self.scene.addLine(0, 300, 200, 300, QPen(QColor(0, 0, 0)))
        self.scene.addLine(400, 300, 600, 300, QPen(QColor(0, 0, 0)))

        for y in range(0, 7):
            for x in range(0, 7):
                space_name = chr(x + 65) + str(y + 1)
                if space_name in self.game.board.spaces:
                    self.scene.addEllipse(x * 100 - 6, y * 100 - 6, 12, 12, QPen(QColor(0, 0, 0)), QBrush(QColor(0, 0, 0)))
    
    def update_board(self):
        self.player_turn_text.setText("Player Turn: " + ("Black" if self.game.current_player == self.game.black_player else "White"))
        for space_graphic in self.space_graphics:
            space_graphic.update()








app = QApplication([])

window = MainWindow()
window.show()

app.exec()