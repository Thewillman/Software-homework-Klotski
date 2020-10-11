import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import MainWindow

class RankWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('往次得分')
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(528, 530)
        self.setFixedSize(528, 530)
        self.initUI()


    def initUI(self):
        layout = QHBoxLayout()
        tablewidget = QTableWidget()
        tablewidget.setRowCount(10)
        tablewidget.setColumnCount(4)
        layout.addWidget(tablewidget)
        tablewidget.setHorizontalHeaderLabels(['排名', '记录日期', '通关数', '总时间(s)'])
        tablewidget.verticalHeader().setVisible(False)
        file = open('rank.txt')
        rank = []
        while True:
            line = file.readline()
            if not line:
                break
            rank.append(line)
        file.close()
        i = 0
        for item in rank:
            item = item.replace('\n', '')
            list = item.split(' ')
            temp = QTableWidgetItem(str(i + 1))
            temp.setTextAlignment(Qt.AlignCenter)
            tablewidget.setItem(i, 0, temp)
            for j in range(3):
                temp = QTableWidgetItem(list[j])
                temp.setTextAlignment(Qt.AlignCenter)
                tablewidget.setItem(i, j + 1, temp)
            i = i + 1
        # 禁止编辑
        tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 整行选择
        tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        toolbar3 = self.addToolBar('返回')
        new = QAction(QIcon('python.png'), '返回', self)
        toolbar3.addAction(new)
        toolbar3.actionTriggered.connect(self.back)
        toolbar3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # self.widght = QWidget()
        # self.widght.setLayout(layout)
        # self.setLayout(layout)
        mainframe = QWidget()
        mainframe.setLayout(layout)
        self.setCentralWidget(mainframe)

    def back(self):
        self.hide()
        self.f = MainWindow.MainWindow()
        self.f.show()
