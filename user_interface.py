import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QDialog
import scrap_data

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initWindow()
        self.initInput()
        self.initOutput()
        self.initWindowLayout()

        self.adjustSize()
        self.show()
    
    def initWindow(self):
        self._font = QtGui.QFont('Times New Roman', 16)
        self._font.setBold(True)

        self.display = QtWidgets.QWidget()
        self.setCentralWidget(self.display)
        self.setGeometry(100, 100, 1600, 900)
        self.setWindowTitle('Weather Forecast')
        self.setFont(self._font)

    def initInput(self):
        self.searchBox = QtWidgets.QTextEdit('Type here')
        self.searchBox.setFont(QtGui.QFont('Aerial', 10))
        self.searchBox.setFixedSize(400, 30)

        button = QtWidgets.QPushButton('Search')
        button.setFixedSize(100, 30)
        button.setFont(self._font)
        button.clicked.connect(self.loadData)

        self.layout_search = QtWidgets.QHBoxLayout()
        self.layout_search.addWidget(self.searchBox)
        self.layout_search.addWidget(button)
    
    def initOutput(self):
        self.outputBox = QtWidgets.QTextEdit()
        self.outputBox.setFont(self._font)
        self.outputBox.setMinimumWidth(800)
        self.outputBox.setMinimumHeight(600)
    
    def initWindowLayout(self):
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addLayout(self.layout_search)
        self._layout.addWidget(self.outputBox)
        self.display.setLayout(self._layout)

    def loadData(self):
        forecast = scrap_data.get_forecast_data(self.searchBox.toPlainText())
        txt = ''
        for day in forecast:
            txt += str(day) + '\n'
        self.outputBox.setText(txt)