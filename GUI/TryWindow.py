import sys
from enum import IntEnum
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from AIshow import AIshow
from queue import PriorityQueue
import Astar
import copy
import MainWindow

blocks = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class TryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('bg.JPG')))
        self.setPalette(palette)

        self.setWindowTitle('挑战模式')
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(800, 800)
        self.setFixedSize(800, 800)
        self.blocks = []
        self.gltMain = QGridLayout()
        self.widght4 = QWidget()
        self.zero_row = 0
        self.zero_column = 0
        self.gothrough = 0
        self.degree = 3
        self.initUI()
        # self.blocks = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


    def initUI(self):
        hox = QHBoxLayout()
        form1 = QFormLayout()
        self.form2 = QFormLayout()

        # self.time_label = TimeLabel(self)
        # self.id = self.time_label.startTimer(1000)
        self.time_label = TimeLabel()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.time_label.addtime)

        form1.addRow('<h1>用时：<h1/>', self.time_label)

        self.step_label = StepLabel(self.gothrough)
        self.form2.addRow('<h1>通关数：<h1/>', self.step_label)

        widght1 = QWidget()
        widght1.setLayout(form1)
        widght2 = QWidget()
        widght2.setLayout(self.form2)
        hox.addWidget(widght1, 0, Qt.AlignCenter)
        hox.addWidget(widght2, 0, Qt.AlignCenter)

        widght3 = QWidget()
        widght3.setLayout(hox)

        self.gltMain.setSpacing(10)
        # gltMain = QGridLayout()
        # for i in range(9):
        #     gltMain.addWidget(Block(blocks[i]), int(i / 3), int(i % 3))

        # widght4 = QWidget()
        # widght4.setLayout(self.gltMain)
        self.onInit()
        self.widght4.setLayout(self.gltMain)

        vbox = QVBoxLayout()
        vbox.addWidget(widght3)
        vbox.addWidget(self.widght4)
        vbox.setStretchFactor(widght3, 1)
        vbox.setStretchFactor(self.widght4, 3)

        mainframe = QWidget()
        mainframe.setLayout(vbox)
        self.setCentralWidget(mainframe)

        # toolbar1 = self.addToolBar('结束游戏')
        # new = QAction(QIcon('python.png'), '结束游戏', self)
        # toolbar1.addAction(new)
        # toolbar1.actionTriggered.connect(self.over)
        # toolbar1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar2 = self.addToolBar('AI演示')
        new = QAction(QIcon('quick.png'), 'AI演示', self)
        self.toolbar2.addAction(new)
        self.toolbar2.actionTriggered.connect(self.AIshow)
        self.toolbar2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar3 = self.addToolBar('返回')
        new = QAction(QIcon('home.png'), '返回', self)
        self.toolbar3.addAction(new)
        self.toolbar3.actionTriggered.connect(self.back)
        self.toolbar3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


    # def over(self):
    #     reply = QMessageBox.question(self, '退出游戏', '你确定退出游戏吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         QCoreApplication.instance().quit()

    def closeEvent(self, event):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        list = timeDisplay.split()
        string = list[0]
        string = string + ' ' + str(self.step_label.getstep()) + ' ' + str(self.time_label.gettime()) + '\n'
        print(string)
        flag = self.reocrd(string)
        if flag:
            reply = QMessageBox.question(self, '退出游戏', '你已打破记录，你确定退出游戏吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            reply = QMessageBox.question(self, '退出游戏', '你并未打破纪录，你确定退出游戏吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def AIshow(self):
        if self.degree == 3:
            # self.toolbar2.setEnabled(True)
            temp1 = copy.deepcopy(self.blocks)
            temp2 = copy.deepcopy(self.zero_row)
            temp3 = copy.deepcopy(self.zero_column)
            list = []
            for i in range(3):
                for j in range(3):
                    list.append(temp1[i][j])
            walklist = Astar.bfsHash(list, temp2, temp3, 3)
            print('walklist:', walklist)
            temp4 = copy.deepcopy(walklist)
            self.time_label.ai_add()
            self.ai_show = AIshow(temp1, temp2, temp3, 3, temp4)
            # self.time_label.tostop()
            self.ai_show.show()
            # print('flag:' ,self.flag)
            # if self.flag == 0:
            #     self.time_label.restart()


    def reocrd(self, string):
        file = open('rank.txt')
        rank = []
        while True:
            line = file.readline()
            if not line:
                break
            rank.append(line)
        file.close()
        temp = []
        for item in rank:
            item = item.replace('\n', '')
            temp.append(item)
        que = PriorityQueue()
        for item in temp:
            list = item.split(' ')
            a = node(list[0], int(list[1]), float(list[2]))
            que.put(a)
        list = string.split(' ')
        a = node(list[0], int(list[1]), float(list[2]))
        que.put(a)
        string = ''
        flag = 0
        i = 0
        while not que.empty():
            top = que.get()
            i = i + 1
            if a == top and i < 11:
                flag = 1
            string = string + top.date + ' ' + str(top.num) + ' ' + str(round(top.time, 2)) + '\n'
        with open('rank.txt', 'a') as file_handle:
            file_handle.truncate(0)
            file_handle.write(string)
            file_handle.close()
        return flag

    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        print(self.degree)
        self.numbers = list(range(1, self.degree * self.degree))
        self.numbers.append(0)
        # 将数字添加到二维数组
        for row in range(self.degree):
            self.blocks.append([])
            for column in range(self.degree):
                temp = self.numbers[row * self.degree + column]
                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)
        # 打乱数组
        for i in range(500):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        self.updatePanel()

    def back(self):
        self.hide()
        self.father = MainWindow.MainWindow()
        self.father.show()

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        if (key == Qt.Key_Up or key == Qt.Key_W):
            self.move(Direction.UP)
        if (key == Qt.Key_Down or key == Qt.Key_S):
            self.move(Direction.DOWN)
        if (key == Qt.Key_Left or key == Qt.Key_A):
            self.move(Direction.LEFT)
        if (key == Qt.Key_Right or key == Qt.Key_D):
            self.move(Direction.RIGHT)
        self.updatePanel()
        if self.checkResult():
            # self.time_label.tostop()
            self.timer.stop()
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成关卡'):
                self.gothrough = self.gothrough + 1
                self.step_label.add_step()
                self.blocks = []
                self.zero_row = 0
                self.zero_column = 0
                if self.gothrough < 1:
                    self.onInit()
                elif self.gothrough >=2 and self.gothrough < 4:
                    if self.gothrough == 2:
                        self.degree = self.degree + 1
                        self.toolbar2.setEnabled(False)
                    self.onInit()
                else:
                    if self.gothrough == 4:
                        self.degree = self.degree + 1
                        self.toolbar2.setEnabled(False)
                    self.onInit()

                # self.onInit()
            # self.time_label.restart()
            self.timer.start()
    # 方块移动算法
    def move(self, direction):
        if (direction == Direction.UP):  # 上
            if self.zero_row != (self.degree - 1):
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if (direction == Direction.DOWN):  # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if (direction == Direction.LEFT):  # 左
            if self.zero_column != (self.degree - 1):
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if (direction == Direction.RIGHT):  # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1

    def updatePanel(self):
        for row in range(self.degree):
            for column in range(self.degree):
                self.gltMain.addWidget(Block(self.blocks[row][column]), row, column)
        self.widght4.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        # 先检测最右下角是否为0
        if self.blocks[self.degree - 1][self.degree - 1] != 0:
            return False

        for row in range(self.degree):
            for column in range(self.degree):
                # 运行到此处说明最右下角已经为0，pass即可
                if row == (self.degree - 1) and column == (self.degree - 1):
                    return True
                # 值是否对应
                elif self.blocks[row][column] != row * self.degree + column + 1:
                    return False


