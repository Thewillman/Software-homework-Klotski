import sys
from enum import IntEnum
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AIshow(QMainWindow):
    # 二维序列，0的行，0的列，几阶
    def __init__(self, blocks, zero_row, zero_column, degree):
        super().__init__()
        self.blocks = blocks
        self.zero_row = zero_row
        self.zero_column = zero_column
        self.degree = degree
        self.initUI()
    def initUI(self):
        print('------------------------')
        print(self.blocks)
        print(self.zero_row)
        print(self.zero_column)
        print('---------------------------')
        self.setFixedSize(600, 600)
        self.setWindowTitle('AI演示')
        self.setWindowModality(Qt.ApplicationModal)
