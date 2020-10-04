import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from TryWindow import TryWindow
from RankWindow import RankWindow
from GameWindowChoose import GameWindowChoose

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        label = QLabel('<h1 align="center"><font color=black>华容道</font></h1>', self)
        label.move(175, 140)
        label.resize(150, 100)

        start_button = QPushButton('简单模式', self)
        start_button.move(200, 250)
        start_button.resize(100, 40)
        start_button.clicked.connect(self.callGame)

        try_button = QPushButton('挑战模式', self)
        try_button.move(200, 300)
        try_button.resize(100, 40)
        try_button.clicked.connect(self.callTry)

        rank_button = QPushButton('往次得分', self)
        rank_button.move(200, 350)
        rank_button.resize(100, 40)
        rank_button.clicked.connect(self.callRank)

        exit_button = QPushButton('退出游戏', self)
        exit_button.move(200, 400)
        exit_button.resize(100, 40)
        exit_button.clicked.connect(self.callQuit)

        self.resize(500, 500)
        self.setFixedSize(500, 500)
        self.setWindowTitle('华容道')

    def callGame(self):
        self.game_window_choose = GameWindowChoose()
        self.game_window_choose.show()

    def callRank(self):
        self.rank_window = RankWindow()
        self.rank_window.show()

    def callTry(self):
        self.try_window = TryWindow()
        self.try_window.show()

    def callQuit(self):
        app = QApplication.instance()
        app.quit()