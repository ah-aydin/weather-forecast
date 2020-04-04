import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PIL.ImageQt import ImageQt
import scrap_data

class Window(QMainWindow):
    
    style = """
        QMainWindow{
            background-color: #182C41;
            border: 2px #0A0A0A
        }
    """
    
    def __init__(self):
        super().__init__()

        self.initWindow()
        self.initInput()
        self.initInfo()
        self.initOutput()
        self.initWindowLayout()

        self.adjustSize()
        self.show()
    
    def initWindow(self):
        self._font = QtGui.QFont('Times New Roman', 16)
        self._font.setBold(True)

        self.display = QtWidgets.QWidget()
        self.setCentralWidget(self.display)
        self.setWindowIcon(QtGui.QIcon('weather icon.png'))
        self.move(100, 100)
        self.setWindowTitle('Weather Forecast')
        self.setFont(self._font)
        self.setStyleSheet(self.style)

    def initInput(self):
        self.searchBox = QtWidgets.QLineEdit('Type here')
        self.searchBox.setFont(QtGui.QFont('Aerial', 10))
        self.searchBox.setFixedHeight(30)
        self.searchBox.setMinimumWidth(400)
        self.searchBox.setStyleSheet('QLineEdit{background-color:#3E6B9D}')
        self.searchBox.returnPressed.connect(self.loadData)

        button = QtWidgets.QPushButton('Search')
        button.setFixedSize(100, 30)
        button.setFont(self._font)
        button.clicked.connect(self.loadData)
        button.setStyleSheet('QPushButton{background-color:#3E6B9D}')

        self.layout_search = QtWidgets.QHBoxLayout()
        self.layout_search.addWidget(self.searchBox)
        self.layout_search.addWidget(button)
    
    def initInfo(self):
        self.lb_countryFlag = QtWidgets.QLabel()
        self.lb_countryFlag.setFixedSize(32, 21)
        self.lb_countryName = QtWidgets.QLabel()
        self.lb_countryName.setFont(QtGui.QFont('Aerial', 16))
        self.lb_countryName.setFixedHeight(30)

        self.layout_info = QtWidgets.QHBoxLayout()
        self.layout_info.addWidget(self.lb_countryFlag)
        self.layout_info.addWidget(self.lb_countryName)

    def initOutput(self):
        self.outputBox = QtWidgets.QTextEdit()
        self.outputBox.setFont(self._font)
        self.outputBox.setMinimumWidth(300)
        self.outputBox.setMinimumHeight(200)
        self.outputBox.setStyleSheet('QTextEdit{background-color:#3E6B9D}')
    
    def initWindowLayout(self):
        self._layout = QtWidgets.QVBoxLayout()
        
        self._layout.addLayout(self.layout_search)
        self._layout.addLayout(self.layout_info)
        self._layout.addWidget(self.outputBox)

        self.display.setLayout(self._layout)

    def loadData(self):
        forecast, img_flag, city_name = scrap_data.get_forecast_data(self.searchBox.text())
        if forecast == None:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Critical)
            mb.setWindowTitle('Error')
            mb.setText('Could not find search result.')
            mb.setStandardButtons(QMessageBox.Ok)
            mb.exec_()
            return
        txt = ''
        for day in forecast:
            txt += str(day) + '\n'
        self.outputBox.setText(txt)
        self.lb_countryFlag.setPixmap(QtGui.QPixmap(QtGui.QImage(ImageQt(img_flag))))
        self.lb_countryName.setText(city_name)