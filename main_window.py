import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PIL.ImageQt import ImageQt
import scrap_data

class Window(QMainWindow):
    
    style = """
        QMainWindow{
            background-color: #FFFFFF;
            border: 2px #0A0A0A
        }
    """
    
    def __init__(self):
        super().__init__()

        self.adjusted = False

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
        
        label = QtWidgets.QLabel('City: ')
        label.setFont(QtGui.QFont('Aerial', 15))
        label.setFixedWidth(40)

        self.searchBox = QtWidgets.QLineEdit('Type here')
        self.searchBox.setFont(QtGui.QFont('Aerial', 10))
        self.searchBox.setFixedHeight(30)
        self.searchBox.setMinimumWidth(400)
        self.searchBox.setStyleSheet('QLineEdit{background-color:#FAFAFA}')
        self.searchBox.returnPressed.connect(self.loadData)

        button = QtWidgets.QPushButton('Search')
        button.setFixedSize(100, 30)
        button.setFont(QtGui.QFont('Aerial', 15))
        button.clicked.connect(self.loadData)
        button.setStyleSheet('QPushButton{background-color:#FAFAFA}')

        self.layout_search = QtWidgets.QHBoxLayout()
        self.layout_search.addWidget(label)
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
        self.outputLayout = QtWidgets.QHBoxLayout()

        self.labelGroups = []
        for i in range(7):
            
            labelGroup = []

            weatherLayout = QtWidgets.QVBoxLayout()

            labelDate = QtWidgets.QLabel()
            font = QtGui.QFont("Aerial", 15)
            labelDate.setFont(font)
            labelDate.setAlignment(Qt.AlignCenter)
            labelDate.setMinimumWidth(50)
            labelDate.setFixedHeight(24)
            
            labelWeather = QtWidgets.QLabel()
            font = QtGui.QFont("Aerial", 8)
            labelWeather.setFont(font)
            labelWeather.setAlignment(Qt.AlignCenter)
            labelWeather.setMinimumWidth(200)
            labelWeather.setFixedHeight(14)

            labelImage = QtWidgets.QLabel()
            labelImage.setFixedSize(40, 40)
            labelImage.setStyleSheet('background-color:#00868B')
            
            labelTemperature = QtWidgets.QLabel()
            font = QtGui.QFont("Aerial", 18)
            labelTemperature.setFont(font)
            labelWeather.setAlignment(Qt.AlignCenter)
            labelWeather.setMinimumWidth(200)
            labelWeather.setFixedHeight(30)

            weatherLayout.addWidget(labelDate)
            weatherLayout.addWidget(labelWeather)
            weatherLayout.addSpacerItem(QtWidgets.QSpacerItem(1, 30))
            weatherLayout.addWidget(labelImage)
            weatherLayout.addSpacerItem(QtWidgets.QSpacerItem(1, 20))
            weatherLayout.addWidget(labelTemperature)

            labelGroup.append(labelDate)
            labelGroup.append(labelWeather)
            labelGroup.append(labelImage)
            labelGroup.append(labelTemperature)

            for label in labelGroup:
                weatherLayout.setAlignment(label, Qt.AlignHCenter)
            weatherLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
            weatherLayout.setSpacing(2)
            self.labelGroups.append(labelGroup)

            weatherGroupBox = QtWidgets.QGroupBox()
            weatherGroupBox.setLayout(weatherLayout)
            weatherGroupBox.setStyleSheet('background-color:#00868B')
            self.outputLayout.addWidget(weatherGroupBox)
            
    def initWindowLayout(self):
        self._layout = QtWidgets.QVBoxLayout()
        
        self._layout.addLayout(self.layout_search)
        self._layout.addLayout(self.layout_info)

        groupBox = QtWidgets.QGroupBox()
        self.outputLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        groupBox.setLayout(self.outputLayout)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumWidth(1600)
        self.scrollArea.setMaximumHeight(500)
        self.scrollArea.hide()
        self._layout.addWidget(self.scrollArea)

        self.display.setLayout(self._layout)

    def loadData(self):
        forecast, img_flag, city_name = scrap_data.get_forecast_data(self.searchBox.text())
        city_name = city_name.replace("14", "7")
        if forecast == None:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Critical)
            mb.setWindowTitle('Error')
            mb.setText('Could not find search result.')
            mb.setStandardButtons(QMessageBox.Ok)
            mb.exec_()
            return
            
        for i in range(7):
            day = forecast[i]
            labelGroup = self.labelGroups[i]
            labelGroup[0].setText(day.day_of_the_week)
            labelGroup[1].setText(day.weather)
            labelGroup[2].setPixmap(QtGui.QPixmap(QtGui.QImage(ImageQt(day.image))))
            labelGroup[3].setText(day.temperature)
            
        self.lb_countryFlag.setPixmap(QtGui.QPixmap(QtGui.QImage(ImageQt(img_flag))))
        self.lb_countryName.setText(city_name)
        self.scrollArea.show()
        if not self.adjusted:
            self.adjustSize()
            self.adjusted = True
        print(self.scrollArea.size())