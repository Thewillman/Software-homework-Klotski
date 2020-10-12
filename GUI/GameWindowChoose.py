import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from GameWindow1 import GameWindow1
from GameWindow2 import GameWindow2
from GameWindow3 import GameWindow3


class GameWindowChoose(QDialog):
    def __init__(self, GameWindow):
        super().__init__()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('bg.JPG')))
        self.setPalette(palette)
        self.window = GameWindow
        self.setWindowTitle('请选择游戏难度')
        self.setWindowModality(Qt.ApplicationModal)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        self.button1 = QPushButton('3X3')
        self.button1.clicked.connect(self.choose3X3)

        self.button2 = QPushButton('4X4')
        self.button2.clicked.connect(self.choose4X4)

        self.button3 = QPushButton('5X5')
        self.button3.clicked.connect(self.choose5X5)

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        self.setLayout(layout)
        self.close()

    def choose3X3(self):
        self.game_window = GameWindow1()
        self.window.hide()
        self.game_window.show()
        self.close()

    def choose4X4(self):
        self.game_window = GameWindow2()
        self.window.hide()
        self.game_window.show()
        self.close()

    def choose5X5(self):
        self.game_window = GameWindow3()
        self.window.hide()
        self.game_window.show()
        self.close()