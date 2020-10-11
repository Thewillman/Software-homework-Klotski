import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from MainWindow import MainWindow
import qdarkstyle

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main.show()
    sys.exit(app.exec_())
