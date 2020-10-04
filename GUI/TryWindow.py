import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('挑战模式')
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(500, 500)
        self.setFixedSize(500, 500)