# class TimeLabel(QLabel):
#     def __init__(self, par):
#         super().__init__()
#         self.setText('0')
#         self.d = par
#         font = QFont()
#         font.setPointSize(30)
#         font.setBold(True)
#         self.setFont(font)
#
#     def timerEvent(self, event):
#         a = int(self.text()) + 1
#         if a == 100000:
#             self.killTimer(self.d.id)
#         self.setText(str(a))
#
#     def tostop(self):
#         self.killTimer(self.d.id)
#
#     def restart(self):
#         self.startTimer(1000)
#
#     def gettime(self):
#         return int(self.text())
#
#     def settime(self):
#         self.setText('0')
#
#     def ai_add(self):
#         a = int(self.text()) + 20
#         self.setText(str(a))

class TimeLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText('0')
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

    def addtime(self):
        a = int(self.text()) + 1
        self.setText(str(a))

    def gettime(self):
        return int(self.text())

    def settime(self):
        self.setText('0')

    def ai_add(self):
        a = int(self.text()) + 20
        self.setText(str(a))

class StepLabel(QLabel):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.setText(str(self.num))
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

    def add_step(self):
        a = int(self.text()) + 1
        self.setText(str(a))

    def getstep(self):
        return int(self.text())

    def setstep(self):
        self.setText('0')



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

class node(object):
    def __init__(self, date, num, time):
        self.date = date
        self.num = num
        self.time = time

    def __lt__(self, other):
        if self.num == other.num:
            return self.time < other.time
        else:
            return self.num > other.num