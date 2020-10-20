import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from TryWindow import TryWindow
from RankWindow import RankWindow
from GameWindowChoose import GameWindowChoose
from RankWindow2 import RankWindow2
from AItry import AItry
from RuleWindow import RuleWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()


        self.initUI()


    def initUI(self):
        label = QLabel('华容道', self)
        label.setStyleSheet('QLabel{font-size:50px}'
                            'QLabel{font-weight:bold}')
        # 手动设置label位置
        label.move(170, 30)
        label.resize(150, 100)

        # 手动设置每个button的位置
        start_button = QPushButton('简单游戏', self)
        start_button.move(200, 150)
        start_button.resize(100, 40)
        # start_button.setStyleSheet('QPushButton{font-size:15px}')
        start_button.clicked.connect(self.callGame)

        try_button = QPushButton('通关挑战', self)
        try_button.move(200, 200)
        try_button.resize(100, 40)
        try_button.clicked.connect(self.callTry)

        ai_button = QPushButton('AI挑战', self)
        ai_button.move(200, 250)
        ai_button.resize(100, 40)
        ai_button.clicked.connect(self.callAI)

        rank_button = QPushButton('通关排名', self)
        rank_button.move(200, 300)
        rank_button.resize(100, 40)
        rank_button.clicked.connect(self.callRank)

        rank2_button = QPushButton('AI排名', self)
        rank2_button.move(200, 350)
        rank2_button.resize(100, 40)
        rank2_button.clicked.connect(self.callRank2)

        rule_button = QPushButton('游戏规则', self)
        rule_button.move(200, 400)
        rule_button.resize(100, 40)
        rule_button.clicked.connect(self.callRule)



        exit_button = QPushButton('退出游戏', self)
        exit_button.move(200, 450)
        exit_button.resize(100, 40)
        exit_button.clicked.connect(self.callQuit)


        self.setFixedSize(500, 550)
        self.setWindowTitle('华容道')

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('bg.JPG')))
        self.setPalette(palette)


    # 打开各个面板
    def callGame(self):
        self.game_window_choose = GameWindowChoose(self)
        self.game_window_choose.show()

    def callRank(self):
        self.rank_window = RankWindow()
        self.hide()
        self.rank_window.show()

    def callTry(self):
        self.try_window = TryWindow()
        self.hide()
        self.try_window.show()

    def callAI(self):
        self.aitry_window = AItry()
        self.hide()
        self.aitry_window.show()

    def callRank2(self):
        self.rank_window = RankWindow2()
        self.hide()
        self.rank_window.show()

    def callQuit(self):
        # 退出游戏，直接关闭
        app = QApplication.instance()
        app.quit()

    def callRule(self):
        self.rule_window = RuleWindow()
        self.hide()
        self.rule_window.show()
