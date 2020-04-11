import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QScrollArea
from PIL.ImageQt import ImageQt
import scrap_data

class Window(QScrollArea):
    
    style = """
        QScrollArea{
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

        #self.display = QtWidgets.QWidget()
        #self.setCentralWidget(self.display)
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
        self.searchBox.returnPressed.connect(lambda: self.loadData(self.searchBox.text()))

        button = QtWidgets.QPushButton('Search')
        button.setFixedSize(100, 30)
        button.setFont(QtGui.QFont('Aerial', 15))
        button.clicked.connect(lambda: self.loadData(self.searchBox.text()))
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
        self.initCurrentOutput()

        for i in range(13):
            
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
            labelImage.setFixedSize(60, 60)
            
            labelTemperature = QtWidgets.QLabel()
            font = QtGui.QFont("Aerial", 18)
            labelTemperature.setFont(font)
            labelTemperature.setAlignment(Qt.AlignCenter)
            labelTemperature.setWordWrap(True)
            labelTemperature.setMinimumWidth(200)
            labelTemperature.setFixedHeight(30)

            labelPrecipitation = QtWidgets.QLabel()
            font = QtGui.QFont("Aerial", 12)
            labelPrecipitation.setFont(font)
            labelPrecipitation.setAlignment(Qt.AlignCenter)
            labelPrecipitation.setMinimumWidth(200)
            labelPrecipitation.setFixedHeight(30)

            weatherLayout.addWidget(labelDate)
            weatherLayout.addWidget(labelWeather)
            weatherLayout.addSpacerItem(QtWidgets.QSpacerItem(1, 30))
            weatherLayout.addWidget(labelImage)
            weatherLayout.addSpacerItem(QtWidgets.QSpacerItem(1, 20))
            weatherLayout.addWidget(labelTemperature)
            weatherLayout.addWidget(labelPrecipitation)

            labelGroup.append(labelDate)
            labelGroup.append(labelWeather)
            labelGroup.append(labelImage)
            labelGroup.append(labelTemperature)
            labelGroup.append(labelPrecipitation)

            for label in labelGroup:
                weatherLayout.setAlignment(label, Qt.AlignHCenter)
            weatherLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
            weatherLayout.setSpacing(2)
            self.labelGroups.append(labelGroup)

            weatherGroupBox = QtWidgets.QGroupBox()
            weatherGroupBox.setLayout(weatherLayout)
            weatherGroupBox.setStyleSheet('background-color:#FFFFFF')
            self.outputLayout.addWidget(weatherGroupBox)

    def initCurrentOutput(self):
        currentDayLayout = QtWidgets.QVBoxLayout()

        labelDate = QtWidgets.QLabel()
        labelDate.setFont(QtGui.QFont("Aerial", 17))
        labelDate.setMinimumWidth(200)
        labelDate.setFixedHeight(30)
        labelDate.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        labelWeather = QtWidgets.QLabel()
        labelWeather.setFont(QtGui.QFont("Aerial", 16))
        labelWeather.setMinimumWidth(800)
        labelWeather.setFixedHeight(30)
        labelWeather.setWordWrap(True)
        labelWeather.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        dateLayout = QtWidgets.QVBoxLayout()
        dateLayout.addWidget(labelDate)
        dateLayout.setAlignment(labelDate, Qt.AlignTop | Qt.AlignLeft)
        dateLayout.addWidget(labelWeather)
        dateLayout.setAlignment(labelWeather, Qt.AlignTop | Qt.AlignLeft)

        labelImage = QtWidgets.QLabel()
        labelImage.setFixedSize(80, 80)
        
        labelTemperature = QtWidgets.QLabel()
        labelTemperature.setFont(QtGui.QFont("Aerial", 20))
        labelTemperature.setMinimumWidth(50)
        labelTemperature.setFixedHeight(40)
        labelTemperature.setAlignment(Qt.AlignCenter)

        labelPrecipitation = QtWidgets.QLabel()
        labelPrecipitation.setFont(QtGui.QFont("Aerial", 16))
        labelPrecipitation.setFixedHeight(24)
        labelPrecipitation.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        labelHumidity = QtWidgets.QLabel()
        labelHumidity.setFont(QtGui.QFont("Aerial", 16))
        labelHumidity.setFixedHeight(24)
        labelHumidity.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        labelWind = QtWidgets.QLabel()
        labelWind.setFont(QtGui.QFont("Aerial", 16))
        labelWind.setFixedHeight(24)
        labelWind.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        subLayout = QtWidgets.QVBoxLayout()
        subLayout.addWidget(labelPrecipitation)
        subLayout.setAlignment(labelPrecipitation, Qt.AlignLeft | Qt.AlignVCenter)
        subLayout.addWidget(labelHumidity)
        subLayout.setAlignment(labelHumidity, Qt.AlignLeft | Qt.AlignVCenter)
        subLayout.addWidget(labelWind)
        subLayout.setAlignment(labelWind, Qt.AlignLeft | Qt.AlignVCenter)

        weatherLayout = QtWidgets.QHBoxLayout()
        weatherLayout.addWidget(labelImage)
        weatherLayout.setAlignment(labelImage, Qt.AlignLeft | Qt.AlignHCenter)
        weatherLayout.addWidget(labelTemperature)
        weatherLayout.setAlignment(labelTemperature, Qt.AlignLeft | Qt.AlignHCenter)
        weatherLayout.addSpacerItem(QtWidgets.QSpacerItem(300, 1))
        weatherLayout.addLayout(subLayout)
        weatherLayout.setAlignment(subLayout, Qt.AlignRight)

        currentDayLayout.addLayout(dateLayout)
        currentDayLayout.setAlignment(dateLayout, Qt.AlignTop | Qt.AlignLeft)
        currentDayLayout.addLayout(weatherLayout)
        currentDayLayout.setAlignment(weatherLayout, Qt.AlignTop | Qt.AlignLeft)
        self.currentDayGroupBox = QtWidgets.QGroupBox()
        self.currentDayGroupBox.setStyleSheet('background-color:#FFFFFF')
        self.currentDayGroupBox.setFixedHeight(200)
        self.currentDayGroupBox.setLayout(currentDayLayout)

        self.labelGroups.append([labelDate, labelWeather, labelImage, labelTemperature, labelPrecipitation, labelHumidity, labelWind])

    def initWindowLayout(self):
        self.topLayout = QtWidgets.QFormLayout()
        
        self.topLayout.addRow(self.layout_search)
        self.topLayout.addRow(self.layout_info)
        self.topLayout.addRow(self.currentDayGroupBox)

        groupBox = QtWidgets.QGroupBox()
        self.outputLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        groupBox.setLayout(self.outputLayout)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedHeight(275)
        self.scrollArea.hide()
        self.topLayout.addRow(self.scrollArea)
        self.topLayout.setSpacing(5)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.topLayout)

        self.setLayout(self.mainLayout)
        self.loadData("Bucharest")

    def loadData(self, city):
        forecast, img_flag, city_name = scrap_data.get_forecast_data(city)
        if forecast == None:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Critical)
            mb.setWindowTitle('Error')
            mb.setText('Could not find search result.')
            mb.setStandardButtons(QMessageBox.Ok)
            mb.exec_()
            return
        
        self.labelGroups[0][0].setText(forecast[0].day_of_the_week)
        self.labelGroups[0][1].setText(forecast[0].weather[0] + forecast[0].weather[1:].lower())
        self.labelGroups[0][2].setPixmap(QtGui.QPixmap(QtGui.QImage(ImageQt(forecast[0].image))).scaled(80, 80, Qt.KeepAspectRatio))
        self.labelGroups[0][3].setText(forecast[0].temperature)
        self.labelGroups[0][4].setText("Precipitation: " + forecast[0].p_chance)
        self.labelGroups[0][5].setText("Humidity: " + forecast[0].humidity)
        self.labelGroups[0][6].setText("Wind: " + forecast[0].wind)

        for i in range(1, 14):
            day = forecast[i]
            labelGroup = self.labelGroups[i]
            labelGroup[0].setText(day.day_of_the_week)
            labelGroup[1].setText(day.weather)
            labelGroup[2].setPixmap(QtGui.QPixmap(QtGui.QImage(ImageQt(day.image))).scaled(60, 60, Qt.KeepAspectRatio))
            labelGroup[3].setText(day.temperature)
            labelGroup[4].setText(day.p_chance)

        self.lb_countryFlag.setPixmap(QtGui.QPixmap(QtGui.QImage(ImageQt(img_flag))))
        self.lb_countryName.setText(city_name)
        self.scrollArea.show()
        if not self.adjusted:
            self.adjustSize()
            self.adjusted = True