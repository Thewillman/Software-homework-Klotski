import sys
from PyQt5 import QtWidgets
from enum import IntEnum
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import copy
import Astar
# import TryWindow

class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3



class AIshow(QMainWindow):
    # 二维序列，0的行，0的列，几阶
    def __init__(self, blocks, zero_row, zero_column, degree, walklist):
        super().__init__()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('bg.JPG')))
        self.setPalette(palette)

        self.initblocks = copy.deepcopy(blocks)
        self.initzerorow = copy.deepcopy(zero_row)
        self.initzerocolumn = copy.deepcopy(zero_column)
        self.initblocks2 = copy.deepcopy(blocks)
        self.initzeroro2 = copy.deepcopy(zero_row)
        self.initzerocolumn2 = copy.deepcopy(zero_column)
        self.block = blocks
        self.zerorow = zero_row
        self.zerocolumn = zero_column
        self.degree = degree
        self.setFixedSize(800, 800)
        self.setWindowTitle('AI演示')
        self.setWindowModality(Qt.ApplicationModal)
        self.gltMain = QGridLayout()
        self.walk_list = walklist
        self.walk_now = 0
        self.initUI()

    def initUI(self):
        self.gltMain.setSpacing(10)
        # print('------------------------')
        # print(self.blocks)
        # print(self.zero_row)
        # print(self.zero_column)
        # print('---------------------------')

        hbox = QHBoxLayout()

        self.widght1 = QWidget()
        self.updatePanel()
        self.widght1.setLayout(self.gltMain)

        # self.edit = QTextEdit()
        # file = open('order.txt').read()
        # self.edit.setText(file)
        # self.edit.setEnabled(False)
        file = open('order.txt').read()
        label = QLabel(file, self)
        label.setStyleSheet('QLabel{font-size:22px}'
                            'QLabel{font-weight:bold}'
                            'QLabel{color:#000000}'
                            'QLabel{font-family:SimSun}'
                            )
        label.setText(file)
        label.setEnabled(False)

        hbox.addWidget(self.widght1)
        # hbox.addWidget(self.edit)
        hbox.addWidget(label)
        hbox.setStretchFactor(self.widght1, 4)
        hbox.setStretchFactor(label, 1)

        mainframe = QWidget()
        mainframe.setLayout(hbox)
        self.setCentralWidget(mainframe)

        self.toolbar1 = self.addToolBar('重新开始')
        new = QAction(QIcon('return.png'), '重新开始', self)
        self.toolbar1.addAction(new)
        self.toolbar1.actionTriggered.connect(self.restart)
        self.toolbar1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar2 = self.addToolBar('动画演示')
        new = QAction(QIcon('play.png'), '动画演示', self)
        self.toolbar2.addAction(new)
        self.toolbar2.actionTriggered.connect(self.AIshow)
        self.toolbar2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar3 = self.addToolBar('逐步演示')
        new = QAction(QIcon('click.png'), '逐步演示', self)
        self.toolbar3.addAction(new)
        self.toolbar3.actionTriggered.connect(self.buttonshow)
        self.toolbar3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar4 = self.addToolBar('返回')
        new = QAction(QIcon('home.png'), '返回', self)
        self.toolbar4.addAction(new)
        self.toolbar4.actionTriggered.connect(self.back)
        self.toolbar4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def back(self):
        self.hide()

    def restart(self):
        self.block = copy.deepcopy(self.initblocks)
        self.zerorow = copy.deepcopy(self.initzerorow)
        self.zerocolumn = copy.deepcopy(self.initzerocolumn)
        self.updatePanel()
        self.toolbar3.setEnabled(True)
        self.toolbar2.setEnabled(True)

    def AIshow(self):
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.start()
        self.timer.timeout.connect(self.walk)
        self.toolbar1.setEnabled(False)
        self.toolbar2.setEnabled(False)
        self.toolbar3.setEnabled(False)


    def buttonshow(self):
        self.toolbar1.setEnabled(False)
        self.toolbar2.setEnabled(False)
        self.move(self.walk_list[self.walk_now])
        self.updatePanel()
        self.walk_now = self.walk_now + 1
        if self.walk_now == len(self.walk_list):
            self.walk_now = 0
            self.toolbar3.setEnabled(False)
            self.toolbar1.setEnabled(True)


    def walk(self):
        self.move(self.walk_list[self.walk_now])
        self.updatePanel()
        self.walk_now = self.walk_now + 1
        if self.walk_now == len(self.walk_list):
            self.timer.stop()
            self.walk_now = 0
            self.toolbar1.setEnabled(True)

    # 方块移动算法
    def move(self, direction):
        if (direction == Direction.UP):  # 上
            if self.zerorow != (self.degree - 1):
                self.block[self.zerorow][self.zerocolumn] = self.block[self.zerorow + 1][self.zerocolumn]
                self.block[self.zerorow + 1][self.zerocolumn] = 0
                self.zerorow += 1
        if (direction == Direction.DOWN):  # 下
            if self.zerorow != 0:
                self.block[self.zerorow][self.zerocolumn] = self.block[self.zerorow - 1][self.zerocolumn]
                self.block[self.zerorow - 1][self.zerocolumn] = 0
                self.zerorow -= 1
        if (direction == Direction.LEFT):  # 左
            if self.zerocolumn != (self.degree - 1):
                self.block[self.zerorow][self.zerocolumn] = self.block[self.zerorow][self.zerocolumn + 1]
                self.block[self.zerorow][self.zerocolumn + 1] = 0
                self.zerocolumn += 1
        if (direction == Direction.RIGHT):  # 右
            if self.zerocolumn != 0:
                self.block[self.zerorow][self.zerocolumn] = self.block[self.zerorow][self.zerocolumn - 1]
                self.block[self.zerorow][self.zerocolumn - 1] = 0
                self.zerocolumn -= 1

    def updatePanel(self):
        for row in range(self.degree):
            for column in range(self.degree):
                self.gltMain.addWidget(Block(self.block[row][column]), row, column)

        self.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        # 先检测最右下角是否为0
        if self.block[self.degree - 1][self.degree - 1] != 0:
            return False

        for row in range(self.degree):
            for column in range(self.degree):
                # 运行到此处说名最右下角已经为0，pass即可
                if row == (self.degree - 1) and column == (self.degree - 1):
                    return True
                # 值是否对应
                elif self.block[row][column] != row * self.degree + column + 1:
                    return False

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出AI', '你确定退出AI吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Block(QLabel):
    """ 数字方块 """

    def __init__(self, number):
        super().__init__()

        self.number = number
        self.setFixedSize(80, 80)

        # 设置字体
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

        # 设置字体颜色
        pa = QPalette()
        pa.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(pa)

        # 设置文字位置
        self.setAlignment(Qt.AlignCenter)

        # 设置背景颜色\圆角和文本内容
        if self.number == 0:
            self.setStyleSheet("background-color:white;border-radius:10px;")
        else:
            self.setStyleSheet("background-color:black;border-radius:10px;")
            self.setText(str(self.number))