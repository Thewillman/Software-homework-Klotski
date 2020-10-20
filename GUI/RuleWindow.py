import sys
from enum import IntEnum
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import MainWindow


# 游戏规则界面
class RuleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('bg.JPG')))
        self.setPalette(palette)

        self.setWindowTitle('游戏规则')
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(600, 600)
        self.initUI()

    # 初始化布局
    def initUI(self):
        layout = QHBoxLayout()
        file = open('rule.txt', encoding='utf-8').read()
        label = QLabel(file, self)
        # 设置优秀规则的css样式
        label.setStyleSheet('QLabel{font-size:25px}'
                            'QLabel{font-weight:bold}'
                            'QLabel{color:#000000}')
        label.setText(file)
        label.setEnabled(False)
        layout.addWidget(label)

        toolbar = self.addToolBar('返回')
        new = QAction(QIcon('home.png'), '返回', self)
        toolbar.addAction(new)
        toolbar.actionTriggered.connect(self.back)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        mainframe = QWidget()
        mainframe.setLayout(layout)
        self.setCentralWidget(mainframe)

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

