from hashlib import blake2b
from string import whitespace
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsView, QSizePolicy, QVBoxLayout, QLabel
from PyQt6.QtGui import QBrush, QColor, QPen, QPainter, QPaintEvent, QMouseEvent, QFont, QPalette, QResizeEvent
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QRect
from PyQt6.QtCore import Qt

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
        self.player_turn_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.player_turn_text)

        self.view = QGraphicsView()
        self.layout.addWidget(self.view)

        self.view.setFrameStyle(0)

        self.setStyleSheet("background-color: #FFFFFF; color: #000000; font-family: Arial; font-size: 20px;align-items: center; justify-content: center;")

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

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


        self.game.move_piece("D3", "C3")
        self.game.move_piece("E4", "E5")
        self.game.move_piece("F4", "E4")
        self.game.move_piece("G4", "F4")

        self.update_board()

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

        for row in range(7):
            self.scene.addText(str(7 - row), QFont("Arial", 20)).setPos(-50, row * 100 - 30)
        
        for col in range(7):
            self.scene.addText(chr(65 + col), QFont("Arial", 20)).setPos(col * 100 - 20, 630)

        for y in range(0, 7):
            for x in range(0, 7):
                space_name = chr(x + 65) + str(y + 1)
                if space_name in self.game.board.spaces:
                    self.scene.addEllipse(x * 100 - 6, y * 100 - 6, 12, 12, QPen(QColor(0, 0, 0)), QBrush(QColor(0, 0, 0)))
    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.scene.update()
        return super().resizeEvent(a0)

    
    def update_board(self):
        self.player_turn_text.setText("Player Turn: " + ("Black" if self.game.current_player == self.game.black_player else "White"))
        for space_graphic in self.space_graphics:
            space_graphic.update()
        
        self.scene.setSceneRect(self.scene.itemsBoundingRect())








app = QApplication([])

window = MainWindow()
window.show()

app.exec()