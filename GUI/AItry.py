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

# AI挑战界面
class AItry(QMainWindow):
    def __init__(self):
        super().__init__()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('bg.JPG')))
        self.setPalette(palette)

        self.setWindowTitle('AI挑战')
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(800, 800)
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0
        self.copyblocks = []
        self.copyrow = 0
        self.copycolumn = 0
        self.widght5 = QWidget()
        self.gltMain = QGridLayout()
        self.initUI()

    def initUI(self):
        self.hbox = QHBoxLayout()
        self.form1 = QFormLayout()
        self.form2 = QFormLayout()
        self.form3 = QFormLayout()

        # self.time_label = TimeLabel(self)
        # self.id = self.time_label.startTimer(1000)

        # 设置用时的定时器
        self.time_label = TimeLabel()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        # 时间间隔结束后增加1秒时间
        self.timer.timeout.connect(self.time_label.addtime)
        self.form1.addRow('<h1>用时：<h1/>', self.time_label)

        self.step_label = StepLabel()
        self.form2.addRow('<h1>已走步数：<h1/>', self.step_label)

        self.ai_label = AILabel(0)
        self.form3.addRow('<h1>AI步数：<h1/>', self.ai_label)

        self.widght1 = QWidget()
        self.widght1.setLayout(self.form1)
        self.widght2 = QWidget()
        self.widght2.setLayout(self.form2)
        self.widght3 = QWidget()
        self.widght3.setLayout(self.form3)
        self.hbox.addWidget(self.widght1, 0, Qt.AlignCenter)
        self.hbox.addWidget(self.widght2, 0, Qt.AlignCenter)
        self.hbox.addWidget(self.widght3, 0, Qt.AlignCenter)

        self.widght4 = QWidget()
        self.widght4.setLayout(self.hbox)

        self.gltMain.setSpacing(10)

        self.onInit()

        self.widght5.setLayout(self.gltMain)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.widght4)
        self.vbox.addWidget(self.widght5)
        self.vbox.setStretchFactor(self.widght4, 1)
        self.vbox.setStretchFactor(self.widght5, 3)

        mainframe = QWidget()
        mainframe.setLayout(self.vbox)
        self.setCentralWidget(mainframe)

        toolbar1 = self.addToolBar('更换题目')
        new = QAction(QIcon('exchangerate.png'), '更换题目', self)
        toolbar1.addAction(new)
        toolbar1.actionTriggered.connect(self.restart)
        toolbar1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar2 = self.addToolBar('重新开始')
        new = QAction(QIcon('return.png'), '重新开始', self)
        toolbar2.addAction(new)
        toolbar2.actionTriggered.connect(self.again)
        toolbar2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar3 = self.addToolBar('返回')
        new = QAction(QIcon('home.png'), '返回', self)
        toolbar3.addAction(new)
        toolbar3.actionTriggered.connect(self.back)
        toolbar3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    # 返回
    def back(self):
        self.hide()
        self.father = MainWindow.MainWindow()
        self.father.show()
    # 更换题目
    def restart(self):
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0
        self.onInit()
        self.time_label.settime()
    # 重新开始
    def again(self):
        self.blocks = copy.deepcopy(self.copyblocks)
        self.zero_row = copy.deepcopy(self.copyrow)
        self.zero_column = copy.deepcopy(self.copycolumn)
        self.step_label.resetstep()
        self.time_label.settime()
        self.updatePanel()

    # 初始化布局
    def onInit(self):
        self.numbers = list(range(1, 9))
        self.numbers.append(0)
        # 将数字添加到二维数组
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
            self.step_label.resetstep()
        self.ai_label.setText(str(self.getai()))
        self.copyblocks = copy.deepcopy(self.blocks)
        self.copyrow = copy.deepcopy(self.zero_row)
        self.copycolumn = copy.deepcopy(self.zero_column)
        self.updatePanel()

    # 监听键盘按键事件
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
            # 游戏完成时，定时器暂停
            self.timer.stop()
            time = QDateTime.currentDateTime()
            timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
            list = timeDisplay.split()
            string = list[0]
            string = string + ' ' + str(self.step_label.getstep() - int(self.ai_label.text())) + ' ' + str(self.time_label.gettime()) + '\n'
            print(string)
            # 记录排行榜
            flag = self.record(string)
            if flag:
                if QMessageBox.Ok == QMessageBox.information(
                        self, '挑战结果', '恭喜您打破纪录！与AI相差：' + str(self.step_label.getstep() - int(self.ai_label.text()))
                                      + '步，用时：' + str(self.time_label.gettime()) + '秒'):
                    self.blocks = []
                    self.zero_row = 0
                    self.zero_column = 0
                    self.time_label.settime()
                    self.onInit()
            else:
                if QMessageBox.Ok == QMessageBox.information(
                        self, '挑战结果', '恭喜您完成关卡！与AI相差：' + str(self.step_label.getstep() - int(self.ai_label.text()))
                                      + '步，用时：' + str(self.time_label.gettime()) + '秒'):
                    self.blocks = []
                    self.zero_row = 0
                    self.zero_column = 0
                    self.time_label.settime()
                    self.onInit()
            # 定时器重新启动
            self.timer.start()

    def move(self, direction):
        if (direction == Direction.UP):  # 上
            if self.zero_row != 2:
                self.step_label.add_step()
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if (direction == Direction.DOWN):  # 下
            if self.zero_row != 0:
                self.step_label.add_step()
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if (direction == Direction.LEFT):  # 左
            if self.zero_column != 2:
                self.step_label.add_step()
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if (direction == Direction.RIGHT):  # 右
            if self.zero_column != 0:
                self.step_label.add_step()
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1


    # 刷新面板
    def updatePanel(self):
        for row in range(3):
            for column in range(3):
                self.gltMain.addWidget(Block(self.blocks[row][column]), row, column)
        self.widght5.setLayout(self.gltMain)

    # 检查是否完成
    def checkResult(self):
        # 先检测最右下角是否为0
        if self.blocks[2][2] != 0:
            return False

        for row in range(3):
            for column in range(3):
                # 运行到此处说明最右下角已经为0，pass即可
                if row == 2 and column == 2:
                    return True
                # 值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False

    # 得到AI步数
    def getai(self):
        temp1 = copy.deepcopy(self.blocks)
        temp2 = copy.deepcopy(self.zero_row)
        temp3 = copy.deepcopy(self.zero_column)
        list = []
        for i in range(3):
            for j in range(3):
                list.append(temp1[i][j])
        # 调用A*算法
        walklist = Astar.bfsHash(list, temp2, temp3, 3)
        return len(walklist)

    # 记录排行榜
    def record(self, string):
        file = open('airank.txt')
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
        # 设置优先队列，每次从优先队列的前十个写入txt
        que = PriorityQueue()
        for item in temp:
            list = item.split(' ')
            a = node(list[0], int(list[1]), int(list[2]))
            que.put(a)
        list = string.split(' ')
        a = node(list[0], int(list[1]), int(list[2]))
        que.put(a)
        string = ''
        flag = 0
        i = 0
        while not que.empty():
            top = que.get()
            i = i + 1
            if a == top and i < 11:
                flag = 1
            string = string + top.date + ' ' + str(top.num) + ' ' + str(top.time) + '\n'
        with open('airank.txt', 'a') as file_handle:
            # 清空txt内容
            file_handle.truncate(0)
            file_handle.write(string)
            file_handle.close()
        return flag

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出游戏', '你确定退出游戏吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# 时间label
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

# 步数label
class StepLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText('0')
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

    def add_step(self):
        a = int(self.text()) + 1
        self.setText(str(a))

    def getstep(self):
        return int(self.text())

    def resetstep(self):
        self.setText('0')

# AI步数label
class AILabel(QLabel):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.setText(str(self.num))
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)



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

# 放入优先队列的节点
class node(object):
    def __init__(self, date, num, time):
        self.date = date
        self.num = num
        self.time = time
    # 先考虑相差步数，在考虑时间
    def __lt__(self, other):
        if self.num == other.num:
            return self.time < other.time
        else:
            return self.num < other.num


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = AItry()
#     main.show()
#     sys.exit(app.exec_())
