import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import MainWindow


class RankWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('bg.JPG')))
        self.setPalette(palette)

        self.setWindowTitle('AI排行')
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
        tablewidget.setHorizontalHeaderLabels(['排名', '记录日期', '总时间(s)', '与AI相差步数'])
        tablewidget.verticalHeader().setVisible(False)
        file = open('airank.txt')
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

        toolbar = self.addToolBar('返回')
        new = QAction(QIcon('home.png'), '返回', self)
        toolbar.addAction(new)
        toolbar.actionTriggered.connect(self.back)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        mainframe = QWidget()
        mainframe.setLayout(layout)
        self.setCentralWidget(mainframe)

        self.setLayout(layout)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出游戏', '你确定退出游戏吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def back(self):
        self.hide()
        self.father = MainWindow.MainWindow()
        self.father.show()

