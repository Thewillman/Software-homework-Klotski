import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from GameWindow1 import GameWindow1
from GameWindow2 import GameWindow2
from GameWindow3 import GameWindow3


# 游戏难度选择
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

    # 初始化
    def initUI(self):
        # 设置水平布局
        layout = QHBoxLayout()

        self.button1 = QPushButton('3X3')
        self.button1.clicked.connect(self.choose3X3)

        self.button2 = QPushButton('4X4')
        self.button2.clicked.connect(self.choose4X4)

        self.button3 = QPushButton('5X5')
        self.button3.clicked.connect(self.choose5X5)
        # 将button加入布局
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        self.setLayout(layout)
        self.close()

    # 打开3X3游戏面板，下同
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