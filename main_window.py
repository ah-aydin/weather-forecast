import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PIL.ImageQt import ImageQt
import scrap_data

class Window(QMainWindow):
    
    style = """
        QMainWindow{
            background-color: #D3D3D3;
            border: 2px #0A0A0A
        }
    """
    
    def __init__(self):
        super().__init__()

        self.adjusted = False

        self.smallFont = QtGui.QFont('Aerial', 9)
        self.normalFont = QtGui.QFont('Aerial', 11)
        self.normalFontBold = QtGui.QFont('Aerial', 11)
        self.normalFontBold.setBold(True)
        self.bigFont = QtGui.QFont('Aerial', 20)

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
        label.setFont(self.normalFont)
        label.setFixedWidth(40)

        self.searchBox = QtWidgets.QLineEdit('Type here')
        self.searchBox.setFont(QtGui.QFont('Aerial', 10))
        self.searchBox.setFixedHeight(30)
        self.searchBox.setMinimumWidth(400)
        self.searchBox.setStyleSheet('QLineEdit{background-color:#FAFAFA}')
        self.searchBox.returnPressed.connect(self.loadData)

        button = QtWidgets.QPushButton('Search')
        button.setFixedSize(100, 30)
        button.setFont(self._font)
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
        self.outputLayout = QtWidgets.QFormLayout()

        rowLayout = QtWidgets.QHBoxLayout()

        self.labelGroups = []
        for i in range(1, 15):
            labelGroup = []

            #########################
            ### DAY LAYOUT
            #########################
            label_weekDay = QtWidgets.QLabel()
            label_weekDay.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label_weekDay.setFont(self.smallFont)
            label_weekDay.setStyleSheet('background-color: #00FF00')
            labelGroup.append(label_weekDay)

            label_month = QtWidgets.QLabel()
            label_month.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label_month.setFont(self.normalFontBold)
            label_month.setStyleSheet('background-color: #00AA00')
            label_month.setFixedWidth(70)
            labelGroup.append(label_month)

            dayLayout = QtWidgets.QVBoxLayout()
            dayLayout.addWidget(label_weekDay)
            dayLayout.addWidget(label_month)

            #########################
            ### CONDITIONS GROUP
            #########################
            img_weather = QtWidgets.QLabel()
            img_weather.setFixedSize(40, 40)
            labelGroup.append(img_weather)

            label_temperature = QtWidgets.QLabel()
            label_temperature.setAlignment(Qt.AlignCenter)
            label_temperature.setFont(self.normalFont)
            label_temperature.setStyleSheet('background-color:#FF0000')
            label_temperature.setMinimumWidth(80)
            labelGroup.append(label_temperature)
            
            label_weather = QtWidgets.QLabel()
            label_weather.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            label_weather.setFont(self.normalFont)
            label_weather.setStyleSheet('background-color:#BB0000')
            label_weather.setMinimumWidth(280)
            labelGroup.append(label_weather)

            conditionsLayout = QtWidgets.QHBoxLayout()
            conditionsLayout.addWidget(img_weather)
            conditionsLayout.addWidget(label_temperature)
            conditionsLayout.addWidget(label_weather)

            #########################
            ### COMFORT GROUP
            #########################
            label_feelsLike = QtWidgets.QLabel()
            label_feelsLike.setAlignment(Qt.AlignCenter)
            label_feelsLike.setFont(self.normalFont)
            label_feelsLike.setStyleSheet('background-color:#0000FF')
            label_feelsLike.setMinimumWidth(80)
            labelGroup.append(label_feelsLike)

            label_wind = QtWidgets.QLabel()
            label_wind.setAlignment(Qt.AlignCenter)
            label_wind.setFont(self.normalFont)
            label_wind.setStyleSheet('background-color:#0000AA')
            label_wind.setMinimumWidth(80)
            labelGroup.append(label_wind)

            label_humidity = QtWidgets.QLabel()
            label_humidity.setAlignment(Qt.AlignCenter)
            label_humidity.setFont(self.normalFont)
            label_humidity.setStyleSheet('background-color:#000088')
            label_humidity.setMinimumWidth(80)
            labelGroup.append(label_humidity)

            comfortLayout = QtWidgets.QHBoxLayout()
            comfortLayout.addWidget(label_feelsLike)
            comfortLayout.addWidget(label_wind)
            conditionsLayout.addWidget(label_humidity)

            #########################
            ### PRECIPITATION GROUP
            #########################
            label_chance = QtWidgets.QLabel()
            label_chance.setAlignment(Qt.AlignCenter)
            label_chance.setFont(self.normalFont)
            label_chance.setStyleSheet('background-color:#FFFF33')
            label_chance.setMinimumWidth(80)
            labelGroup.append(label_chance)

            label_amount = QtWidgets.QLabel()
            label_amount.setAlignment(Qt.AlignCenter)
            label_amount.setFont(self.normalFont)
            label_amount.setStyleSheet('background-color:#FFFF00')
            label_amount.setMinimumWidth(110)
            labelGroup.append(label_amount)

            precipitationLayout = QtWidgets.QHBoxLayout()
            precipitationLayout.addWidget(label_chance)
            precipitationLayout.addWidget(label_amount)
            #########################
            ### SUN GROUP
            #########################
            label_UV = QtWidgets.QLabel()
            label_UV.setAlignment(Qt.AlignCenter)
            label_UV.setFont(self.normalFont)
            label_UV.setStyleSheet('background-color:#9400D3')
            label_UV.setMinimumWidth(160)
            labelGroup.append(label_UV)

            label_sunrise = QtWidgets.QLabel()
            label_sunrise.setAlignment(Qt.AlignCenter)
            label_sunrise.setFont(self.normalFont)
            label_sunrise.setStyleSheet('background-color:#8B008B')
            label_sunrise.setMinimumWidth(80)
            labelGroup.append(label_sunrise)

            label_sunset = QtWidgets.QLabel()
            label_sunset.setAlignment(Qt.AlignCenter)
            label_sunset.setFont(self.normalFont)
            label_sunset.setStyleSheet('background-color:#4B0082')
            label_sunset.setMinimumWidth(80)
            labelGroup.append(label_sunset)
            
            sunLayout = QtWidgets.QHBoxLayout()
            sunLayout.addWidget(label_UV)
            sunLayout.addWidget(label_sunrise)
            sunLayout.addWidget(label_sunset)

            #########################
            ### ROW LAYOUT
            #########################
            rowLayout = QtWidgets.QHBoxLayout()
            rowLayout.addLayout(dayLayout)
            rowLayout.addLayout(conditionsLayout)
            rowLayout.addLayout(comfortLayout)
            rowLayout.addLayout(precipitationLayout)
            rowLayout.addLayout(sunLayout)
            groupBox = QtWidgets.QGroupBox()
            groupBox.setLayout(rowLayout)
            groupBox.setStyleSheet('background-color:#D0D0D0')
            self.outputLayout.addRow(groupBox)

            self.labelGroups.append(labelGroup)

    def initWindowLayout(self):
        self._layout = QtWidgets.QVBoxLayout()
        
        self._layout.addLayout(self.layout_search)
        self._layout.addLayout(self.layout_info)

        groupBox = QtWidgets.QGroupBox()
        groupBox.setLayout(self.outputLayout)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.hide()
        self._layout.addWidget(self.scrollArea)

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
            
        for i in range(14):
            day = forecast[i]
            labelGroup = self.labelGroups[i]
            labelGroup[0].setText(day.day_of_the_week)
            labelGroup[1].setText(day.day_of_the_month + ' ' + day.month)
            labelGroup[2].setPixmap(QtGui.QPixmap(QtGui.QImage(ImageQt(day.image))))
            labelGroup[3].setText(day.temperature)
            labelGroup[4].setText(day.weather)
            labelGroup[5].setText(day.feels_like)
            labelGroup[6].setText(day.wind)
            labelGroup[7].setText(day.humidity)
            labelGroup[8].setText(day.p_chance)
            labelGroup[9].setText(day.p_ammount)
            labelGroup[10].setText(day.UV)
            labelGroup[11].setText(day.sunrise)
            labelGroup[12].setText(day.sunset)
        self.lb_countryFlag.setPixmap(QtGui.QPixmap(QtGui.QImage(ImageQt(img_flag))))
        self.lb_countryName.setText(city_name)
        self.scrollArea.show()
        if not self.adjusted:
            self.adjustSize()
            self.adjusted = True