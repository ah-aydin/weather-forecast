from PyQt5.QtWidgets import QApplication
import sys
from user_interface import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()
    del window, app
    exit()
