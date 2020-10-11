import sys
from enum import IntEnum
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from AIshow import AIshow
import copy
import Astar
import random
import MainWindow

class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class GameWindow1(QMainWindow):

    def __init__(self):
        super().__init__()
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0
        self.des = ""
        self.step = 0
        self.least_step = 0
        self.gltMain = QGridLayout()
        self.initUI()
        # self.button1 = QPushButton('AI演示')
        # self.button2 = QPushButton('重开本局')
        # self.button2.clicked.connect(self.onInit)

    def initUI(self):
        # 设置方块间隔
        self.gltMain.setSpacing(10)
        self.onInit()
        self.time_label = TimeLabel(self)
        self.id = self.time_label.startTimer(1000)
        # 设置布局
        mainframe = QWidget()
        mainframe.setLayout(self.gltMain)
        self.setCentralWidget(mainframe)
        # self.setLayout(self.gltMain)

        # 设置宽和高
        self.setFixedSize(600, 600)
        self.setWindowTitle('简单模式-3X3')
        self.setWindowModality(Qt.ApplicationModal)
        # 设置背景颜色
        # self.setStyleSheet("background-color:gray;")
        # self.show()

        toolbar1 = self.addToolBar('重新开始')
        new = QAction(QIcon('python.png'), '重新开始', self)
        toolbar1.addAction(new)
        toolbar1.actionTriggered.connect(self.restart)
        toolbar1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar2 = self.addToolBar('AI演示')
        new = QAction(QIcon('python.png'), 'AI演示', self)
        toolbar2.addAction(new)
        toolbar2.actionTriggered.connect(self.AIshow)
        toolbar2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar3 = self.addToolBar('返回')
        new = QAction(QIcon('python.png'), '返回', self)
        toolbar3.addAction(new)
        toolbar3.actionTriggered.connect(self.back)
        toolbar3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def back(self):
        self.hide()
        self.f = MainWindow.MainWindow()
        self.f.show()

    def restart(self):
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0
        self.des = ""
        self.walklist = []
        self.step = 0
        self.least_step = 0
        self.numbers = []
        self.onInit()

    def AIshow(self):
        temp1 = copy.deepcopy(self.blocks)
        temp2 = copy.deepcopy(self.zero_row)
        temp3 = copy.deepcopy(self.zero_column)
        list = []
        for i in range(3):
            for j in range(3):
                list.append(temp1[i][j])
        #print(temp1)
        #print(temp2)
        #print(temp3)
        walklist = Astar.bfsHash(list, temp2, temp3, self.des,3)
        print('walklist:', walklist)
        temp4 = copy.deepcopy(walklist)
        self.ai_show = AIshow(self.time_label, temp1, temp2, temp3, 3, temp4,self)
        self.ai_show.show()
        # print(self.blocks)
        # print(self.zero_row)
        # print(self.zero_column)

    # 初始化布局
    def onInit(self):
        # 产生顺序数组

        self.numbers = [1,2,3,4,5,6,7,8,9]
        k = random.randint(0,8)
        self.numbers[k] = 0
        self.des = ""

        for i in self.numbers:
            self.des += str(i)
        print(self.des)
        # 将数字添加到二维数组
        self.blocks = []
        for row in range(3):
            self.blocks.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]
                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)
        # 打乱数组
        for i in range(500):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        temp1 = copy.deepcopy(self.blocks)
        temp2 = copy.deepcopy(self.zero_row)
        temp3 = copy.deepcopy(self.zero_column)
        print(temp1)
        print(temp2)
        print(temp3)
        list = []
        for i in range(3):
            for j in range(3):
                list.append(temp1[i][j])
        print(list)
        self.least_step = len(Astar.bfsHash(list, temp2, temp3, self.des,3))
        self.updatePanel()


    # 检测按键
    def keyPressEvent(self, event):
        # print(self.blocks)
        # print(self.zero_row)
        # print(self.zero_column)
        key = event.key()
        if (key == Qt.Key_Up or key == Qt.Key_W):
            self.move(Direction.UP)
        if (key == Qt.Key_Down or key == Qt.Key_S):
            self.move(Direction.DOWN)
        if (key == Qt.Key_Left or key == Qt.Key_A):
            self.move(Direction.LEFT)
        if (key == Qt.Key_Right or key == Qt.Key_D):
            self.move(Direction.RIGHT)
        self.step += 1
        self.updatePanel()
        # print(self.blocks)
        # print(self.zero_column)
        # print(self.zero_row)
        if self.checkResult():
            str2 = '恭喜您完成挑战！'+'移动了'+str(self.step)+'步,和ai差'+str(self.step-self.least_step)+'步'
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', str2):
                self.restart()
                self.onInit()

    # 方块移动算法
    def move(self, direction):
        if (direction == Direction.UP):  # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if (direction == Direction.DOWN):  # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if (direction == Direction.LEFT):  # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if (direction == Direction.RIGHT):  # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1

    def updatePanel(self):
        for row in range(3):
            for column in range(3):
                self.gltMain.addWidget(Block(self.blocks[row][column]), row, column)
        self.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        # 先检测最右下角是否为0

        for row in range(3):
            for column in range(3):
                # 值是否对应
                if self.blocks[row][column] != int(self.des[row*3+column]):
                    return False
        return True


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

class TimeLabel(QLabel):
    def __init__(self, par):
        super().__init__()
        self.setText('0')
        self.d = par
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)
        self.flag = 0

    def timerEvent(self, event):
        #print(self.flag)
        if self.flag == 0:
            a = int(self.text()) + 1
            if a == 100000:
                self.killTimer(self.d.id)
            self.setText(str(a))
        else:
            a = int(self.text())
            self.setText(str(a))

    def tokill(self):
        self.killTimer(self.d.id)

    def tostop(self):
        self.flag = 1

    def tocontinue(self):
        self.flag = 0

    def restart(self):
        self.startTimer(1000)

    def gettime(self):
        return int(self.text())

    def settime(self):
        self.setText('0')