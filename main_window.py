import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
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
        self.outputLayout = QtWidgets.QGridLayout()

        self.labelGroups = []
        for i in range(1, 15):

            labelGroup = []
            vspacer = QtWidgets.QLabel()
            vspacer.setFixedHeight(6)
            hspacer = QtWidgets.QLabel()
            hspacer.setFixedWidth(10)

            ############################
            ### DAY LAYOUT
            ############################
            dayLayout = QtWidgets.QVBoxLayout()
            dayLayout.addWidget(vspacer)

            daySubLayout = QtWidgets.QGridLayout()
            daySubLayout.addWidget(hspacer, 0, 0)
            daySubLayout.addWidget(hspacer, 1, 0)

            label_weekDay = QtWidgets.QLabel()
            label_weekDay.setFont(self.smallFont)
            label_weekDay.setMaximumWidth(60)
            labelGroup.append(label_weekDay)
            daySubLayout.addWidget(label_weekDay, 0, 1)

            label_month = QtWidgets.QLabel()
            label_month.setFont(self.normalFontBold)
            label_month.setMaximumWidth(60)
            labelGroup.append(label_month)
            daySubLayout.addWidget(label_month, 1, 1)
            daySubLayout.addWidget(hspacer)
            
            dayLayout.addLayout(daySubLayout)
            dayLayout.addWidget(vspacer)
            
            self.outputLayout.addLayout(dayLayout, i, 0)

            ############################
            ### CONDITIONS LAYOUT
            ############################
            conditionsLayout = QtWidgets.QVBoxLayout()
            conditionsLayout.addWidget(vspacer)

            conditionsSubLayout = QtWidgets.QHBoxLayout()
            conditionsSubLayout.addWidget(hspacer)

            img_weather = QtWidgets.QLabel()
            img_weather.setFixedSize(40, 40)
            labelGroup.append(img_weather)
            conditionsSubLayout.addWidget(img_weather)

            spacer1 = QtWidgets.QLabel()
            spacer1.setFixedWidth(20)
            conditionsSubLayout.addWidget(spacer1)

            label_temperature = QtWidgets.QLabel()
            label_temperature.setMaximumWidth(90)
            label_temperature.setFont(self.normalFont)
            labelGroup.append(label_temperature)
            conditionsSubLayout.addWidget(label_temperature)

            spacer2 = QtWidgets.QLabel()
            spacer2.setFixedWidth(30)
            conditionsSubLayout.addWidget(spacer2)

            label_weather = QtWidgets.QLabel()
            label_weather.setFont(self.normalFont)
            label_weather.setMaximumWidth(170)
            labelGroup.append(label_weather)
            conditionsSubLayout.addWidget(label_weather)

            conditionsLayout.addLayout(conditionsSubLayout)
            conditionsLayout.addWidget(vspacer)

            self.outputLayout.addLayout(conditionsLayout, i, 1)

            ############################
            ### COMFORT LAYOUT
            ############################
            comfortLayout = QtWidgets.QVBoxLayout()
            comfortLayout.addWidget(vspacer)

            comfortSubLayout = QtWidgets.QHBoxLayout()
            comfortSubLayout.addWidget(hspacer)

            label_feelsLike = QtWidgets.QLabel()
            label_feelsLike.setMaximumWidth(50)
            label_feelsLike.setFont(self.normalFont)
            labelGroup.append(label_feelsLike)
            comfortSubLayout.addWidget(label_feelsLike)

            spacer1 = QtWidgets.QLabel()
            spacer1.setFixedWidth(20)
            comfortSubLayout.addWidget(spacer1)

            label_wind = QtWidgets.QLabel()
            label_wind.setMaximumWidth(90)
            label_wind.setFont(self.normalFont)
            labelGroup.append(label_wind)
            comfortSubLayout.addWidget(label_wind)

            spacer2 = QtWidgets.QLabel()
            spacer2.setFixedWidth(30)
            comfortSubLayout.addWidget(spacer2)

            label_humidity = QtWidgets.QLabel()
            label_humidity.setFont(self.normalFont)
            label_humidity.setMaximumWidth(70)
            labelGroup.append(label_humidity)
            comfortSubLayout.addWidget(label_humidity)

            comfortLayout.addLayout(comfortSubLayout)
            comfortLayout.addWidget(vspacer)
            self.outputLayout.addLayout(comfortLayout, i, 2)

            ############################
            ### PRECIPITATION LAYOUT
            ############################
            precipitationLayout = QtWidgets.QVBoxLayout()
            precipitationLayout.addWidget(vspacer)

            precipitationSubLayout = QtWidgets.QHBoxLayout()
            precipitationSubLayout.addWidget(hspacer)

            label_chance = QtWidgets.QLabel()
            label_chance.setMaximumWidth(50)
            label_chance.setFont(self.normalFont)
            labelGroup.append(label_chance)
            precipitationSubLayout.addWidget(label_chance)

            spacer1 = QtWidgets.QLabel()
            spacer1.setFixedWidth(20)
            precipitationSubLayout.addWidget(spacer1)

            label_amount = QtWidgets.QLabel()
            label_amount.setMaximumWidth(90)
            label_amount.setFont(self.normalFont)
            labelGroup.append(label_amount)
            precipitationSubLayout.addWidget(label_amount)

            precipitationLayout.addLayout(precipitationSubLayout)
            precipitationLayout.addWidget(vspacer)
            self.outputLayout.addLayout(precipitationLayout, i, 3)

            ############################
            ### SUN LAYOUT
            ############################
            sunLayout = QtWidgets.QVBoxLayout()
            sunLayout.addWidget(vspacer)

            sunSubLayout = QtWidgets.QHBoxLayout()
            sunSubLayout.addWidget(hspacer)

            label_UV = QtWidgets.QLabel()
            label_UV.setMaximumWidth(100)
            label_UV.setFont(self.normalFont)
            labelGroup.append(label_UV)
            sunSubLayout.addWidget(label_UV)

            spacer1 = QtWidgets.QLabel()
            spacer1.setFixedWidth(20)
            sunSubLayout.addWidget(spacer1)

            label_sunrise = QtWidgets.QLabel()
            label_sunrise.setMaximumWidth(70)
            label_sunrise.setFont(self.normalFont)
            labelGroup.append(label_sunrise)
            sunSubLayout.addWidget(label_sunrise)

            spacer2 = QtWidgets.QLabel()
            spacer2.setFixedWidth(30)
            sunSubLayout.addWidget(spacer2)

            label_sunset = QtWidgets.QLabel()
            label_sunset.setFont(self.normalFont)
            label_sunset.setMaximumWidth(70)
            labelGroup.append(label_sunset)
            sunSubLayout.addWidget(label_sunset)

            sunLayout.addLayout(sunSubLayout)
            sunLayout.addWidget(vspacer)
            self.outputLayout.addLayout(sunLayout, i, 4)

            self.labelGroups.append(labelGroup)

    
    def initWindowLayout(self):
        self._layout = QtWidgets.QVBoxLayout()
        
        self._layout.addLayout(self.layout_search)
        self._layout.addLayout(self.layout_info)
        self._layout.addLayout(self.outputLayout)

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